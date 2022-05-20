#from crypt import methods
import os
import urllib.request
from xml.etree.ElementTree import tostring
# from flask import Flask, request, make_response, redirect, render_template, url_for
from flask import Flask, request, make_response,redirect, render_template, url_for,flash
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg',"svg"])

app = Flask(__name__, template_folder='./templates', static_folder='./static')
# app = Flask(__name__)

# 0. terminar la clase producto
# 1. llenar los productos default de uwuzon (imagen1 a imagen9)
#    el array de productos, debe tener 9 instancias u objetos
# 2. hacer que el form de upload haga append al array productos
# 3. home itera el array de productos
# 4. descansar

# peor de los casos, imagen por typos
# 1. cambiar el upload por un input select
# 2. poner las imagenes de los tipos
# 3. 4 ifs en el home, e iterar los productos

#

# class Product:
#     def __init__(self,filename,title,description,price) -> None:
#         self.filename = filename
#         self.title = title
#         self.description = description
#         self.price = price
#         pass

def Product(filename,title,description,price):
        product={"filename" : filename,
        "title" : title,
        "description" : description,
        "price" : price,}
        return product

products = [
    Product("imagen1.jpg", "Cargador celular laptop", "Conecta tu celular a tu laptop para cargarla", "15 uwu"),
    Product("imagen2.jpg", "Laptop acer nitro gamer", "Disfruta la experiencia acer gamer con tecnología de ultra gama, impermeable", "15.000 uwu"),
    Product("imagen3.jpg", "Cama de perro marca SO", "Engríe a tu mascota con esta cama para perro de 85cm x 135 cm", "325 uwu"),
    Product("imagen4.jpg", "Audifonos inalambricos", "Escucha música sin alambres, sin preocupaciones, escuchalo con Micronics", "95 uwu"),
    Product("imagen5.jpg", "Cámara Lumix", "Captura los mejores momentos de tu vida en alta definición", "4.500 uwu"),
    Product("imagen6.jpg", "Lentes Anyluv olor a menta", "Domina la jerarquía del inconsciente y dá una imagen de intelectual con lentes Anyluv", "99 uwu"),
    Product("imagen7.jpg", "Juego animal crossing", "Relajate en este mundo de fantasía y danos tu dinero mientras pierdes tu vida", "175 uwu"),
    Product("imagen8.jpg", "Smart echo dot speaker/microphone", "Interactúa con el mundo desde la comodidad de tu casa", "875 uwu"),
    Product("imagen9.jpg", "Zapatillas T blancas", "Corre como flash, corre como the big T man", "15 uwu"),

]
car=[]
data = {
    "username": "",
    "email": "",
    "password": "",
    "birthday": "",
}

UPLOAD_FOLDER = 'static/assets'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

users = {
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_logged(user_ip):
    return users.get(user_ip, False) == True

@app.route('/',methods=["POST","GET"])
def index():
    user_ip = request.remote_addr
    if request.method == 'POST':
        email =request.form.get("email")
        if email and data["email"] == email:
            if data["password"] == request.form.get("password"):
                users[user_ip] = True
                context = {"data": data, "products":products}
                return render_template("welcome.html", **context,user=data["username"], log=True)
            else:
                flash("Incorrect password")
                return redirect(url_for("login"))
        else:
            flash("User not found")
            return redirect(url_for("login"))
    if is_logged(user_ip):  # is logged
        context = {"data": data, "products":products}
        return render_template("welcome.html", **context, user=data["username"], log=True)
    return redirect(url_for("login"))


@app.route('/login', methods=["POST","GET"])
def login():
    user_ip = request.remote_addr
    if is_logged(user_ip): return redirect(url_for("profile"))
    if request.method == 'POST':
        for key, value in data.items():
            data[key] = request.form.get(key)
        context = {"data": data}
        return render_template("login.html")
    return render_template("login.html")


@app.route('/register')
def register():
    user_ip = request.remote_addr
    if is_logged(user_ip):  return redirect("/home")
    return render_template("register.html")


@app.route("/profile", methods=["POST","GET"])
def profile():
    user_ip = request.remote_addr
    if not is_logged(user_ip):  return redirect("/login")
    context = {"data": data}
    if is_logged(user_ip):  return render_template("profile.html", **context)



@app.route('/register_product')
def register_product():
    user_ip = request.remote_addr
    if not is_logged(user_ip): return redirect("/login")
    context = {"data": data}
    return render_template("register_product.html", **context)

@app.route('/home', methods=['POST',"GET"])
def upload_image():
    user_ip = request.remote_addr
    if not is_logged(user_ip): return redirect("/login")

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_product = Product(filename,"","","")
            for key, value in new_product.items():
                if key == "filename": continue
                new_product[key] = request.form.get(key)
            # print(new_product)
            products.append(new_product)
            # print(products)
            return redirect('/')
            # return render_template('welcome.html', **context)
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        # return render_template('welcome.html')
        return redirect("/")



@app.route('/images/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='assets/' + filename), code=301)

@app.route('/carrito', methods=['POST','GET'])
def carrito():
    user_ip = request.remote_addr
    if not is_logged(user_ip):
        redirect("/login")
    context = {"data": data, "products":car}
    if is_logged(user_ip):  return render_template("carrito.html", **context)

@app.route('/carproducts/<filename>',methods=['POST','GET'])
def carproduct(filename):
    for key in products:
        if key["filename"] == filename:
            print("producto encontrado: ",filename)
            car.append(key)
            print(car)
    return redirect(url_for("index"))
if __name__ == '__main__':
    app.run(debug=True)

