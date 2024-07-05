# Banking Application API
This project implements a RESTful API for a banking application using Flask, MySQL, and SQLAlchemy. It provides endpoints for user management, account management, transaction management, and basic financial functionalities.

## Features Implemented
1. RESTful API Endpoints:
- User Management
- Account Management
- Transaction Management
- Budget Management
- Bill Management

2. Database Models:
- User: Represents user accounts.
- Account: Represents user accounts with account type, balance, etc.
- Transaction: Represents financial transactions with details like amount, type, etc.
- Budget: Represents budget categories for expense tracking.
- Bill: Represents scheduled bill payments.

3. Authentication:
Session-based authentication using Flask-Login.

## Setup and Installation
1. Clone the Repository:
- git clone https://github.com/your/repository.git
- cd repository
2. Install Dependencies:
- pip install -r requirements.txt
3. Set Up Environment Variables:
- ##### Create a .env file in the root directory with the following configuration:
dotenv
##### DATABASE_URI=mysql+pymysql://username:password@localhost/dbname
##### SECRET_KEY=your_secret_key
##### Replace username, password, localhost, and dbname with your actual database credentials.

- Run the Application:
flask run

## API Endpoints
![postman](<assets/All postman.png>)
1. User Management
POST /auth/register: Create a new user account.
![create user](assets/createuser.png)

- Get Account Profile
![get acount profile](assets/getuserprofile.png)

- Update User
![updateuser](assets/updateuser.png)

- POST /auth/login: Authenticate user and generate session token.
![login](assets/loginuser.png)

- POST /auth/logout: Logout the currently authenticated user.
![logout](assets/logout.png)

2. Account Management
- GET /accounts: Retrieve all accounts.
![1](assets/gatallaccount.png)

- GET /accounts/:id: Retrieve details of a specific account.
![2](assets/gataccountbyid.png)

- POST /accounts: Create a new account.
![3](assets/createaccount.png)

- PUT /accounts/:id: Update details of an existing account.
![4](assets/updateaccount.png)

- DELETE /accounts/:id: Delete an account.
![5](assets/deleteaccount.png)

3. Transaction Management
- GET /transactions: Retrieve all transactions.
![1](assets/gettransaction.png)

- GET /transactions/:id: Retrieve details of a specific transaction.
![2](assets/gettransactionbyid.png)

- POST /transactions: Create a new transaction (deposit, withdrawal, transfer).
![createtrx](assets/createtransaction.png)

4. Budget Management
- POST /budgets: Create a new budget category.
![1](assets/createbudget.png)

- GET /budgets: Retrieve all budget categories.
![2](assets/getbudget.png)

- PUT /budgets/:id: Update an existing budget category.
![3](assets/UpdateBudget.png)

5. Bill Management
- POST /bills: Schedule a bill payment.
![1](assets/createbill.png)

- GET /bills: Retrieve all scheduled bill payments.
![2](<assets/get user'sbill.png>)

- PUT /bills/:id: Update details of a scheduled bill payment.
![3](assets/updatebill.png)

- DELETE /bills/:id: Cancel a scheduled bill payment.
![4](assets/deletebill.png)

## Error Handling
Proper error handling and validation are implemented for each endpoint to handle potential errors and provide meaningful error messages.