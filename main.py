from flask import Flask, request, render_template

from facebook_post_bot import FacebookPostBot

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/start', methods=['POST'])
def start():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        groups = request.form['groups']
        message = request.form['message']
        retry_attempts = 5
        groups = groups.split(",")
        groups = [g.strip() for g in groups]
        bot = FacebookPostBot("chromedriver.exe", email, password, groups)
        bot.start_bot(change_identity=True,
                      message=message,
                      retry_attempts=retry_attempts)
        return render_template("home.html")


if __name__ == '__main__':
    app.run()
