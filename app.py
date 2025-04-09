from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
import mysql.connector
from config import db_config

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# Login route
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Call the stored procedure to handle login
            cursor.callproc('LoginUser', [username, password, None, None])
            
            # Fetch the output parameters
            login_result = None
            for result in cursor.stored_results():
                login_result = result.fetchone()
            
            # Check if login_result is not None
            if login_result is not None:
                customer_id = login_result[0]
                message = login_result[1]

                # Handle login result
                if message == 'Login successful!':
                    session['customer_id'] = customer_id
                    print(f"Login successful for user: {username}, customer_id: {customer_id}")  # Debug output
                    return redirect(url_for('dashboard'))
                else:
                    flash(message, 'error')
            else:
                flash("Login failed: No response from the database.", 'error')

        except mysql.connector.Error as err:
            flash(f"Database error: {str(err)}", 'error')

        finally:
            cursor.close()
            conn.close()

    return render_template('dashboard.html')


# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'customer_id' not in session:
        return redirect(url_for('login'))

    customer_id = session['customer_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch customer information
        cursor.execute("SELECT * FROM Customer WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()

        # Fetch account information
        cursor.execute("SELECT * FROM Account WHERE customer_id = %s", (customer_id,))
        account = cursor.fetchone()

        # Fetch bank and branch information
        cursor.execute("""
            SELECT Bank.bank_name, Branch.branch_name 
            FROM Branch
            JOIN Bank ON Branch.bank_id = Bank.bank_id
            WHERE Branch.branch_id = %s
        """, (account['branch_id'],))
        bank_branch = cursor.fetchone()

        return render_template('dashboard.html', customer=customer, account=account, bank=bank_branch, branch=bank_branch)
    finally:
        cursor.close()
        conn.close()

# Logout route
@app.route('/logout')
def logout():
    session.pop('customer_id', None)
    return redirect(url_for('login'))

# Bank management route
@app.route('/banks')
def banks():
    return render_template('banks.html')

# Branch management route
@app.route('/branches')
def branches():
    return render_template('branches.html')

# Customer management route
@app.route('/customers')
def customers():
    return render_template('customers.html')

# Add this function to test the database connection
def test_db_connection():
    try:
        conn = get_db_connection()
        conn.close()
        print("Database connection successful.")
    except mysql.connector.Error as err:
        print(f"Database connection failed: {str(err)}")
        
# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
