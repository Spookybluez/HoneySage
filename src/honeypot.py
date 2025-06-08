from flask import Flask, request, render_template
from logger import log_attempt

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        ip = request.remote_addr
        log_attempt(ip, username, password)
        message = "Invalid credentials"
    return render_template("login.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
