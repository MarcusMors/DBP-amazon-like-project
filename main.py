#from crypt import methods
from xml.etree.ElementTree import tostring
from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)

data = {
    "username": "",
    "email": "",
    "password": "",
    "birthday": "",
}


users = {
}


@app.route('/')
def index():
    user_ip = request.remote_addr
    if(users.get(user_ip, False) == True):  # is logged
        context = {"data": data}
        return render_template("welcome.html", **context)
    return render_template("login.html")


@app.route('/login')
def login():
    user_ip = request.remote_addr
    if(users.get(user_ip, False) == True):  # is logged
        # response = make_response(redirect("/profile"), data)
        response = make_response(redirect("/profile"))
        return response
    return render_template("login.html")


@app.route('/register')
def register():
    user_ip = request.remote_addr
    if(users.get(user_ip, False) == True):  # is logged
        # response = make_response(redirect("/profile"), data)
        response = make_response(redirect("/profile"))
        return response
    return render_template("register.html")


@app.route("/profile", methods=["POST"])
def profile():
    if request.method != 'POST':
        user_ip = request.remote_addr
        if(users.get(user_ip, False) == True):  # is logged
            # response = make_response(redirect("/profile"), data)
            return render_template("profile.html", **context)
    user_ip = request.remote_addr
    users[user_ip] = True
    for key, value in data.items():
        data[key] = request.form.get(key)

    context = {"data": data}

    return render_template("profile.html", **context)


if __name__ == '__main__':
    app.run(debug=True)
