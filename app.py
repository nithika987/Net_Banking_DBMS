from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import time  # Import the time module
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to MySQL Database
db = mysql.connector.connect(
    host="localhost",
    user="root",  # replace with your MySQL username
    password="eshSpecialtopic78",  # replace with your MySQL password
    database="net_banking"
)
cursor = db.cursor()

LOCKOUT_DURATION = 300  # Lockout duration in seconds (5 minutes)

@app.route('/')
def home():
    return render_template('login.html', attempts=0)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Check if user is locked out
    if 'login_attempts' in session:
        if session['login_attempts'] >= 3:
            lockout_time = session.get('lockout_time', 0)
            if time.time() < lockout_time:
                remaining_time = int(lockout_time - time.time())
                error_message = f"You are locked out. Try again in {remaining_time} seconds."
                return render_template('login.html', error=error_message, attempts=session['login_attempts'])

    cursor = db.cursor(buffered=True)
    query = "SELECT customer_id, role FROM Login WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()

    if result:
        session['customer_id'] = result[0]
        session['role'] = result[1]
        session['login_attempts'] = 0
        session.pop('lockout_time', None)
        
        if result[1] == 'manager':
            cursor = db.cursor(buffered=True)
    
            # Step 1: Retrieve the login_id for the manager based on the username
            query_login_id = "SELECT login_id FROM Login WHERE username = %s"
            cursor.execute(query_login_id, (username,))
            login_id_result = cursor.fetchone()
            
            if login_id_result:
                login_id = login_id_result[0]  # Get login_id from result
                print(f"Login ID Retrieved: {login_id}")  # Debug print
                session['login_id'] = login_id  # Store login_id in session

                # Step 2: Use login_id to retrieve the manager’s employee_email
                query_email = "SELECT employee_email FROM Employee WHERE login_id = %s"
                print(login_id)
                cursor.execute(query_email, (login_id,))
                manager_email = cursor.fetchone()

                if manager_email:
                    session['employee_email'] = manager_email[0]  # Store employee_email in session
                    print(f"Manager Email Retrieved: {manager_email[0]}")  # Debug print
            cursor.close()
            return redirect(url_for('manager_dashboard'))
            
        else:
            return redirect(url_for('dashboard'))
    else:
        if 'login_attempts' not in session:
            session['login_attempts'] = 0
        session['login_attempts'] += 1

        if session['login_attempts'] >= 3:
            session['lockout_time'] = time.time() + LOCKOUT_DURATION
            error_message = "You have reached 3 failed login attempts. You are locked out for 5 minutes."
        else:
            error_message = "Invalid username or password"

        return render_template('login.html', error=error_message, attempts=session['login_attempts'])

'''
@app.route('/dashboard')
def dashboard():
    if 'customer_id' in session:
        customer_id = session['customer_id']
        query = "SELECT account_id, account_type, balance FROM Account WHERE customer_id=%s"
        cursor.execute(query, (customer_id,))
        accounts = cursor.fetchall()
        print(accounts)
        return render_template('dashboard.html', accounts=accounts)
    else:
        return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'customer_id' in session:
        customer_id = session['customer_id']
        query = "SELECT account_id, account_type, balance FROM Account WHERE customer_id=%s"
        cursor.execute(query, (customer_id,))
        accounts = cursor.fetchall()
        print(accounts)
        return render_template('dashboard.html', accounts=accounts)
    else:
        return redirect(url_for('home'))
'''

@app.route('/dashboard')
def dashboard():
    if 'customer_id' in session and session.get('role') == 'customer':
        customer_id = session['customer_id']
        
        cursor = db.cursor(buffered=True)
        
        # Fetch account details
        query_accounts = "SELECT * FROM CustomerAcc WHERE customer_id = %s"
        cursor.execute(query_accounts, (customer_id,))
        accounts = cursor.fetchall()
        print(accounts)

        # Fetch matured FDs for alerts (alerted = 0 means not alerted)
        query_alerts = """
        SELECT fd_id, fd_amount, fd_end_date 
        FROM FixedDeposits 
        WHERE customer_id = %s AND alerted = 1
        """
        cursor.execute(query_alerts, (customer_id,))
        maturity_alerts = cursor.fetchall()

        # Update alerts for FDs that reached maturity today
        update_alerts = "UPDATE FixedDeposits SET alerted = 1 WHERE fd_end_date = CURDATE() AND customer_id = %s"
        cursor.execute(update_alerts, (customer_id,))
        db.commit()

        # Fetch Pending and Accepted Fixed Deposits (FDs)
        query_fds = """
        SELECT fd_id, fd_amount, fd_duration, fd_interest_rate, fd_start_date, fd_end_date, status
        FROM FixedDeposits 
        WHERE customer_id = %s and status='Pending'
        """
        #print(query_fds)
        cursor.execute(query_fds, (customer_id,))
        fds = cursor.fetchall()
        print(fds)

        cursor.close()

        # Render the dashboard with accounts, alerts, and FDs data
        return render_template('dashboard.html', accounts=accounts, alerts=maturity_alerts, pending_fds=fds)
    
    else:
        return redirect(url_for('home'))
'''
@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if 'customer_id' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Process transaction
        customer_id = session['customer_id']
        account_id = int(request.form['account_id'])
        transaction_type = request.form['transaction_type']  # 'deposit', 'withdrawal', or 'transfer'
        amount = float(request.form['amount'])
        
        # For transfer, get the recipient account ID
        recipient_account_id = request.form.get('recipient_account_id', None)
        if recipient_account_id:
            recipient_account_id = int(recipient_account_id)

        try:
            # Call the stored procedure with all required parameters
            cursor.callproc('PerformTransaction', (transaction_type, amount, account_id, customer_id, recipient_account_id))
            db.commit()
            success_message = "Transaction successful"
        except mysql.connector.Error as err:
            db.rollback()
            success_message = f"Transaction failed: {err.msg}"

        return render_template('transaction.html', message=success_message)
    
    # If GET, render the transaction form
    return render_template('transaction.html')



@app.route('/add_beneficiary', methods=['GET', 'POST'])
def add_beneficiary():
    if 'customer_id' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Process the form submission to add a beneficiary
        customer_id = session['customer_id']
        beneficiary_name = request.form['beneficiary_name']
        beneficiary_account_no = request.form['beneficiary_account_no']
        beneficiary_type = request.form['beneficiary_type']
        ifsc_code = request.form['ifsc_code']
        account_id = request.form['account_id']

        try:
            cursor.callproc('AddBeneficiary', (beneficiary_name, beneficiary_account_no, customer_id, beneficiary_type, ifsc_code, account_id))
            db.commit()
            message = "Beneficiary added successfully"
        except mysql.connector.Error as err:
            db.rollback()
            message = f"Failed to add beneficiary: {err.msg}"

        return render_template('add_beneficiary.html', message=message)

    # If GET, display the add beneficiary form
    return render_template('add_beneficiary.html')
'''
    
@app.route('/manager_dashboard')
def manager_dashboard():
    if 'employee_email' in session and session.get('role') == 'manager':
        cursor = db.cursor(buffered=True)
        
        # Fetch manager details from the view using employee_email
        query_manager = "SELECT * FROM ManagerEmployeeDetails WHERE employee_email = %s"
        cursor.execute(query_manager, (session['employee_email'],))
        manager_details = cursor.fetchone()
        
        if manager_details:
            branch_id = manager_details[4]  # Assuming branch_id is at index 4 in the manager details
            
            # Fetch customers in the manager's branch
            query_customers = "SELECT customer_id, customer_name FROM Customer WHERE branch_id = %s"
            cursor.execute(query_customers, (branch_id,))
            customers_in_branch = cursor.fetchall()  # This will be a list of tuples (customer_id, customer_name)
            
            print("Manager Details:", manager_details)
            print("Customers in Branch:", customers_in_branch)
            
            # Close the cursor
            cursor.close()
            
            # Render the template with manager and customers details
            return render_template('manager_dashboard.html', manager=manager_details, customers=customers_in_branch)
        
        cursor.close()
        return render_template('manager_dashboard.html', error="Manager details not found.")
    
    else:
        return redirect(url_for('home'))

 

@app.route('/transaction_history/<int:account_id>', methods=['GET'])
def transaction_history(account_id):
    if 'customer_id' not in session:
        return redirect(url_for('home'))

    # Retrieve optional date filters from query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    try:
        cursor = db.cursor(buffered=True)
        transactions = []

        # If both start_date and end_date are provided, use the date-filtered procedure
        if start_date and end_date:
            # Call GetTransactionsByDateRange procedure with start_date and end_date
            cursor.callproc('GetTransactionsByDateRange', (start_date, end_date))

            # Fetch the filtered transactions from the stored procedure
            for result in cursor.stored_results():
                transactions = result.fetchall()

            if not transactions:
                message = "No transactions found for the specified date range."
                return render_template('transaction_history.html', message=message, current_balance=None, account_id=account_id)
        else:
            # If no dates are provided, call GetTransactionHistory for the account_id
            cursor.callproc('GetTransactionHistory', (account_id,))

            # Fetch all transactions for the account
            for result in cursor.stored_results():
                transactions = result.fetchall()

            if not transactions:
                message = "No transactions found."
                return render_template('transaction_history.html', message=message, current_balance=None, account_id=account_id)

        # Assuming the last transaction has the most up-to-date balance
        current_balance = transactions[-1][5] if transactions else 0  # Adjust if balance is not in the 6th column

        return render_template('transaction_history.html', transactions=transactions, current_balance=current_balance, account_id=account_id)

    except mysql.connector.Error as err:
        message = f"Error fetching transaction history: {err.msg}"
        return render_template('transaction_history.html', message=message, current_balance=None, account_id=account_id)

    finally:
        # Ensure the database cursor is closed
        cursor.close()

'''
@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    # Check if customer is logged in
    if 'customer_id' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Process transaction
        customer_id = session['customer_id']
        account_id = int(request.form['account_id'])
        transaction_type = request.form['transaction_type']  # 'deposit', 'withdrawal', or 'transfer'
        amount = float(request.form['amount'])
        
        # For transfer, get the recipient account ID; otherwise, set to None
        recipient_account_id = request.form.get('recipient_account_id')
        if transaction_type == 'transfer' and recipient_account_id:
            recipient_account_id = int(recipient_account_id)  # Convert to int if it's a transfer
        else:
            recipient_account_id = None  # Set to None (NULL) for non-transfer transactions

        try:
            # Call the stored procedure with the parameters
            cursor.callproc('PerformTransaction', (
                transaction_type,
                amount,
                account_id,
                customer_id,
                recipient_account_id
            ))
            db.commit()
            success_message = "Transaction successful"
        except mysql.connector.Error as err:
            db.rollback()
            success_message = f"Transaction failed: {err.msg}"

        # Render the form with a success or error message
        return render_template('transaction.html', message=success_message)
    
    # If GET request, render the transaction form
    return render_template('transaction.html')
'''
@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    # Check if customer is logged in
    if 'customer_id' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Process transaction
        customer_id = session['customer_id']
        account_id = int(request.form['account_id'])
        transaction_type = request.form['transaction_type']  # 'deposit', 'withdrawal', or 'transfer'
        amount = float(request.form['amount'])
        
        # For transfer, get the recipient account ID; otherwise, set to None
        recipient_account_id = request.form.get('recipient_account_id')
        if transaction_type == 'transfer' and recipient_account_id:
            recipient_account_id = int(recipient_account_id)  # Convert to int if it's a transfer
        else:
            recipient_account_id = None  # Set to None (NULL) for non-transfer transactions

        try:
            # Call the stored procedure with the parameters
            cursor.callproc('PerformTransaction', (
                transaction_type,
                amount,
                account_id,
                customer_id,
                recipient_account_id
            ))
            db.commit()  # Commit the transaction if no errors

            success_message = "Transaction successful"

        except mysql.connector.Error as err:
            # If the trigger raises an error (e.g., balance below minimum), handle it here
            db.rollback()
            if err.sqlstate == '45000':  # Trigger raises this error when the balance goes below minimum
                success_message = f"Transaction failed: {err.msg}"  # Error message from the trigger
            else:
                success_message = f"Transaction failed: {err.msg}"  # Handle other MySQL errors

        # Render the form with a success or error message
        return render_template('transaction.html', message=success_message)
    
    # If GET request, render the transaction form
    return render_template('transaction.html')


@app.route('/add_beneficiary', methods=['GET', 'POST'])
def add_beneficiary():
    if 'customer_id' not in session:
        return redirect(url_for('home'))

    message = ""
    
    # If POST request, handle adding the beneficiary
    if request.method == 'POST':
        customer_id = session['customer_id']
        beneficiary_name = request.form['beneficiary_name']
        beneficiary_account_no = request.form['beneficiary_account_no']
        beneficiary_type = request.form['beneficiary_type']
        ifsc_code = request.form['ifsc_code']
        account_id = request.form['account_id']

        try:
            cursor.callproc('AddBeneficiary', (beneficiary_name, beneficiary_account_no, customer_id, beneficiary_type, ifsc_code, account_id))
            db.commit()
            message = "Beneficiary added successfully"
        except mysql.connector.Error as err:
            db.rollback()
            message = f"Failed to add beneficiary: {err.msg}"

    # Fetch beneficiaries for the current customer
    cursor.callproc('ViewBeneficiaries', (session['customer_id'],))
    beneficiaries = cursor.fetchall()

    return render_template('add_beneficiary.html', message=message, beneficiaries=beneficiaries)

'''
@app.route('/edit_beneficiary/<beneficiary_account_no>', methods=['GET', 'POST'])
def edit_beneficiary(beneficiary_account_no):
    message = ""  # or message = None if you prefer

    if 'customer_id' not in session:
        return redirect(url_for('home'))

    # If POST request, handle editing the beneficiary
    if request.method == 'POST':
        beneficiary_name = request.form['beneficiary_name']
        #beneficiary_account_no = request.form['beneficiary_account_no']  # This is now required to pass to the procedure
        beneficiary_type = request.form['beneficiary_type']
        ifsc_code = request.form['ifsc_code']
        account_id = request.form['account_id']

        try:
            # Call the stored procedure with the necessary parameters
            cursor.callproc('EditBeneficiary', (beneficiary_account_no, beneficiary_name, beneficiary_type, ifsc_code, account_id))
            db.commit()
            message = "Beneficiary updated successfully"
        except mysql.connector.Error as err:
            db.rollback()
            message = f"Failed to update beneficiary: {err.msg}"

        return redirect(url_for('edit_beneficiary', beneficiary_account_no=beneficiary_account_no))  # Redirect to the same page to see the updated details

    # Fetch the existing beneficiary details for editing
    cursor.execute("SELECT beneficiary_name, beneficiary_account_no, beneficiary_type, ifsc_code, account_id FROM Beneficiary WHERE beneficiary_account_no = %s", (beneficiary_account_no,))
    beneficiary = cursor.fetchone()

    return render_template('edit_beneficiary.html', beneficiary=beneficiary, message=message)
'''
from flask import render_template, redirect, url_for, flash, request, session
import mysql.connector

@app.route('/edit_beneficiary/<string:beneficiary_account_no>', methods=['GET', 'POST'])
def edit_beneficiary(beneficiary_account_no):
    if 'customer_id' not in session:
        return redirect(url_for('home'))  # Ensure the user is logged in
    
    # If POST request, handle editing the beneficiary
    if request.method == 'POST':
        beneficiary_name = request.form['beneficiary_name']
        beneficiary_type = request.form['beneficiary_type']
        ifsc_code = request.form['ifsc_code']
        account_id = request.form['account_id']

        try:
            # Call the stored procedure to update the beneficiary details
            cursor.callproc('EditBeneficiary', (beneficiary_account_no, beneficiary_name, beneficiary_type, ifsc_code, account_id))
            db.commit()
            
            # Flash a success message
            flash('Beneficiary updated successfully!', 'success')
        except mysql.connector.Error as err:
            db.rollback()
            # Flash an error message if the update fails
            flash(f'Failed to update beneficiary: {err.msg}', 'error')

        # Redirect to the same page to reflect the updated details
        return redirect(url_for('edit_beneficiary', beneficiary_account_no=beneficiary_account_no))

    # Fetch the existing beneficiary details for editing
    cursor.execute("SELECT beneficiary_name, beneficiary_account_no, beneficiary_type, ifsc_code, account_id FROM Beneficiary WHERE beneficiary_account_no = %s", (beneficiary_account_no,))
    beneficiary = cursor.fetchone()

    if not beneficiary:
        # Flash a message if the beneficiary is not found
        flash('Beneficiary not found', 'error')
        return render_template('edit_beneficiary.html', message="Beneficiary not found")

    return render_template('edit_beneficiary.html', beneficiary=beneficiary)



@app.route('/delete_beneficiary/<string:ben_account_no>', methods=['GET'])
def delete_beneficiary(ben_account_no):
    if 'customer_id' not in session:
        return redirect(url_for('home'))

    try:
        # Call the stored procedure, passing the beneficiary account number
        cursor.callproc('DeleteBeneficiary', (ben_account_no,))
        db.commit()
        message = "Beneficiary deleted successfully"
    except mysql.connector.Error as err:
        db.rollback()
        message = f"Failed to delete beneficiary: {err.msg}"

    # Optionally, you can return the message to the frontend or log it for debugging
    return redirect(url_for('view_beneficiary'))  # Redirect to the add beneficiary page to see the updated list

@app.route('/view_beneficiary', methods=['GET'])
def view_beneficiary():
    
    # Check if the user is logged in by checking session for 'customer_id'
    if 'customer_id' not in session:
        return redirect(url_for('home'))  # Redirect to home if not logged in

    customer_id = session['customer_id']  # Get customer ID from session
    beneficiaries = []  # List to store beneficiary data
    message = ""  # Variable to store a message for the template

    try:
        # Call the stored procedure to get beneficiaries for the customer
        cursor.callproc('ViewBeneficiaries', (customer_id,))

        # Iterate over the result set returned by the stored procedure
        for result in cursor.stored_results():
            rows = result.fetchall()  # Fetch all rows from the result set

            # Process each row and convert it to a dictionary for easier access in the template
            for row in rows:
                beneficiary = {
                    'beneficiary_name': row[0],  # Assuming 'beneficiary_name' is at index 0
                    'beneficiary_account_no': row[1],  # Assuming 'beneficiary_account_no' is at index 1
                    'beneficiary_type': row[2],  # Assuming 'beneficiary_type' is at index 2
                    'ifsc_code': row[3],  # Assuming 'ifsc_code' is at index 3
                    'account_id': row[4]  # Assuming 'account_id' is at index 4
                }
                beneficiaries.append(beneficiary)  # Add each beneficiary dictionary to the list

        # Check if there were no beneficiaries returned
        if not beneficiaries:
            message = "No beneficiaries found for this customer."
        else:
            message = "Beneficiaries fetched successfully."

    except mysql.connector.Error as err:
        # Handle any MySQL errors
        message = f"Failed to retrieve beneficiaries: {err.msg}"

    # Pass the beneficiaries list and the message to the template for rendering
    return render_template('view_beneficiary.html', beneficiaries=beneficiaries, message=message)

@app.route('/accept_fd/<int:fd_id>', methods=['POST'])
def accept_fd(fd_id):
    if 'customer_id' in session and session.get('role') == 'customer':
        customer_id = session['customer_id']
        
        cursor = db.cursor()
        
        # Update FD status to Accepted
        update_fd = "UPDATE FixedDeposits SET status = 'Accepted' WHERE fd_id = %s AND customer_id = %s"
        cursor.execute(update_fd, (fd_id, customer_id))
        db.commit()
        
        cursor.close()
        
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('home'))


@app.route('/reject_fd/<int:fd_id>', methods=['POST'])
def reject_fd(fd_id):
    if 'customer_id' in session and session.get('role') == 'customer':
        customer_id = session['customer_id']
        
        cursor = db.cursor()
        
        # Update FD status to Rejected
        update_fd = "UPDATE FixedDeposits SET status = 'Rejected' WHERE fd_id = %s AND customer_id = %s"
        cursor.execute(update_fd, (fd_id, customer_id))
        db.commit()
        
        cursor.close()
        
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('home'))

@app.route('/view_fds')
def view_fds():
    if 'customer_id' in session and session['role'] == 'customer':
        customer_id = session['customer_id']
        cursor = db.cursor()

        # Fetch accepted Fixed Deposits (FDs) only
        query = """
        SELECT fd_id,fd_amount, fd_duration, fd_interest_rate, fd_start_date, fd_end_date 
        FROM FixedDeposits 
        WHERE customer_id = %s AND status = 'Accepted'
        """
        cursor.execute(query, (customer_id,))
        accepted_fds = cursor.fetchall()
        cursor.close()

        # Render the 'view_fds.html' template with accepted FDs only
        return render_template('view_fds.html', fds=accepted_fds)
    else:
        return redirect(url_for('home'))

@app.route('/renew_fd/<int:fd_id>', methods=['POST'])
def renew_fd(fd_id):
    if 'customer_id' in session:
        customer_id = session['customer_id']
        
        # Connect to the database
        cursor = db.cursor()
        
        # Verify that the FD belongs to the logged-in customer
        check_query = "SELECT fd_id FROM FixedDeposits WHERE fd_id = %s AND customer_id = %s"
        cursor.execute(check_query, (fd_id, customer_id))
        result = cursor.fetchone()
        
        if result:
            # Renew FD by updating start and end dates
            renew_query = """
            UPDATE FixedDeposits 
            SET fd_start_date = CURDATE(), 
                fd_end_date = DATE_ADD(CURDATE(), INTERVAL 1 YEAR),
                alerted = 0,
                status = 'Accepted'  -- Corrected status assignment
            WHERE fd_id = %s AND customer_id = %s
            """
            cursor.execute(renew_query, (fd_id, customer_id))
            db.commit()
        
        cursor.close()
        return redirect(url_for('dashboard'))
    
    return redirect(url_for('home'))


@app.route('/withdraw_fd/<int:fd_id>', methods=['POST'])
def withdraw_fd(fd_id):
    if 'customer_id' in session:
        customer_id = session['customer_id']
        cursor = db.cursor()

        # Fetch FD amount
        cursor.execute("SELECT fd_amount FROM FixedDeposits WHERE fd_id = %s", (fd_id,))
        fd_amount = cursor.fetchone()[0]

        # Deposit FD amount into customer's account
        query_update_balance = """
        UPDATE CustomerAcc 
        SET balance = balance + %s 
        WHERE customer_id = %s
        """
        cursor.execute(query_update_balance, (fd_amount, customer_id))

        # Remove the FD or mark it as closed
        cursor.execute("DELETE FROM FixedDeposits WHERE fd_id = %s", (fd_id,))

        db.commit()
        cursor.close()
        return redirect(url_for('dashboard'))
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('customer_id', None)
    session.pop('login_attempts', None)  # Clear login attempts
    session.pop('lockout_time', None)  # Clear lockout time
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)