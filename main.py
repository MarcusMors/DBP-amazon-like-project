from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)

data = {
    "name": "",
    "email": "",
    "password": "",
    "birthday": "",
    "date": "",
}


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/login')
def index():
    return render_template("login.html")


@app.route('/register')
def index():
    return render_template("register.html")


@app.route("/profile", methods=["POST"])
def login():
    for key, value in data.items():
        data[key] = request.form.get(key)

    return render_template("index.html", **data)


if __name__ == '__main__':
    app.run(debug=True)
