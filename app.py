from backend_main import *

from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

my_pet = start_backend_main()


@app.route("/")
def home():
    return render_template("home_page.html")


@app.route("/status")
def status():
    data = my_pet.status
    return render_template("status_page.html", data=data)


@app.route("/action")
def action():
    if request.method == "POST":
        choice = request.form.get("choice")
        print(choice)
    return render_template("action_page.html")


@app.post("/action/eat")
def post_eat():
    output = my_pet.eat()
    return render_template("action_page.html", output=output)


@app.post("/action/sleep")
def post_sleep():
    output = my_pet.sleep()
    return render_template("action_page.html", output=output)


@app.post("/action/play")
def post_play():
    output = my_pet.play()
    return render_template("action_page.html", output=output)


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
