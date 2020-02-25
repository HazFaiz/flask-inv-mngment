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

# ------------------ LIST ALL STORES IN A TABLE FORMAT & DELETE INSTANCE----------
@app.route("/stores")
def index_stores():
    sname = Store.select()
    return render_template('index_stores.html', sname=sname)


@app.route("/stores/<id>/delete", methods=["POST"])
def destroy_store(id):
    # select_store = request.form.get("deletestore")  # this will get id
    store = Store.get_by_id(id)
    store.delete_instance(recursive=True)
    return redirect(url_for("index_stores"))
# ------------------ LIST INFORMATION FOR A PARTICULAR STORE & UPDATE----------


@app.route('/store/<id>', methods=["GET"])
def show_store(id):
    sname = Store.get(id=id)
    return render_template('show_store.html', sname=sname)


@app.route('/store/<id>', methods=["POST"])  # POST REQUEST TO UPDATE NAME
def update_store(id):
    old_name = Store.get(id=id).name
    new_store_name = Store.update(name=request.form.get(
        "name")).where(Store.name == old_name)

    if new_store_name.execute():
        flash(f"Successfully updated")
        # have to pass in id as id, since def show_store(id):
        return redirect(url_for("show_store", id=id))
    else:
        flash("That name is already taken")
        return render_template("show_store.html")
    # ------------------------- FORM FOR ADDING STORE ------------


@app.route("/store", methods=["GET"])
def new_store():
    return render_template('store.html')  # JUST RENDERS STORE>HTML


@app.route("/store/new", methods=["POST"])  # POST REQUEST AND RUN FUNCTION
# WHEN ADDING DATA, UPDATING, OR DELETING DATA, USE POST. GET ONLY FOR READING
def create_store():
    store_name = request.form.get("store_name")
    store = Store(name=store_name)

    if store.save():
        flash(f"Saved store: {store_name}")
        return redirect(url_for("new_store"))
    else:
        flash("That name is already taken")
        return render_template("store.html")

# ----------------------- FORM FOR ADDING WAREHOUSE ----------------
#
# 1.The warehouse creation form needs to have a dropdown of stores to select from
#     The view function that renders the form needs to retrieve all stores
#     We then pass all the stores to the template to be displayed as selection options in the warehouse form

# 2 ext, we can find the store in our create view function before attempting to create a warehouse:
#     store = Store.get_by_id(request.form['store_id'])
#     w = Warehouse(location=request.form['location'], store=store)


# create form for inputting warehouse first

@app.route("/warehouse", methods=["GET"])
def new_warehouse():
    sname = Store.select()
    # JUST RENDERS WAREHOUSE>HTML
    # pass down sname variable that contains all store names to warehouse.html
    return render_template('warehouse.html', sname=sname)


@app.route("/warehouse/new", methods=["POST"])
def create_warehouse():
    storeid = request.form.get("storeid")
    warehouseloc = request.form.get("warehouse_location")
    whouse = Warehouse(location=warehouseloc, store_id=storeid)
    if whouse.save():
        flash(f"Warehouse {warehouseloc} saved at Store {storeid}")
        return redirect(url_for("new_warehouse"))
    else:
        flash("That name is already taken")
        return render_template("warehouse.html")

# ------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)
