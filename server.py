# server.py

import os
from flask import Flask, request, jsonify, send_from_directory, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key'
static_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwords.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return send_from_directory(static_directory, 'index.html')

@app.route('/api/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Ce nom d\'utilisateur existe déjà. Veuillez en choisir un autre.'}), 400

    if not password:
        return jsonify({'message': 'Veuillez entrer un mot de passe.'}), 400

    try:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Compte créé avec succès !'})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Erreur lors de la création du compte. Veuillez réessayer.'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session['user_id'] = user.id  # Stockez l'ID de l'utilisateur dans la session
        return jsonify({'message': 'Connexion réussie !'})
    else:
        return jsonify({'message': 'Nom d\'utilisateur ou mot de passe incorrect.'}), 401

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Déconnectez l'utilisateur en supprimant l'ID de la session
    return jsonify({'message': 'Déconnexion réussie !'})


@app.route('/api/save_entry', methods=['POST'])
def save_entry():
    data = request.get_json()
    entry_name = data.get('entryName')
    entry_login = data.get('entryLogin')
    entry_password = data.get('entryPassword')

    user_id = session.get('user_id')  # Récupérez l'ID de l'utilisateur à partir de la session

    if user_id is None:
        return jsonify({'message': 'Utilisateur non connecté.'}), 401

    new_entry = Entry(name=entry_name, login=entry_login, password=entry_password, user_id=user_id)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({'message': 'Entrée enregistrée avec succès !'})

@app.route('/api/get_entries', methods=['GET'])
def get_entries():
    user_id = session.get('user_id')  # Récupérez l'ID de l'utilisateur à partir de la session

    if user_id is None:
        return jsonify({'entries': []})

    entries = Entry.query.filter_by(user_id=user_id).all()
    entries_list = [{'id': entry.id, 'name': entry.name, 'login': entry.login, 'password': entry.password} for entry in entries]
    return jsonify({'entries': entries_list})

@app.route('/api/delete_entry/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    user_id = session.get('user_id')

    if user_id is None:
        return jsonify({'message': 'Utilisateur non connecté.'}), 401

    entry = Entry.query.filter_by(id=entry_id, user_id=user_id).first()

    if entry:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({'message': 'Entrée supprimée avec succès !'})
    else:
        return jsonify({'message': 'Entrée non trouvée ou non autorisée.'}), 404

if __name__ == '__main__':
    app.run(host='192.168.1.97', port=5000, debug=True)
