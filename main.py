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
def login():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route("/profile", methods=["POST"])
def profile():
    for key, value in data.items():
        data[key] = request.form.get(key)

    context = {"data": data}

    return render_template("profile.html", **context)


if __name__ == '__main__':
    app.run(debug=True)
