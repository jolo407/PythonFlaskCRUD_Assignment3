"""HTTP route definition"""

import functools
from flask import (
    Blueprint, flash, g, Flask, redirect, render_template, request, session, url_for
)
from app import app
from app.database import create, read, update, delete, scan, get_db
from datetime import datetime
from app.forms.product import ProductForm
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/')
def home():
    return render_template('auth/login.html')

#@app.route("/")
#def index():
    #serv_time = datetime.now().strftime("%F %H:%M:%S")
    #return{
        #"ok": True,
        #"version": "1.0.0",
        #"server_time": serv_time
    #}
    
    
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

@app.route("/products/delete/<pid>", methods=["GET", "POST"])
def delete_product(pid):
    if request.method == "POST":
        scan(pid, request.form)
    out = read(int(pid)) 
    if out["body"]:
        return render_template("delete.html", product=out["body"][0])
        

#@app.route('/login/', methods=("GET", "POST"))
#def login():
  #  if request.method == "POST":
  #      username = request.form['username']
   #     password = request.form['password']
    #    db = get_db()
     #   error = None
      #  user = db.execute(
       #     'SELECT * FROM user WHERE username = ?', (username,)
        #).fetchone()

        #if user is None:
         #   error = 'Incorrect username.'
        #elif not check_password_hash(user['password'], password):
         #   error = 'Incorrect password.'

        #if error is None:
         #   session.clear()
          #  session['user_id'] = user['id']
           # return redirect(url_for('review.dashboard'))

        #flash(error)

    #return render_template('auth/login.html')

#@app.route('/register', methods=("GET", "POST"))
#def register():
    #if request.method == "POST":
       # username = request.form['username']
        #password = request.form['password']
       # db = get_db()
       # error = None

      #  if not username:
       #     error = 'Username is required.'
      #  elif not password: 
       #     error = 'Password is required.'
       # elif db.execute(
      #      'SELECT id FROM user WHERE username = ?', (username,)
       # ).fetchone() is not None:
       #     error = 'User {} is already registered.'.format(username)

       # if error is None:
       #     db.execute(
       #         'INSERT INTO user (username, password) VALUES (?, ?)',
       #         (username, generate_password_hash(password))
       #     )
       #     db.commit()
        #    return redirect(url_for('auth.login/'))

       # flash(error)

   ## return render_template('auth/register.html')

@app.route('/logout')
def logout():
    session.clear()
    return ("You have been logged out")



def login_required(view):
    @fuctools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@app.route('/reviews/<int:pid>', methods=("GET", "POST"))
def reviews(pid):
    if request.method == "POST":
        update(pid, request.form)
        return {"ok": "True", "message": "Updated"}
    out = read(int(pid))
    if out["body"]:
         return render_template("review/create.html", product=out["body"][0])
    else:
        return render_template("404.html"), 404


       
    

@app.route('/reviews', methods=("GET", "POST"))
def view_reviews():
    return render_template('review/reviews.html')



        

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404














if __name__ == '__main__':
    app.run(debug=True)