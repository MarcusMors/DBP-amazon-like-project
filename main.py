# from crypt import methods
import json
import os

# import atexit
# import urllib.request
# from xml.etree.ElementTree import tostring

# from flask import Flask, request, make_response, redirect, render_template, url_for

from flask import (
    Flask,
    request,
    # make_response,
    redirect,
    render_template,
    url_for,
    flash,
)

from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "svg"])

app = Flask(__name__, template_folder="./templates", static_folder="./static")


def Product(filename, title, description, price):
    product = {
        "filename": filename,
        "title": title,
        "description": description,
        "price": price,
    }
    return product


# products = []
car = []
data = {}
users_data = {}

UPLOAD_FOLDER = "static/assets"
USERS_PATH = "./users_data.json"
PRODUCTS_PATH = "./products.json"


app.secret_key = "secret key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

users = {}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def is_logged(user_ip):
    return users.get(user_ip, False) == True


@app.route("/check_credentials", methods=["POST", "GET"])
def check_credentials():
    user_ip = request.remote_addr
    answer = {
        "correct_email": False,
        "correct_password": False,
    }

    if request.method == "POST":
        email = request.form.get("email")
        user_data = users_data[email]
        if email and user_data["email"] == email:
            answer["correct_email"] = True
            if user_data["password"] == request.form.get("password"):
                users[user_ip] = True

        return answer
    return {"id": "your method wasn't post"}


@app.route("/", methods=["POST", "GET"])
def index():
    user_ip = request.remote_addr

    if request.method == "POST":
        email = request.form.get("email")
        # print(f"user_data[hash({email})] : {users_data[hash(email)]}")
        # print(f"users_data : {users_data}")
        # user_data = users_data[hash(email)]
        user_data = users_data[email]
        if email and user_data["email"] == email:
            if user_data["password"] == request.form.get("password"):
                users[user_ip] = True
                context = {"data": user_data, "products": products}
                return render_template(
                    "welcome.html", **context, user=user_data["username"], log=True
                )

            else:
                flash("Incorrect password")
                return redirect(url_for("login"))
        else:
            flash("User not found")
            return redirect(url_for("login"))
    if is_logged(user_ip):  # is logged
        context = {"data": data, "products": products}
        return render_template(
            "welcome.html", **context, user=data["username"], log=True
        )
    return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    user_ip = request.remote_addr
    if is_logged(user_ip):
        return redirect(url_for("profile"))
    if request.method == "POST":

        user_data = {
            "username": "",
            "email": "",
            "password": "",
            "birthday": "",
        }

        for key in user_data:
            user_data[key] = request.form.get(key)

        email = user_data["email"]
        # users_data[hash(email)] = user_data
        users_data[email] = user_data
        # print(f"user_data[hash({email})] : {users_data[hash(email)]}")
        print(f"user_data[{email}] : {users_data[email]}")
        print(f"users_data : {users_data}")
        # context = {"user_data": user_data}
        # print(f"before users_data : {users_data}")
        with open(USERS_PATH, "w") as outfile:
            json.dump(users_data, outfile, indent=4)
        # print(f"after users_data : {users_data}")

        return render_template("login.html")
    return render_template("login.html")


@app.route("/register")
def register():
    user_ip = request.remote_addr
    if is_logged(user_ip):
        return redirect("/home")
    return render_template("register.html")


@app.route("/profile", methods=["POST", "GET"])
def profile():
    user_ip = request.remote_addr
    if not is_logged(user_ip):
        return redirect("/login")
    context = {"data": data}
    if is_logged(user_ip):
        return render_template("profile.html", **context)


@app.route("/register_product")
def register_product():
    user_ip = request.remote_addr
    if not is_logged(user_ip):
        return redirect("/login")
    context = {"data": data}
    return render_template("register_product.html", **context)


@app.route("/home", methods=["POST", "GET"])
def upload_image():
    user_ip = request.remote_addr
    if not is_logged(user_ip):
        return redirect("/login")

    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No image selected for uploading")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            new_product = Product(filename, "", "", "")
            for key, value in new_product.items():
                if key == "filename":
                    continue
                new_product[key] = request.form.get(key)
            # print(new_product)
            products.append(new_product)
            # print(products)
            return redirect("/")
            # return render_template('welcome.html', **context)
        else:
            flash("Allowed image types are -> png, jpg, jpeg, gif")
            return redirect(request.url)
    else:
        # return render_template('welcome.html')
        return redirect("/")


@app.route("/images/<filename>")
def display_image(filename):
    return redirect(url_for("static", filename="assets/" + filename), code=301)


@app.route("/carrito", methods=["POST", "GET"])
def carrito():
    user_ip = request.remote_addr
    if not is_logged(user_ip):
        redirect("/login")
    context = {"data": data, "products": car}
    if is_logged(user_ip):
        return render_template("carrito.html", **context)


@app.route("/carproducts/<filename>", methods=["POST", "GET"])
def carproduct(filename):
    for key in products:
        if key["filename"] == filename:
            print("producto encontrado: ", filename)
            car.append(key)
            print(car)
    return redirect(url_for("index"))


def exit_handler():
    print("CTRL + C interruption")
    print("SAVING VARS INTO FILES")
    with open(PRODUCTS_PATH, "w") as outfile:
        json.dump(products, outfile, indent=4)

    print(f"users_data : {users_data}")
    with open(USERS_PATH, "w") as outfile:
        json.dump(users_data, outfile, indent=4)


if __name__ == "__main__":
    try:
        # load files into local variables
        print("LOCAL VARS LOADED")
        if os.path.isfile(PRODUCTS_PATH):
            products_file = open(PRODUCTS_PATH)
            products = json.load(products_file)
            print(f"products : {products}")
        if os.path.isfile(USERS_PATH):
            users_data_file = open(USERS_PATH)
            users_data = json.load(users_data_file)
            print(f"users_data : {users_data}")

        app.run(debug=True)

        while True:
            pass

    # atexit.register(exit_handler)

    except KeyboardInterrupt:
        # save variables into files
        print("CTRL + C interruption")
        print("SAVING VARS INTO FILES")

        # if(os.path.isfile(PRODUCTS_PATH)):
        # with open(PRODUCTS_PATH, "w") as outfile:
        #     json.dump(products, outfile, indent=4)
        # print(f"products : {products}")

        # # if(os.path.isfile(USERS_PATH)):
        # print(f"before users_data : {users_data}")
        # with open(USERS_PATH, "w") as outfile:
        #     json.dump(users_data, outfile, indent=4)
        # print(f"after users_data : {users_data}")
