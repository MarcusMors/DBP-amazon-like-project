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

@app.route('/')
def index():
    user_ip = request.remote_addr
    if is_logged(user_ip):  # is logged
        context = {"data": data}
        return render_template("welcome.html", **context)
    return render_template("login.html")


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

    if request.method == 'POST':
        email =request.form.get("email")
        if email and data["email"] == email:
            if data["password"] == request.form.get("password"):
                users[user_ip] = True
                context = {"data": data}
                return render_template("profile.html", **context)
            else:
                flash("Incorrect password")
                return redirect(url_for("login"))
        else:
            flash("User not found")
            return redirect(url_for("login"))
    if not is_logged(user_ip):  return redirect("/")
    context = {"data": data}
    if is_logged(user_ip):  return render_template("profile.html", **context)



@app.route('/register_product')
def register_product():
    user_ip = request.remote_addr
    if not is_logged(user_ip): redirect("/")

    context = {"data": data}
    return render_template("register_product.html", **context)

@app.route('/home', methods=['POST'])
def upload_image():
    user_ip = request.remote_addr
    if not is_logged(user_ip):
        redirect("/")
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
            #print('upload_image filename: ' + filename)
            flash('Image successfully uploaded and displayed below')
            return render_template('home.html', filename=filename)
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
          return render_template('home.html', filename=filename)



# @app.route('/static/assets/<filename>')
# def display_image(filename):
#     #print('display_image filename: ' + filename)
#     return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    app.run(debug=True)
