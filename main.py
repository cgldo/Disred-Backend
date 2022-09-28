from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine
from flask_cors import CORS
import os
from dotenv import dotenv_values
import psycopg2

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

config = dotenv_values(".env")

app.config['SQLALCHEMY_DATABASE_URI'] = config['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

# Initialize DB
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Model
class PostModel(db.Model):
    __tablename__ = 'post_table'
 
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String())
    author =  db.Column(db.String())
    body = db.Column(db.String())
    imgUrl = db.Column(db.String())
    tags = db.Column(db.String())
    
    def __init__(self, title, author, body, imgUrl, tags):
        self.title = title
        self.author = author
        self.body = body
        self.imgUrl = imgUrl
        self.tags = tags
        
class CommentModel(db.Model):
    __tablename__ = 'comment_table'
    id = db.Column(db.Integer, primary_key = True)
    author =  db.Column(db.String())
    body = db.Column(db.String())
    tags = db.Column(db.String())
    post_id = db.Column(db.ForeignKey(PostModel.id))
 

# Schema
class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author', 'body', 'imgUrl', 'tags')
        
class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'author', 'body', 'tags', 'post_id')

# Initialize Schema
post_schema = PostSchema()
posts_schema = PostSchema(many=True)
comment_schema = CommentSchema()

# Create/add new
@app.route('/post', methods=['POST'])
def add_post():
    title = request.json['title']
    author = request.json['author']
    body = request.json['body']
    imgUrl = request.json['imgUrl']
    tags = request.json['tags']
    

    new_post = PostModel(title, author, body, imgUrl, tags)
    db.session.add(new_post)
    db.session.commit()

    return post_schema.jsonify(new_post)

@app.route('/postall', methods=['POST'])
def add_allpost():
    all_post = []
    for post in request.json:
        title = post.title
        author = post.author
        body = post.body
        imgUrl = post.imgUrl
        tags = post.tags
        new_post = PostModel(title, author, body, imgUrl, tags)
        db.session.add(new_post)
        all_post.append(new_post)

    db.session.commit()
    return posts_schema.dump(all_post)

# Get all
@app.route('/post', methods=['GET'])
def get_all_products():
    all_post = PostModel.query.all()
    result = posts_schema.dump(all_post)
    return jsonify(result)

# Get one
@app.route('/post/<id>', methods=['GET'])
def get_post(id):
    post = PostModel.query.get(id)
    
    return post_schema.jsonify(post)

# Update existing item
@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    post = PostModel.query.get(id)

    post.title = request.json['title']
    post.author = request.json['author']
    post.body = request.json['body']
    post.imgUrl = request.json['imgUrl']
    post.tags = request.json['tags']

    db.session.commit()

    return post_schema.jsonify(post)

# Delete one
@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    post = PostModel.query.get(id)
    if post != None:
        # Successfully found the item we want to delete
        db.session.delete(post)
        db.session.commit()
        return post_schema.jsonify(post)
    else:
        # Can't find the item we want to delete
        return post_schema.jsonify({})

# Base route
@app.route('/', methods=['GET'])
def get():
    return jsonify({"hey":"hi"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0",port=5000)
    #app.run(debug=True) #can alter host and port number here. Right now the default host is localhost and port is 5000