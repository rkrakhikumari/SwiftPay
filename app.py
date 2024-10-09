from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session



app = Flask(__name__)
app.secret_key = 'your_secret_key'

# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///p2p_fund_transfer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Define relationships
    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])


# Create the database and tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        initial_balance = float(request.form['balance'])

        new_user = User(username=username, password=password, balance=initial_balance)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')  # Flash message on successful registration
        return redirect(url_for('login'))

    return render_template('register.html')


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()

        if user is None:
            flash('Not registered! Please register yourself first.', 'error')  # Flash message if user does not exist
            return redirect(url_for('login'))

        if check_password_hash(user.password, password):
            session['username'] = user.username
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


# User dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    return render_template('dashboard.html', username=user.username, balance=user.balance)

# Fund transfer
@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == 'POST':
        receiver_username = request.form['receiver']
        amount = float(request.form['amount'])

        sender_id = session['user_id']
        sender = User.query.get(sender_id)
        receiver = User.query.filter_by(username=receiver_username).first()

        if receiver is None:
            flash('Receiver does not exist!', 'error')
            return redirect(url_for('transfer'))

        if sender.balance < amount:
            flash('Insufficient balance!', 'error')
            return redirect(url_for('transfer'))

        # Update balances
        sender.balance -= amount
        receiver.balance += amount

        # Create a new transaction
        new_transaction = Transaction(sender_id=sender_id, receiver_id=receiver.id, amount=amount)
        db.session.add(new_transaction)
        db.session.commit()

        # Flash success message and redirect back to the same transfer page
        flash('Transaction successful!', 'success')
        return redirect(url_for('transfer'))

    return render_template('transfer.html')


@app.route('/history')
def history():
    user_id = session['user_id']
    transactions = []

    # Fetch sent transactions
    sent_transactions = Transaction.query.filter_by(sender_id=user_id).all()
    for transaction in sent_transactions:
        # Get receiver's username for better readability
        receiver_username = User.query.get(transaction.receiver_id).username
        transactions.append({
            'transaction_type': 'Sent',
            'user': receiver_username,  # Display receiver's username
            'amount': transaction.amount,
            'date': transaction.transaction_date.strftime('%Y-%m-%d %H:%M:%S')  # Format date
        })

    # Fetch received transactions
    received_transactions = Transaction.query.filter_by(receiver_id=user_id).all()
    for transaction in received_transactions:
        sender_username = User.query.get(transaction.sender_id).username
        transactions.append({
            'transaction_type': 'Received',
            'user': sender_username,  # Display sender's username
            'amount': transaction.amount,
            'date': transaction.transaction_date.strftime('%Y-%m-%d %H:%M:%S')  # Format date
        })

    return render_template('history.html', all_transactions=transactions)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
