#server.py

import os
from flask import Flask, request, jsonify, send_from_directory, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from cryptography.fernet import Fernet

app = Flask(__name__)
bcrypt = Bcrypt(app)
static_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwords.db'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
db = SQLAlchemy(app)

def flask_secret_key():
    secret_key = os.urandom(24)
    with open("flask_secret_key", "wb") as key_file:
        key_file.write(secret_key)

def load_flask_secret_key():
    if not os.path.exists("flask_secret_key"):
        flask_secret_key()
    with open("flask_secret_key", "rb") as key_file:
        secret_key = key_file.read()
    return secret_key

app.secret_key = load_flask_secret_key()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, password):
        self.username = bcrypt.generate_password_hash(username).decode('utf-8')
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_username(self, username):
        return bcrypt.check_password_hash(self.username, username)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

def encryption_key():
    key = Fernet.generate_key()
    with open("encryption_key", "wb") as key_file:
        key_file.write(key)

def load_encryption_key():
    if not os.path.exists("encryption_key"):
        encryption_key()
    with open("encryption_key", "rb") as key_file:
        key = key_file.read()
    return key

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    login = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, login, password, user_id):
        self.name = self.encrypt_data(name)
        self.login = self.encrypt_data(login)
        self.password = self.encrypt_data(password)
        self.user_id = user_id

    def encrypt_data(self, data):
        key = load_encryption_key()
        cipher_suite = Fernet(key)
        ciphered_text = cipher_suite.encrypt(data.encode())
        return ciphered_text.decode()

    def decrypt_data(self, data):
        key = load_encryption_key()
        cipher_suite = Fernet(key)
        unciphered_text = cipher_suite.decrypt(data.encode())
        return unciphered_text.decode()

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return send_from_directory(static_directory, 'index.html')

def check_password(password):
    if len(password) < 8 or len(password) > 80:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    special_characters = "!@#$%^&*()-+?_=,<>/"
    if not any(char in special_characters for char in password):
        return False
    return True

def check_username(username):
    if len(username) < 8 or len(username) > 30:
        return False 
    special_characters = "!@#$%^&*()-+?_=,<>/ÀàÂâÉéÈèÊêËëÎîÏïÔôŒœÙùÛûÜüÇç"
    if any(char in special_characters for char in username):
        return False
    return True

@app.route('/api/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    users = User.query.all()
    user = None

    for u in users:
        if u.check_username(username):
            user = u
            break

    if user: 
        return jsonify({'message': 'Ce nom d\'utilisateur existe déjà. Veuillez en choisir un autre.'}), 400 

    if not check_username(username):
        return jsonify({'message': 'Le nom d\'utilisateur doit comporter entre 8 et 30 caractères et ne doit pas contenir de caractères spéciaux ou de lettre avec accent.'}), 400

    if not password:
        return jsonify({'message': 'Veuillez entrer un mot de passe.'}), 400

    if not check_password(password):
        return jsonify({'message': 'Le mot de passe doit comporter entre 8 et 80 caractères, dont une majuscule, une minuscule, un chiffre et un caractère spécial.'}), 400

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

    users = User.query.all()
    user = None

    for u in users:
        if u.check_username(username):
            user = u
            break

    if user and user.check_username(username) and user.check_password(password):
        session['user_id'] = user.id
        return jsonify({'message': 'Connexion réussie !'})
    else:
        return jsonify({'message': 'Nom d\'utilisateur ou mot de passe incorrect.'}), 401

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Déconnexion réussie !'})

@app.route('/api/save_entry', methods=['POST'])
def save_entry():
    data = request.get_json()
    entry_name = data.get('entryName')
    entry_login = data.get('entryLogin')
    entry_password = data.get('entryPassword')

    if not entry_name or not entry_login or not entry_password:
        return jsonify({'message': 'Les champs Nom, Login et Mot de passe ne doivent pas être vides.'}), 400
    if len(entry_name) > 30 :
        return jsonify({'message': 'Le champ Nom ne doit pas dépasser 30 caractères.'}), 400
    if len(entry_login) > 30 :
        return jsonify({'message': 'Le champ Login ne doit pas dépasser 30 caractères.'}), 400
    if len(entry_password) > 80:
        return jsonify({'message': 'Le champ Mot de passe ne doit pas dépasser 80 caractères.'}), 400

    user_id = session.get('user_id')

    if user_id is None:
        return jsonify({'message': 'Utilisateur non connecté.'}), 401

    try:
        new_entry = Entry(name=entry_name, login=entry_login, password=entry_password, user_id=user_id)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'message': 'Entrée enregistrée avec succès !'})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Erreur lors de l\'enregistrement de l\'entrée. Veuillez réessayer.'}), 500


@app.route('/api/get_entries', methods=['GET'])
def get_entries():
    user_id = session.get('user_id')

    if user_id is None:
        return jsonify({'entries': []})

    entries = Entry.query.filter_by(user_id=user_id).all()
    entries_list = [{'id': entry.id, 'name': entry.decrypt_data(entry.name), 'login': entry.decrypt_data(entry.login), 'password': entry.decrypt_data(entry.password)} for entry in entries]
    return jsonify({'entries': entries_list})

@app.route('/api/delete_entry/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    user_id = session.get('user_id')

    if user_id is None:
        return jsonify({'message': 'Utilisateur non connecté.'}), 401

    entry = Entry.query.filter_by(id=entry_id, user_id=user_id).first()

    if entry:
        try:
            db.session.delete(entry)
            db.session.commit()
            return jsonify({'message': 'Entrée supprimée avec succès !'})
        except IntegrityError:
            db.session.rollback()
            return jsonify({'message': 'Erreur lors de la suppression de l\'entrée. Veuillez réessayer.'}), 500
    else:
        return jsonify({'message': 'Entrée non trouvée ou non autorisée.'}), 404

if __name__ == '__main__':
    app.run(host='192.168.1.97', port=5000, debug=True)
