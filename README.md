# 🏦 Net Banking Database Management System  

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white) ![MySQL](https://img.shields.io/badge/MySQL-Database-orange?logo=mysql&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-Framework-black?logo=flask&logoColor=white) ![HTML](https://img.shields.io/badge/HTML-Frontend-red?logo=html5&logoColor=white) ![CSS](https://img.shields.io/badge/CSS-Styling-blue?logo=css3&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-Version_Control-lightgrey?logo=github)

🚀 A comprehensive **DBMS project** simulating real-world Net Banking operations.  
This project provides secure, efficient, and user-friendly online banking functionalities such as **account management, fund transfers, transaction history, beneficiary management, fixed deposits, and more**.  

<img width="782" height="350" alt="image" src="https://github.com/user-attachments/assets/f7fa368c-ff95-49d4-bc3e-325301abb4e0" />

## 📖 Project Abstract

The Net Banking System ensures seamless digital banking services.
It handles customers, managers, employees, accounts, branches, and banks using a robust relational database.
Security, scalability, and usability are core to the design.

## ✨ Features & Functionalities
**🔐 Login Management**

- Secure login system for customers & managers.
- ccount lock after 3 failed login attempts (unlock after 5 minutes).
- Role-based dashboards.

**👤 Customer Features**

- View account details & balances.
- Deposit, withdraw, and transfer funds.
- View transaction history (with date filters 📅).
- Manage beneficiaries (Add ➕, View 👀, Edit ✏️, Delete ❌).
- Manage Fixed Deposits (FDs) (Accept ✅, Reject ❌, Renew 🔄).

**👨‍💼 Manager Features**

- Dashboard with branch and customer details.
- Create and publish Fixed Deposit schemes.
- Send alerts for upcoming FD deadlines.

**💳 Account & Transaction Management**

- Supports Savings/Current accounts.
- Maintains minimum balance check ✅.
- Tracks deposits, withdrawals, transfers.
- Transaction queries within date ranges.

**🏦 Bank & Branch Management**

- Handles bank details, branches, employees.
- Tracks branch managers and employees.
## 🛠️ Tech Stack

- 🐍 Python (Backend logic)
- 🗄️ MySQL (Database)
- 🌐 HTML, CSS (Frontend)
- ⚙️ Flask (Web Framework)
- 💻 VS Code (IDE)
- 🌱 GitHub (Version Control)
## ER Diagram
<img width="324" height="406" alt="image" src="https://github.com/user-attachments/assets/1013c266-48d8-4ed4-80c1-1a1dae78b1d2" />

## Relational Schema
<img width="370" height="271" alt="image" src="https://github.com/user-attachments/assets/118ae363-d24e-4ccd-8c88-bab7d0a9779d" />

## ⚡ Advanced DB Features
**🔔 Triggers**

- CheckMinimumBalance → Prevents account balance from dropping below threshold.

**🛠️ Stored Procedures**

- PerformTransaction → Deposit, Withdraw, Transfer with validations.
- AddBeneficiary / EditBeneficiary / DeleteBeneficiary → Beneficiary management.
- GetTransactionHistory / GetTransactionsByDateRange → Retrieve past transactions.
- ViewBeneficiaries → Display linked beneficiaries.

**👁️ Views**

- ManagerEmployeeDetails → Manager, employee & customer insights.
- CustomerAccView → Quick account summaries.

**📊 Aggregate Queries**

- Total deposits 💰, withdrawals, transaction summaries.

## 💻 Application Pages  

- 🔐 **Login Page** (Customer / Manager)

<img width="545" height="239" alt="image" src="https://github.com/user-attachments/assets/6305ffd6-97ed-49d6-b495-329b9296ef9f" />

- 🏠 **Customer Dashboard**

<img width="547" height="242" alt="image" src="https://github.com/user-attachments/assets/b0d5095d-784e-4bce-bf4b-c8e4ff521d06" />

- 👨‍💼 **Manager Dashboard**
  
<img width="546" height="239" alt="image" src="https://github.com/user-attachments/assets/db3dab73-9748-4d08-a49e-910f0733efa6" />

- 💳 **Transaction Page** (Deposit / Withdraw / Transfer)

<img width="544" height="233" alt="image" src="https://github.com/user-attachments/assets/201b2617-f027-4696-acd9-a8feed8f215b" />

- 📜 **Transaction History Page** (with date filters)

 <img width="690" height="311" alt="image" src="https://github.com/user-attachments/assets/929281bf-8379-4c52-8c45-6a385a9ce1a2" />

- 👥 **Beneficiary Management** (Add/View/Edit/Delete)

<img width="778" height="339" alt="image" src="https://github.com/user-attachments/assets/1d91fbfc-963a-4c22-95aa-46460fe55fda" />
<img width="521" height="357" alt="image" src="https://github.com/user-attachments/assets/0c2ec373-6316-49f6-9b65-006a1338eb67" />

- 📈 **Fixed Deposit Management** (View/Accept/Reject/Renew)  

<img width="409" height="373" alt="image" src="https://github.com/user-attachments/assets/a39e8485-1497-4742-bd20-7cca6fe4c66f" />

<img width="418" height="296" alt="image" src="https://github.com/user-attachments/assets/0e152c10-030a-480b-9ea2-798ab2b296d9" />


## 👥 Team Details    
- 👩‍💻 *Nithika Balaji* 
- 👩‍💻 *Eshwari L Adiga* 
---

## 📜 License  
This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details. 
