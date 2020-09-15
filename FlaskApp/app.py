from flask import Flask, render_template, url_for
from BlogPost import BlogPost

app = Flask(__name__)

blogs = [
    BlogPost(1,'Red flowers', 'text about red flowers','User1','today',),
    BlogPost(2,'Yellow flowers', 'text about yellow flowers','User2','yesterday',),
    BlogPost(3,'Blue flowers', 'text about blue flowers','User3','5 minutes ago',)
         ]

@app.route('/')
@app.route('/index')
def index(blogs=blogs):
    # Render the page
    return render_template('index.html', blogs=blogs)

if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449)
