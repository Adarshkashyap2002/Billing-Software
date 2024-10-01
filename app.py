from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///billing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Models for the database
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)

# Route to display all customers and invoices
@app.route('/')
def index():
    customers = Customer.query.all()
    invoices = Invoice.query.all()
    return render_template('index.html', customers=customers, invoices=invoices)

# Route to add a new customer
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_customer = Customer(name=name, email=email)
        
        try:
            db.session.add(new_customer)
            db.session.commit()
            flash('Customer added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error: {str(e)} - Customer could not be added.', 'error')
            return redirect(url_for('add_customer'))
    
    return render_template('add_customer.html')

# Route to create a new invoice
@app.route('/create_invoice', methods=['GET', 'POST'])
def create_invoice():
    customers = Customer.query.all()
    
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        amount = request.form['amount']
        new_invoice = Invoice(customer_id=customer_id, amount=amount)
        
        try:
            db.session.add(new_invoice)
            db.session.commit()
            flash('Invoice created successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error: {str(e)} - Invoice could not be created.', 'error')
            return redirect(url_for('create_invoice'))
    
    return render_template('create_invoice.html', customers=customers)

# Initialize the database when the app is run
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
