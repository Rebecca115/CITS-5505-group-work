from flask import Flask, render_template, request,redirect

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():

    pass


if __name__ == '__main__':
    app.run(debug=True)