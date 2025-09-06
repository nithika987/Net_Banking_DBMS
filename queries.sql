


-- Table: Bank
CREATE TABLE Bank (
    bank_id INT AUTO_INCREMENT PRIMARY KEY,
    bank_name VARCHAR(255) NOT NULL,
    bank_headq_address VARCHAR(255) NOT NULL,
    established_date DATE,
    bank_email VARCHAR(255),
    bank_contact_number VARCHAR(20),
    bank_website_url VARCHAR(255),
    bank_logo MEDIUMBLOB
);

-- Table: Branch
CREATE TABLE Branch (
    branch_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_name VARCHAR(255) NOT NULL,
    branch_address VARCHAR(255),
    bank_id INT,
    branch_manager_id INT,
    branch_phone VARCHAR(20),
    branch_email VARCHAR(255),
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id)
);

-- Table: Employee
CREATE TABLE Employee (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_name VARCHAR(255) NOT NULL,
    employee_position VARCHAR(255),
    employee_salary DECIMAL(10,2),
    branch_id INT,
    employee_date_of_joining DATE,
    employee_email VARCHAR(255),
    employee_phone VARCHAR(20),
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);

-- Update Branch table to include foreign key reference to Employee after creating the Employee table
ALTER TABLE Branch
    ADD CONSTRAINT fk_branch_manager FOREIGN KEY (branch_manager_id) REFERENCES Employee(employee_id);

-- Table: Customer
CREATE TABLE Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    customer_email VARCHAR(255),
    customer_phone VARCHAR(20),
    customer_address VARCHAR(255),
    customer_dob DATE,
    customer_profile_picture MEDIUMBLOB
);

-- Table: Account
CREATE TABLE Account (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    account_type VARCHAR(50),
    balance DECIMAL(15,2),
    customer_id INT,
    branch_id INT,
    account_opening_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);

-- Table: BankTransaction (renamed to avoid using reserved word 'Transaction')
CREATE TABLE BankTransaction (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_date DATE,
    transaction_type VARCHAR(50),
    amount DECIMAL(15,2),
    account_id INT,
    customer_id INT,
    FOREIGN KEY (account_id) REFERENCES Account(account_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- Table: Beneficiary
CREATE TABLE Beneficiary (
    beneficiary_name VARCHAR(255),
    beneficiary_account_no VARCHAR(20),
    customer_id INT,
    beneficiary_type VARCHAR(50),
    ifsc_code VARCHAR(11),
    account_id INT,
    PRIMARY KEY (beneficiary_account_no, customer_id),
    FOREIGN KEY (account_id) REFERENCES Account(account_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- Table: Card
CREATE TABLE Card (
    card_number VARCHAR(20) PRIMARY KEY,
    card_type VARCHAR(50),
    expiration_date DATE,
    cvv INT,
    customer_id INT,
    issue_date DATE,
    card_limit DECIMAL(15,2),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- Table: Login
CREATE TABLE Login (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    username VARCHAR(255),
    password VARCHAR(255),
    last_login DATETIME,
    account_lock_status VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

 alter table login add column failed_attempts INT DEFAULT 0;


CREATE TABLE Login (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    failed_attempts INT DEFAULT 0,
    last_login DATETIME,
    account_lock_status VARCHAR(50) DEFAULT 'UNLOCKED',
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

ALTER TABLE Employee
ADD COLUMN bank_id INT;

-- Inserting data into the Bank table
INSERT INTO Bank (bank_name, bank_headq_address, established_date, bank_email, bank_contact_number, bank_website_url) VALUES
('First National Bank', '123 Main St, Springfield, IL', '1995-05-15', 'info@firstnational.com', '123-456-7890', 'www.firstnational.com'),
('Global Finance', '456 Elm St, Capital City, CA', '2000-07-10', 'contact@globalfinance.com', '098-765-4321', 'www.globalfinance.com');

-- Inserting data into the Branch table
INSERT INTO Branch (branch_name, branch_address, bank_id, branch_manager_id, branch_phone, branch_email) VALUES
('Downtown Branch', '101 Market St, Springfield, IL', 1, NULL, '123-456-1111', 'downtown@firstnational.com'),
('Uptown Branch', '202 Broadway St, Capital City, CA', 2, NULL, '098-765-2222', 'uptown@globalfinance.com');

-- Inserting data into the Employee table
INSERT INTO Employee (employee_name, employee_position, employee_salary, branch_id, employee_date_of_joining, employee_email, employee_phone) VALUES
('Alice Smith', 'Branch Manager', 60000.00, 1, '2020-01-10', 'alice.smith@firstnational.com', '123-456-3333'),
('Bob Johnson', 'Teller', 40000.00, 1, '2021-03-15', 'bob.johnson@firstnational.com', '123-456-4444'),
('Carol White', 'Branch Manager', 65000.00, 2, '2019-08-20', 'carol.white@globalfinance.com', '098-765-5555');

-- Inserting data into the Customer table
INSERT INTO Customer (customer_name, customer_email, customer_phone, customer_address, customer_dob, customer_profile_picture) VALUES
('John Doe', 'john.doe@example.com', '123-456-7891', '789 Willow St, Springfield, IL', '1985-06-01', NULL),
('Jane Smith', 'jane.smith@example.com', '098-765-4320', '321 Oak St, Capital City, CA', '1990-12-15', NULL);

-- Inserting data into the Account table
INSERT INTO Account (account_type, balance, customer_id, branch_id, account_opening_date) VALUES
('Savings', 5000.00, 1, 1, '2021-05-01'),
('Checking', 1500.00, 2, 2, '2022-07-20');

-- Inserting data into the BankTransaction table
INSERT INTO BankTransaction (transaction_date, transaction_type, amount, account_id, customer_id) VALUES
('2023-10-01', 'Deposit', 1000.00, 1, 1),
('2023-10-05', 'Withdrawal', 500.00, 2, 2);

-- Inserting data into the Beneficiary table
INSERT INTO Beneficiary (beneficiary_name, beneficiary_account_no, customer_id, beneficiary_type, ifsc_code, account_id) VALUES
('Mark Brown', 'ACC123456789', 1, 'Family', 'IFSC0001', 1),
('Lucy Green', 'ACC987654321', 2, 'Friend', 'IFSC0002', 2);

-- Inserting data into the Card table
INSERT INTO Card (card_number, card_type, expiration_date, cvv, customer_id, issue_date, card_limit) VALUES
('CARD1234567890123', 'Debit', '2025-12-31', 123, 1, '2021-05-01', 3000.00),
('CARD9876543210987', 'Credit', '2024-11-30', 456, 2, '2022-07-20', 5000.00);

-- Inserting data into the Login table
INSERT INTO Login (customer_id, username, password, last_login, account_lock_status) VALUES
(1, 'johndoe', 'hashed_password_1', '2024-10-20 08:00:00', 'Unlocked'),
(2, 'janesmith', 'hashed_password_2', '2024-10-21 09:30:00', 'Locked');


DELIMITER //

CREATE PROCEDURE PerformTransaction(
    IN trans_type VARCHAR(50),
    IN trans_amount DECIMAL(15,2),
    IN acc_id INT,
    IN cust_id INT
)
BEGIN
    DECLARE current_balance DECIMAL(15,2);

    -- Check if the account belongs to the customer
    SELECT balance INTO current_balance FROM Account WHERE account_id = acc_id AND customer_id = cust_id;
    IF current_balance IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account not found or does not belong to customer';
    END IF;

    -- Check for sufficient balance for withdrawals
    IF trans_type = 'withdrawal' AND current_balance < trans_amount THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient balance';
    END IF;

    -- Update the balance based on transaction type
    IF trans_type = 'deposit' THEN
        UPDATE Account SET balance = balance + trans_amount WHERE account_id = acc_id;
    ELSEIF trans_type = 'withdrawal' THEN
        UPDATE Account SET balance = balance - trans_amount WHERE account_id = acc_id;
    END IF;

    -- Record the transaction
    INSERT INTO BankTransaction (transaction_date, transaction_type, amount, account_id, customer_id)
    VALUES (NOW(), trans_type, trans_amount, acc_id, cust_id);
END //

DELIMITER ;




DELIMITER //

CREATE PROCEDURE AddBeneficiary(
    IN ben_name VARCHAR(255),
    IN ben_account_no VARCHAR(20),
    IN cust_id INT,
    IN ben_type VARCHAR(50),
    IN ben_ifsc VARCHAR(11),
    IN acc_id INT
)
BEGIN
    DECLARE acc_exists INT;

    -- Check if the beneficiary's account exists
    SELECT COUNT(*) INTO acc_exists FROM Account WHERE account_id = acc_id;
    IF acc_exists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Beneficiary account not found';
    END IF;

    -- Add beneficiary
    INSERT INTO Beneficiary (beneficiary_name, beneficiary_account_no, customer_id, beneficiary_type, ifsc_code, account_id)
    VALUES (ben_name, ben_account_no, cust_id, ben_type, ben_ifsc, acc_id);
END //

DELIMITER ;




DELIMITER //
CREATE PROCEDURE GetTransactionHistory(IN p_account_id INT)
BEGIN
    SELECT 
        bt.transaction_id,
        bt.transaction_date,
        bt.transaction_type,
        bt.amount,
        a.account_type,
        a.balance,
        bt. recipient_account_id 
    FROM 
        BankTransaction bt
    INNER JOIN 
        Account a ON bt.account_id = a.account_id
    WHERE 
        bt.account_id = p_account_id
    ORDER BY 
        bt.transaction_date DESC;
END //
DELIMITER ;




DELIMITER //

CREATE PROCEDURE PerformTransaction(
    IN trans_type VARCHAR(50),
    IN trans_amount DECIMAL(15,2),
    IN acc_id INT,
    IN cust_id INT,
    IN recipient_acc_id INT -- No default value here
)
BEGIN
    DECLARE current_balance DECIMAL(15,2);

    -- Check if the account belongs to the customer
    SELECT balance INTO current_balance FROM Account WHERE account_id = acc_id AND customer_id = cust_id;
    IF current_balance IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account not found or does not belong to customer';
    END IF;

    -- Check for sufficient balance for withdrawals or transfers
    IF (trans_type = 'withdrawal' OR trans_type = 'transfer') AND current_balance < trans_amount THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient balance';
    END IF;

    -- Update the balance based on transaction type
    IF trans_type = 'deposit' THEN
        UPDATE Account SET balance = balance + trans_amount WHERE account_id = acc_id;

    ELSEIF trans_type = 'withdrawal' THEN
        UPDATE Account SET balance = balance - trans_amount WHERE account_id = acc_id;

    ELSEIF trans_type = 'transfer' THEN
        -- Check if recipient account exists and is valid
        IF recipient_acc_id IS NULL THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Recipient account ID required for transfer';
        END IF;

        UPDATE Account SET balance = balance - trans_amount WHERE account_id = acc_id; -- Deduct from sender
        UPDATE Account SET balance = balance + trans_amount WHERE account_id = recipient_acc_id; -- Add to recipient
    END IF;

    -- Record the transaction
    INSERT INTO BankTransaction (transaction_date, transaction_type, amount, account_id, customer_id, recipient_account_id)
    VALUES (NOW(), trans_type, trans_amount, acc_id, cust_id, recipient_acc_id);
END //

DELIMITER ;


ALTER TABLE BankTransaction ADD COLUMN recipient_account_id INT;

DELIMITER $$

CREATE PROCEDURE GetTransactionsByDateRange(
    IN start_date DATE,
    IN end_date DATE
)
BEGIN
    IF start_date = end_date THEN
        -- If start and end dates are the same, only retrieve transactions on that date
        SELECT * FROM banktransaction
        WHERE DATE(transaction_date) = start_date;
    ELSE
        -- Otherwise, retrieve transactions within the date range
        SELECT * FROM banktransaction
        WHERE DATE(transaction_date) BETWEEN start_date AND end_date;
    END IF;
END $$

DELIMITER ;




DELIMITER //

CREATE PROCEDURE ViewBeneficiaries(
    IN cust_id INT
)
BEGIN
    -- Select all beneficiaries for the given customer
    SELECT beneficiary_name, beneficiary_account_no, beneficiary_type, ifsc_code, account_id
    FROM beneficiary
    WHERE customer_id = cust_id;
END //

DELIMITER ;





DELIMITER //

CREATE PROCEDURE DeleteBeneficiary(
    IN ben_account_no VARCHAR(20)
)
BEGIN
    -- Delete the beneficiary with the given account number
    DELETE FROM beneficiary
    WHERE beneficiary_account_no = ben_account_no;

    -- Optionally, you can check if the deletion was successful
    IF ROW_COUNT() = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Beneficiary not found';
    END IF;
END //

DELIMITER ;



DELIMITER //

CREATE PROCEDURE EditBeneficiary(
    IN ben_account_no VARCHAR(20),
    IN ben_name VARCHAR(255),
    IN ben_type VARCHAR(50),
    IN ben_ifsc VARCHAR(11),
    IN acc_id INT
)
BEGIN
    DECLARE acc_exists INT;

    -- Check if the account exists
    SELECT COUNT(*) INTO acc_exists FROM Account WHERE account_id = acc_id;
    IF acc_exists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Beneficiary account not found';
    END IF;

    -- Update the beneficiary information
    UPDATE beneficiary
    SET beneficiary_name = ben_name,
        beneficiary_type = ben_type,
        ifsc_code = ben_ifsc,
        account_id = acc_id
    WHERE beneficiary_account_no = ben_account_no;

    -- Optionally, you can check if the update was successful
    IF ROW_COUNT() = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Beneficiary not found';
    END IF;
END //

DELIMITER ;



DELIMITER //

CREATE TRIGGER CheckMinimumBalance
AFTER UPDATE ON Account
FOR EACH ROW
BEGIN
    DECLARE minimum_balance DECIMAL(15,2) DEFAULT 100.00;

    -- Check if the balance falls below the minimum after an update
    IF NEW.balance < minimum_balance THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account balance cannot go below the minimum balance';
    END IF;
END //

DELIMITER ;


CREATE OR REPLACE VIEW ManagerEmployeeDetails AS
SELECT 
    e.employee_id,
    e.employee_name,
    e.employee_position,
    e.employee_salary,
    e.branch_id,
    e.bank_id,
    e.employee_date_of_joining,
    e.employee_email,
    e.employee_phone,
    l.username AS manager_username,
    c.customer_id,
    c.customer_name
FROM 
    Employee e
JOIN 
    Login l ON e.login_id = l.login_id AND l.role = 'manager'
LEFT JOIN 
    Customer c ON e.branch_id = c.branch_id
WHERE 
    e.bank_id IS NOT NULL;


CREATE VIEW CustomerAcc AS
SELECT account_id, account_type, balance, customer_id  
FROM Account;


ALTER TABLE Employee ADD COLUMN login_id INT;

ALTER TABLE Customer ADD COLUMN branch_id INT;

ALTER TABLE Login ADD COLUMN role varchar(20);

UPDATE Employee 
SET login_id = (SELECT login_id FROM Login WHERE username = 'manager_john')
WHERE employee_name = 'John Doe';

UPDATE Employee 
SET login_id = (SELECT login_id FROM Login WHERE username = 'manager_susan')
WHERE employee_name = 'Susan Smith';


UPDATE Customer 
SET branch_id = (SELECT branch_id FROM Login WHERE username = 'manager_john')
WHERE employee_name = 'John Doe';


SELECT fd_amount, fd_duration, fd_interest_rate, fd_start_date, fd_end_date 
FROM FixedDeposits 
WHERE customer_id = 1 AND status = 'Pending';


CREATE TABLE FixedDeposits (
    fd_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    fd_amount DECIMAL(10, 2),
    fd_duration INT,  -- in months
    fd_interest_rate DECIMAL(5, 2),  -- interest rate as a percentage
    fd_start_date DATE,
    fd_end_date DATE,
    created_by INT,  -- manager_id who created the FD
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (created_by) REFERENCES Login(login_id)  -- assuming login_id is for the manager
);



-- Step 1: Create a new MySQL user for the manager
CREATE USER 'manager_user'@'localhost' IDENTIFIED BY 'manager_password';

-- Step 2: Grant the manager limited permissions
GRANT INSERT, SELECT ON net_banking.FixedDeposits TO 'manager_user'@'localhost';

-- Optionally, if the manager needs to view customer details to create FDs
GRANT SELECT ON net_banking.Customer TO 'manager_user'@'localhost';

-- Step 3: Apply changes
FLUSH PRIVILEGES;


INSERT INTO FixedDeposits (customer_id, fd_amount, fd_duration, fd_interest_rate, fd_start_date, fd_end_date, created_by)
VALUES (1, 15000.00, 24, 4.5, '2024-12-01', '2026-12-01', 6);

INSERT INTO FixedDeposits (customer_id, fd_amount, fd_duration, fd_interest_rate, fd_start_date, fd_end_date, created_by)
VALUES (1, 20000.00, 24, 4.5, '2023-11-11', '2024-11-11', 6);

INSERT INTO FixedDeposits (customer_id, fd_amount, fd_duration, fd_interest_rate, fd_start_date, fd_end_date, created_by, status)
VALUES (1, 25000.00, 24, 3.5, '2024-11-01', '2025-12-01', 6, 'Pending');

INSERT INTO FixedDeposits (customer_id, fd_amount, fd_duration, fd_interest_rate, fd_start_date, fd_end_date, created_by, status)
VALUES (1, 28000.00, 24, 5.5, '2024-11-02', '2026-12-01', 6, 'Pending');

INSERT INTO FixedDeposits (customer_id, fd_amount, fd_duration, fd_interest_rate, fd_start_date, fd_end_date, created_by, status)
VALUES (1, 38000.00, 24, 2.5, '2024-12-02', '2026-12-01', 6, 'Pending');

INSERT INTO FixedDeposits (customer_id, fd_amount, fd_duration, fd_interest_rate, fd_start_date, fd_end_date, created_by, status)
VALUES (1, 48000.00, 24, 5.1, '2025-01-02', '2026-10-01', 6, 'Pending');

INSERT INTO FixedDeposits (customer_id, fd_amount, fd_duration, fd_interest_rate, fd_start_date, fd_end_date, created_by, status)
VALUES (1, 50000.00, 24, 5.9, '2023-02-02', '2024-11-12', 6, 'Pending');

INSERT INTO FixedDeposits (customer_id, fd_amount, fd_duration, fd_interest_rate, fd_start_date, fd_end_date, created_by, status)
VALUES (1, 60000.00, 24, 4.9, '2023-05-03', '2024-11-12', 6, 'Pending');




SHOW GRANTS FOR 'manager_user'@'localhost';

GRANT SELECT ON net_banking.Customer TO 'manager_user'@'localhost';

GRANT ALTER ON net_banking.Customer TO 'manager_user'@'localhost';



ALTER TABLE FixedDeposits 
ADD COLUMN alerted BOOLEAN DEFAULT FALSE;

ALTER TABLE FixedDeposits
     ADD COLUMN status ENUM('Pending', 'Accepted', 'Rejected') DEFAULT 'Pending';


--Add transaction to account id 2, update seen in transaction history, check balance also, procedure

CALL PerformTransaction(
    'transfer',100.00,             
    1,1,2);

--fd related: renew withdraw

INSERT INTO FixedDeposits (customer_id, fd_amount, fd_duration, fd_interest_rate, fd_start_date, fd_end_date, created_by, status)
VALUES (1, 55000.00, 24, 3.5, '2021-05-15', '2024-11-12', 5, 'Pending');

INSERT INTO FixedDeposits (customer_id, fd_amount, fd_duration, fd_interest_rate, fd_start_date, fd_end_date, created_by, status)
VALUES (1, 25000.00, 24, 3.5, '2023-09-02', '2024-11-12', 5, 'Pending');


--add fd from manager

INSERT INTO FixedDeposits (customer_id, fd_amount, fd_duration, fd_interest_rate, fd_start_date, fd_end_date, created_by, status)
VALUES (1, 28000.00, 24, 3.8, '2024-10-02', '2025-12-01', 5, 'Pending');

--get the transactions between 2 dates,procedure

CALL GetTransactionsByDateRange('2024-11-08', '2024-11-10');

--edit beneficiary, procedure

CALL EditBeneficiary(
    '2', 
    'kurt jane','Individual','IFSC12345', 1);

--trigger 

UPDATE Account
SET balance = 50.00
WHERE account_id = 1;






