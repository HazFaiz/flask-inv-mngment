import peeweedbevolve
from flask import Flask, render_template, request, flash, redirect, url_for
from models import db, Store, Warehouse, Product  # new line
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.before_request  # new line
def before_request():
    db.connect()


@app.after_request  # new line
def after_request(response):
    db.close()
    return response


@app.cli.command()  # new
def migrate():  # new
    db.evolve(ignore_tables={'base_model'})  # new


@app.route("/")
def index():
    return render_template('index.html')

# Forms


@app.route("/store", methods=["GET"])
def show_store():
    return render_template('store.html')


@app.route("/store/new", methods=["POST"])
def create():
    store_name = request.form.get("store_name")
    store = Store(name=store_name)

    if store.save():
        flash(f"Saved store: {store_name}")
        return redirect(url_for("show_store"))
    else:
        flash("That name is already taken")
        return render_template("store.html")


if __name__ == '__main__':
    app.run(debug=True)
