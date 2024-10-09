# SwiftPay

SwiftPay is a peer-to-peer (P2P) fund transfer application developed using Flask. The application allows users to register, log in, and transfer funds securely between accounts. It also provides features for viewing transaction history and account balance, ensuring a smooth and efficient payment experience.

## Features

- **User Registration**: Users can create an account and set their initial balance.
- **Login Functionality**: Secure login for users to access their accounts.
- **Fund Transfer**: Users can easily transfer funds to other users.
- **Transaction History**: A comprehensive list of all transactions made by the user.
- **Account Balance Viewing**: Users can check their current balance.
- **Sufficient Balance Checks**: Ensures that users cannot transfer more funds than they have available.

## Technologies Used

- **Backend**: Flask
- **Database**: MySQL or SQLite
- **Frontend**: HTML/CSS (optional if using a frontend framework)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/swiftpay.git
   ```

cd swiftpay

python -m venv venv

Activate the virtual environment:
for Windows:
venv\Scripts\activate

For macOS/Linux:
source venv/bin/activate

Install the required packages:
pip install -r requirements.txt

Run the Flask application:
python app.py
