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
    return render_template("index.html")


@app.route("/profile", methods=["POST"])
def login():
    for [key]
    form_name = request.form.get("name")
    data["name"] = request.form.get("name")

    return render_template("index.html", **context)


if __name__ == '__main__':
    app.run(debug=True)
