from flask import Flask, render_template, url_for

app = Flask(__name__)

blogs = []

@app.route('/')
@app.route('/index')
def hello(name = None):
    # Render the page
    return render_template('index.html', name = name)

if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449)
