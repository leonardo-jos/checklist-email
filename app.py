from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///suppliers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Supplier model
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)
    order_sent = db.Column(db.Boolean, default=False)
    order_received = db.Column(db.Boolean, default=False)
    order_confirmed = db.Column(db.Boolean, default=False)

# Initialize the database
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating database: {e}")

@app.route("/")
def index():
    suppliers = Supplier.query.all()
    return render_template("index.html", suppliers=suppliers)

@app.route("/update_supplier/<int:supplier_id>", methods=["POST"])
def update_supplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if supplier:
        supplier.order_sent = request.json.get('order_sent', supplier.order_sent)
        supplier.order_received = request.json.get('order_received', supplier.order_received)
        supplier.order_confirmed = request.json.get('order_confirmed', supplier.order_confirmed)
        db.session.commit()
    return jsonify({"status": "success"})

@app.route("/toggle_supplier/<int:supplier_id>", methods=["POST"])
def toggle_supplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if supplier:
        supplier.active = not supplier.active
        db.session.commit()
    return jsonify({"status": "success"})

@app.route("/add_supplier", methods=["POST"])
def add_supplier():
    name = request.form.get("name")
    if name:
        new_supplier = Supplier(name=name)
        db.session.add(new_supplier)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/suppliers")
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([{
        "id": s.id,
        "name": s.name,
        "active": s.active,
        "order_sent": s.order_sent,
        "order_received": s.order_received,
        "order_confirmed": s.order_confirmed
    } for s in suppliers])

if __name__ == "__main__":
    app.run(debug=True)
