from flask import Flask, render_template, url_for, request
from datetime import datetime
from BlogPost import BlogPost

app = Flask(__name__)

blogs = [
    BlogPost(1,'Red flowers', 'text about red flowers','User1',datetime.now(),),
    BlogPost(2,'Yellow flowers', 'text about yellow flowers','User2',datetime.now(),),
    BlogPost(3,'Blue flowers', 'text about blue flowers','User3',datetime.now(),)
         ]

def add_post(form):
    post=BlogPost(len(blogs)+1,form.get('title'),form.get('contents'),form.get('owner'), datetime.now())
    blogs.insert(0,post)
    return render_template('index.html', blogs=blogs)

@app.route('/', methods=['GET','POST'])
def post_blog(blogs=blogs):
    if request.method == 'GET':
        return render_template('index.html', blogs=blogs)
    else:
        return add_post(request.form)

@app.route('/index')
def index(blogs=blogs):
    # Render the page
    return render_template('index.html', blogs=blogs)

if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449)
