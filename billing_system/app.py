from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///billing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))

# Invoice model
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)

# Home route
@app.route('/')
def index():
    customers = Customer.query.all()
    invoices = Invoice.query.all()
    return render_template('index.html', customers=customers, invoices=invoices)

# Add Customer route
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_customer = Customer(name=name, email=email)
        db.session.add(new_customer)
        db.session.commit()
        return redirect('/')
    
    return render_template('add_customer.html')

# Create Invoice route
@app.route('/create_invoice', methods=['GET', 'POST'])
def create_invoice():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        amount = request.form['amount']
        new_invoice = Invoice(customer_id=customer_id, amount=amount)
        db.session.add(new_invoice)
        db.session.commit()
        return redirect('/')
    
    customers = Customer.query.all()
    return render_template('create_invoice.html', customers=customers)

# Invoice View route
@app.route('/invoice/<int:invoice_id>')
def invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    customer = Customer.query.get(invoice.customer_id)
    return render_template('invoice.html', invoice=invoice, customer=customer)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database and tables
    app.run(debug=True)
