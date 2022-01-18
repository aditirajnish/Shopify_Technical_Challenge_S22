
from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from io import StringIO, BytesIO
from datetime import datetime
import csv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"  # relative path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Create model for Products with the following attributes.
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100), nullable=False)  # don't want it to be blank
    inventory_level = db.Column(db.Integer, default=0)
    description = db.Column(db.String(200))

# Creates the SQLite database (db).
@app.before_first_request
def create_table():
    db.create_all()


@app.route("/", methods=["POST", "GET"])
def index():
    columns = [column.name for column in Products.__mapper__.columns if column.name != "id"]

    # If new product is created, add it to the db.
    if request.method == "POST":
        new_task = Products(**request.form)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue creating your product"

    # View a list of the products.
    else:
        products = Products.query.all()
        return render_template("index.html", products=products, columns=columns)


@app.route("/delete/<int:id>")
def delete(id):
    # Delete product with given id value from the db.
    product_to_delete = Products.query.get_or_404(id)
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was an issue deleting that product"


@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    columns = [column.name for column in Products.__mapper__.columns if column.name != "id"]
    product_to_update = Products.query.get_or_404(id)

    # Updates the product info, then redirect to view list of products.
    if request.method == "POST":
        for column in columns:
            setattr(product_to_update, column, request.form[column])
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating that product"

    # Display form where user can update product fields.
    else:
        return render_template("update.html", product=product_to_update, columns=columns)


@app.route("/export")
def export():
    # Exports product data to a CSV for user download.
    # Creates CSV in memory via StringIO and converts buffer into a file-like object via BytesIO.
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)

    first_row = [column.name for column in Products.__mapper__.columns]
    writer.writerow(first_row)

    for record in Products.query.all():
        row = []
        for column in Products.__mapper__.columns:
            row.append(getattr(record, column.name))
        writer.writerow(row)

    csv_obj = BytesIO()
    csv_obj.write(csv_buffer.getvalue().encode())
    csv_obj.seek(0)

    return send_file(
        path_or_file=csv_obj,
        as_attachment=True,
        download_name=f"product_data_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
