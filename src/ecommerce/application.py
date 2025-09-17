from datetime import datetime

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

_db = None


def get_db():
    global _db
    if _db is None:
        _db = SQL("mysql://shopuser:password@10.11.5.5:3306/ecommerce")
    return _db


@app.route("/")
def index():
    db = get_db()
    shirts = db.execute("SELECT * FROM shirts ORDER BY onSalePrice")
    shirts_len = len(shirts)

    shopping_cart = []
    shop_len = len(shopping_cart)
    tot_items, total, display = 0, 0, 0

    if "user" in session:
        shopping_cart = db.execute(
            "SELECT samplename, image, SUM(qty), SUM(subTotal), price, id "
            "FROM cart GROUP BY samplename"
        )
        shop_len = len(shopping_cart)
        for i in range(shop_len):
            total += shopping_cart[i]["SUM(subTotal)"]
            tot_items += shopping_cart[i]["SUM(qty)"]
        shirts = db.execute("SELECT * FROM shirts ORDER BY onSalePrice ASC")
        shirts_len = len(shirts)
        return render_template(
            "index.html",
            shoppingCart=shopping_cart,
            shirts=shirts,
            shopLen=shop_len,
            shirtsLen=shirts_len,
            total=total,
            totItems=tot_items,
            display=display,
            session=session,
        )

    return render_template(
        "index.html",
        shirts=shirts,
        shoppingCart=shopping_cart,
        shirtsLen=shirts_len,
        shopLen=shop_len,
        total=total,
        totItems=tot_items,
        display=display,
    )


@app.route("/buy/")
def buy():
    db = get_db()
    shopping_cart = []
    shop_len = len(shopping_cart)
    tot_items, total, display = 0, 0, 0
    qty = int(request.args.get("quantity", 0))

    if session:
        item_id = int(request.args.get("id"))
        goods = db.execute("SELECT * FROM shirts WHERE id = :id", id=item_id)

        price = goods[0]["onSalePrice"] if goods[0]["onSale"] == 1 else goods[0]["price"]
        samplename = goods[0]["samplename"]
        image = goods[0]["image"]
        sub_total = qty * price

        db.execute(
            "INSERT INTO cart (id, qty, samplename, image, price, subTotal) "
            "VALUES (:id, :qty, :samplename, :image, :price, :subTotal)",
            id=item_id,
            qty=qty,
            samplename=samplename,
            image=image,
            price=price,
            subTotal=sub_total,
        )

        shopping_cart = db.execute(
            "SELECT samplename, image, SUM(qty), SUM(subTotal), price, id "
            "FROM cart GROUP BY samplename"
        )
        shop_len = len(shopping_cart)
        for i in range(shop_len):
            total += shopping_cart[i]["SUM(subTotal)"]
            tot_items += shopping_cart[i]["SUM(qty)"]

        shirts = db.execute("SELECT * FROM shirts ORDER BY samplename ASC")
        shirts_len = len(shirts)
        return render_template(
            "index.html",
            shoppingCart=shopping_cart,
            shirts=shirts,
            shopLen=shop_len,
            shirtsLen=shirts_len,
            total=total,
            totItems=tot_items,
            display=display,
            session=session,
        )


@app.route("/update/")
def update():
    db = get_db()
    shopping_cart = []
    shop_len = len(shopping_cart)
    tot_items, total, display = 0, 0, 0
    qty = int(request.args.get("quantity", 0))

    if session:
        item_id = int(request.args.get("id"))
        db.execute("DELETE FROM cart WHERE id = :id", id=item_id)

        goods = db.execute("SELECT * FROM shirts WHERE id = :id", id=item_id)
        price = goods[0]["onSalePrice"] if goods[0]["onSale"] == 1 else goods[0]["price"]
        samplename = goods[0]["samplename"]
        image = goods[0]["image"]
        sub_total = qty * price

        db.execute(
            "INSERT INTO cart (id, qty, samplename, image, price, subTotal) "
            "VALUES (:id, :qty, :samplename, :image, :price, :subTotal)",
            id=item_id,
            qty=qty,
            samplename=samplename,
            image=image,
            price=price,
            subTotal=sub_total,
        )

        shopping_cart = db.execute(
            "SELECT samplename, image, SUM(qty), SUM(subTotal), price, id "
            "FROM cart GROUP BY samplename"
        )
        shop_len = len(shopping_cart)
        for i in range(shop_len):
            total += shopping_cart[i]["SUM(subTotal)"]
            tot_items += shopping_cart[i]["SUM(qty)"]

        return render_template(
            "cart.html",
            shoppingCart=shopping_cart,
            shopLen=shop_len,
            total=total,
            totItems=tot_items,
            display=display,
            session=session,
        )


@app.route("/filter/")
def filter_route():
    db = get_db()

    shirts = []
    if request.args.get("typeClothes"):
        query = request.args.get("typeClothes")
        shirts = db.execute(
            "SELECT * FROM shirts WHERE typeClothes = :query ORDER BY samplename ASC",
            query=query,
        )
    if request.args.get("sale"):
        query = request.args.get("sale")
        shirts = db.execute(
            "SELECT * FROM shirts WHERE onSale = :query ORDER BY samplename ASC",
            query=query,
        )
    if request.args.get("id"):
        query = int(request.args.get("id"))
        shirts = db.execute(
            "SELECT * FROM shirts WHERE id = :query ORDER BY samplename ASC", query=query
        )
    if request.args.get("kind"):
        query = request.args.get("kind")
        shirts = db.execute(
            "SELECT * FROM shirts WHERE kind = :query ORDER BY samplename ASC",
            query=query,
        )
    if request.args.get("price"):
        shirts = db.execute("SELECT * FROM shirts ORDER BY onSalePrice ASC")

    shirts_len = len(shirts)

    shopping_cart = []
    shop_len = len(shopping_cart)
    tot_items, total, display = 0, 0, 0

    if "user" in session:
        shopping_cart = db.execute(
            "SELECT samplename, image, SUM(qty), SUM(subTotal), price, id "
            "FROM cart GROUP BY samplename"
        )
        shop_len = len(shopping_cart)
        for i in range(shop_len):
            total += shopping_cart[i]["SUM(subTotal)"]
            tot_items += shopping_cart[i]["SUM(qty)"]

        return render_template(
            "index.html",
            shoppingCart=shopping_cart,
            shirts=shirts,
            shopLen=shop_len,
            shirtsLen=shirts_len,
            total=total,
            totItems=tot_items,
            display=display,
            session=session,
        )

    return render_template(
        "index.html",
        shirts=shirts,
        shoppingCart=shopping_cart,
        shirtsLen=shirts_len,
        shopLen=shop_len,
        total=total,
        totItems=tot_items,
        display=display,
    )


@app.route("/checkout/")
def checkout():
    db = get_db()
    order = db.execute("SELECT * from cart")
    for item in order:
        db.execute(
            "INSERT INTO purchases (uid, id, samplename, image, quantity) "
            "VALUES(:uid, :id, :samplename, :image, :quantity)",
            uid=session["uid"],
            id=item["id"],
            samplename=item["samplename"],
            image=item["image"],
            quantity=item["qty"],
        )
    db.execute("DELETE from cart")
    return redirect("/")


@app.route("/remove/", methods=["GET"])
def remove():
    db = get_db()
    out = int(request.args.get("id"))
    db.execute("DELETE from cart WHERE id=:id", id=out)

    tot_items, total, display = 0, 0, 0
    shopping_cart = db.execute(
        "SELECT samplename, image, SUM(qty), SUM(subTotal), price, id "
        "FROM cart GROUP BY samplename"
    )
    shop_len = len(shopping_cart)
    for i in range(shop_len):
        total += shopping_cart[i]["SUM(subTotal)"]
        tot_items += shopping_cart[i]["SUM(qty)"]
    display = 1

    return render_template(
        "cart.html",
        shoppingCart=shopping_cart,
        shopLen=shop_len,
        total=total,
        totItems=tot_items,
        display=display,
        session=session,
    )


@app.route("/login/", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/new/", methods=["GET"])
def new():
    return render_template("new.html")


@app.route("/logged/", methods=["POST"])
def logged():
    db = get_db()
    user = request.form.get("username", "").lower()
    pwd = request.form.get("password", "")

    if user == "" or pwd == "":
        return render_template("login.html")

    rows = db.execute(
        "SELECT * FROM users WHERE username = :user AND password = :pwd",
        user=user,
        pwd=pwd,
    )

    if len(rows) == 1:
        session["user"] = user
        session["time"] = datetime.now()
        session["uid"] = rows[0]["id"]

    if "user" in session:
        return redirect("/")

    return render_template("login.html", msg="Wrong username or password.")


@app.route("/history/")
def history():
    db = get_db()
    shopping_cart = []
    shop_len = len(shopping_cart)
    tot_items, total, display = 0, 0, 0

    my_shirts = db.execute("SELECT * FROM purchases WHERE uid=:uid", uid=session["uid"])
    my_shirts_len = len(my_shirts)

    return render_template(
        "history.html",
        shoppingCart=shopping_cart,
        shopLen=shop_len,
        total=total,
        totItems=tot_items,
        display=display,
        session=session,
        myShirts=my_shirts,
        myShirtsLen=my_shirts_len,
    )


@app.route("/logout/")
def logout():
    db = get_db()
    db.execute("DELETE from cart")
    session.clear()
    return redirect("/")


@app.route("/register/", methods=["POST"])
def registration():
    db = get_db()

    # robust gegen leere POSTs (Integrationstest)
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    confirm = request.form.get("confirm", "")
    fname = request.form.get("fname", "")
    lname = request.form.get("lname", "")
    email = request.form.get("email", "")

    if not username or not password or password != confirm:
        return render_template("login.html")

    rows = db.execute(
        "SELECT * FROM users WHERE username = :username ", username=username
    )
    if len(rows) > 0:
        return render_template("new.html", msg="Username already exists!")

    db.execute(
        "INSERT INTO users (username, password, fname, lname, email) "
        "VALUES (:username, :password, :fname, :lname, :email)",
        username=username,
        password=password,
        fname=fname,
        lname=lname,
        email=email,
    )
    return render_template("login.html")


@app.route("/cart/")
def cart():
    db = get_db()
    shopping_cart = []
    shop_len = 0
    tot_items, total, display = 0, 0, 0

    if "user" in session:
        shopping_cart = db.execute(
            "SELECT samplename, image, SUM(qty), SUM(subTotal), price, id "
            "FROM cart GROUP BY samplename"
        )
        shop_len = len(shopping_cart)
        for i in range(shop_len):
            total += shopping_cart[i]["SUM(subTotal)"]
            tot_items += shopping_cart[i]["SUM(qty)"]

    return render_template(
        "cart.html",
        shoppingCart=shopping_cart,
        shopLen=shop_len,
        total=total,
        totItems=tot_items,
        display=display,
        session=session,
    )
