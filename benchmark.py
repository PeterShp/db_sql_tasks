from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
)
from passlib.hash import pbkdf2_sha256
from datetime import timedelta

app = Flask(__name__)

# Підключення до БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@34.141.145.160:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)

jwt_blocklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in jwt_blocklist

# Додаємо індекси до колонок, які часто використовуються для вибірок/фільтрації:

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True, index=True)  # індекс на name

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True, index=True)  # індекс на name
    books = relationship("Book", back_populates="author", cascade="all, delete")

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, index=True)  # індекс на title
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)
    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", lazy="joined")

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False, index=True)  # індекс на username
    password = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        hashed_pw = pbkdf2_sha256.hash('admin')
        admin_user = User(username='admin', password=hashed_pw)
        db.session.add(admin_user)
        db.session.commit()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and pbkdf2_sha256.verify(password, user.password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(msg="Bad username or password"), 401

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_blocklist.add(jti)
    return jsonify(msg="Successfully logged out"), 200

@app.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    title = data.get('title')
    author_name = data.get('author_name')
    genre_name = data.get('genre_name')

    if not (title and author_name and genre_name):
        return jsonify(msg="Missing required fields"), 400

    author = Author.query.filter_by(name=author_name).first()
    if not author:
        author = Author(name=author_name)
        db.session.add(author)
        db.session.commit()

    genre = Genre.query.filter_by(name=genre_name).first()
    if not genre:
        genre = Genre(name=genre_name)
        db.session.add(genre)
        db.session.commit()

    book = Book(title=title, author=author, genre=genre)
    db.session.add(book)
    db.session.commit()
    return jsonify(msg="Book added", book_id=book.id), 201

@app.route('/books', methods=['GET'])
@jwt_required()
def get_books():    
    books = Book.query.all()
    result = [{
        "id": b.id,
        "title": b.title,
        "author": b.author.name,
        "genre": b.genre.name
    } for b in books]
    return jsonify(books=result), 200

@app.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    data = request.get_json()
    title = data.get('title')
    book = Book.query.get(book_id)
    if not book:
        return jsonify(msg="Book not found"), 404

    if title:
        book.title = title
        db.session.commit()
    return jsonify(msg="Book updated"), 200

@app.route('/books/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify(msg="Book not found"), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify(msg="Book deleted"), 200

@app.route('/reset', methods=['DELETE'])
def reset():
    db.drop_all()
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        hashed_pw = pbkdf2_sha256.hash('admin')
        admin_user = User(username='admin', password=hashed_pw)
        db.session.add(admin_user)
        db.session.commit()
    return jsonify(msg="Database reset done"), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
