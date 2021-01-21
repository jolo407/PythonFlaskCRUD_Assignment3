"""HTTP route definition"""

from flask import request, render_template
from app import app
from app.database import create, read, update, delete, scan
from datetime import datetime
from app.forms.product import ProductForm

@app.route("/")
def index():
    serv_time = datetime.now().strftime("%F %H:%M:%S")
    return{
        "ok": True,
        "version": "1.0.0",
        "server_time": serv_time
    }

@app.route("/product_form", methods=["GET", "POST"])
def product_form():
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")
        category = request.form.get("category")
        quantity = request.form.get("quantity")
        unique_tag = request.form.get("unique_tag")
        create(name, price, description, category, quantity, unique_tag)
    form = ProductForm()
    return render_template("form_example.html", form=form) 


@app.route("/products")
def get_all_products():
    out = scan()
    #out["ok"] = True
    #out["message"] = "Success"
    #return out
    return render_template("products.html", products=out["body"])

#@app.route("/products/<pid>")
#def get_one_product(pid):
    #out = read(int(pid))
   # out["ok"] = True
    #out["message"] = "Success"
   # return out

@app.route("/products", methods=["POST"])
def create_products():
    products_data = request.json
    new_id = create(
        products_data.get("name"),
        products_data.get("price"),
        products_data.get("description"),
        products_data.get("category"),
        products_data.get("quantity"),
        products_data.get("unique_tag")
    )

    return {"ok": True, "message": "Success", "new_id": new_id}

@app.route("/products/<pid>", methods=["GET", "PUT"])
def update_product(pid):
    #product_data = request.json
    if request.method == "PUT":
        update(pid, request.form)
        return {"ok": "True", "message": "Updated"}
    out = read(int(pid))
    update_form = ProductForm()
    if out["body"]:
        return render_template("single_product.html", product=out["body"][0], form=update_form)
    else:
        return render_template("404.html"), 404

@app.route("/products/delete/<pid>", methods=["GET"])
def delete_product(pid):
    out = update(int(pid), {"active": 0})
    return {"ok": out, "message": "Updated"}
    
    return render_template("delete.html", product=out["body"][0])
    



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

