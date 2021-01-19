from flask import Flask, render_template,request,redirect,url_for,session,send_from_directory

app = Flask(__name__)


@app.route("/")
def load_home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
