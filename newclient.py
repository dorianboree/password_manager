import tkinter as tk
from tkinter import messagebox, font, filedialog
import requests
import pyperclip
import webbrowser
import csv
import random
import string

session = requests.Session()

def open_webpage(event):
    webbrowser.open('https://monsite.local/')

def check_password(password):
    if len(password) < 8:
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

def generate_password(length=12, use_digits=True, use_uppercase=True, use_lowercase=True, use_special=True):
    characters = ''
    if use_digits:
        characters += string.digits
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_special:
        characters += "!@#$%^&*()-+?_=,<>/"
    
    if not characters:
        return ''
    
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def fill_generated_password_with_length(entry, length_entry):
    try:
        length = int(length_entry.get())
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre entier pour la longueur du mot de passe.")
        return
    
    if length <= 0:
        messagebox.showerror("Erreur", "La longueur du mot de passe doit être supérieure à zéro.")
        return
    
    use_digits = var_digits.get()
    use_uppercase = var_uppercase.get()
    use_lowercase = var_lowercase.get()
    use_special = var_special.get()
    generated_password = generate_password(length=length, use_digits=use_digits, use_uppercase=use_uppercase, use_lowercase=use_lowercase, use_special=use_special)
    entry.delete(0, tk.END)
    entry.insert(0, generated_password)

def create_account(username, password):
    if len(username) < 8:
        messagebox.showerror("Erreur", "Le nom d'utilisateur doit contenir au moins 8 caractères.")
        return
    if not check_password(password):
        messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 8 caractères, dont une majuscule, une minuscule, un chiffre et un caractère spécial.")
        return

    server_url = "https://monsite.local/api/create_account"
    
    data = {'username': username, 'password': password} 
    
    try:
        response = session.post(server_url, json=data, verify=False)
        
        if response.status_code == 200:
            messagebox.showinfo("Succès", "Compte créé avec succès !") 
        elif response.status_code == 400:
            error_message = response.json().get('message', 'Erreur de création de compte.')
            messagebox.showerror("Erreur", error_message)
        else:
            messagebox.showerror("Erreur", "Échec de la création de compte !") 
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de création de compte : {str(e)}") 

def create_account_button_clicked():
    create_account(username_entry.get(), password_entry.get())

def login(username, password):
    if len(username) < 8:
        messagebox.showerror("Erreur", "Le nom d'utilisateur doit contenir au moins 8 caractères.")
        return
    if not check_password(password):
        messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 8 caractères, dont une majuscule, une minuscule, un chiffre et un caractère spécial.")
        return
    
    server_url = "https://monsite.local/api/login" 
    
    data = {'username': username, 'password': password} 
    
    try:
        response = session.post(server_url, json=data, verify=False)
        
        if response.status_code == 200: 
            show_dashboard()
            show_entries() 
        else:
            messagebox.showerror("Erreur", "Échec de la connexion !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de connexion : {str(e)}") 

def login_button_clicked():
    login(username_entry.get(), password_entry.get())

def toggle_password_connection():
    if password_entry.cget('show') == '': 
        password_entry.config(show='*')
        toggle_button_password.config(text='Afficher le mot de passe', cursor="hand2")
    else:
        password_entry.config(show='') 
        toggle_button_password.config(text='Cacher le mot de passe', cursor="hand2")

def show_dashboard():
    clear_login_widgets()

    welcome_label.grid(row=10, column=0, columnspan=2)
    logout_button.grid(row=11, column=0, sticky='e', padx=5, pady=5)
    export_button.grid(row=11, column=1, sticky='w', padx=5, pady=5)

    search_label.grid(row=12, column=0, sticky='e', padx=5, pady=5)
    search_entry.grid(row=12, column=1, sticky='w', padx=5, pady=5)
    entry_name_label.grid(row=13, column=0, sticky='e', padx=5, pady=5)
    entry_name_entry.grid(row=13, column=1, sticky='w', padx=5, pady=5)
    entry_login_label.grid(row=14, column=0, sticky='e', padx=5, pady=5)
    entry_login_entry.grid(row=14, column=1, sticky='w', padx=5, pady=5)
    entry_password_label.grid(row=15, column=0, sticky='e', padx=5, pady=5)
    entry_password_entry.grid(row=15, column=1, sticky='w', padx=5, pady=5)
    save_button.grid(row=16, column=0, columnspan=2, pady=5)

def logout():
    global entry_labels
    global scrolling_frame 

    server_url = "https://monsite.local/api/logout" 
    
    try:
        response = session.post(server_url, verify=False)
        if response.status_code == 200:
            messagebox.showinfo("Succès", "Déconnexion réussie !") 
        else:
            messagebox.showerror("Erreur", "Échec de la déconnexion !") 
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de communication avec le serveur : {str(e)}") 

    clear_login_widgets()

    for label in entry_labels:
        label.grid_forget()
    entry_labels = []

    if scrolling_frame is not None:
        scrolling_frame.destroy()

    username_label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
    username_entry.grid(row=0, column=1, columnspan=2, sticky='w', padx=5, pady=5)
    password_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
    password_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    toggle_button_password.grid(row=1, column=2, padx=5, pady=5)
    digits_checkbox.grid(row=2, column=0, sticky='w', padx=5, pady=5)
    uppercase_checkbox.grid(row=3, column=0, sticky='w', padx=5, pady=5)
    lowercase_checkbox.grid(row=4, column=0, sticky='w', padx=5, pady=5)
    special_checkbox.grid(row=5, column=0, sticky='w', padx=5, pady=5)
    length_label.grid(row=7, column=0, sticky='e', padx=5, pady=5)
    length_entry.grid(row=7, column=1, sticky='w', padx=5, pady=5)
    generate_entry_password_with_length_button.grid(row=8, column=0, columnspan=2, pady=5)
    create_account_button.grid(row=9, column=0, pady=5)
    login_button.grid(row=9, column=1, pady=5)

def clear_login_widgets():
    welcome_label.grid_forget()
    logout_button.grid_forget()
    export_button.grid_forget()
    search_label.grid_forget()
    search_entry.grid_forget()
    entry_name_label.grid_forget()
    entry_name_entry.grid_forget()
    entry_login_label.grid_forget()
    entry_login_entry.grid_forget()
    entry_password_label.grid_forget()
    entry_password_entry.grid_forget()
    save_button.grid_forget()

def save_entry(name, login, password):
    server_url = "https://monsite.local/api/save_entry" 
    
    data = {'name': name, 'login': login, 'password': password} 
    
    try:
        response = session.post(server_url, json=data, verify=False)
        
        if response.status_code == 200:
            messagebox.showinfo("Succès", "Entrée enregistrée avec succès !") 
            entry_name_entry.delete(0, tk.END)
            entry_login_entry.delete(0, tk.END)
            entry_password_entry.delete(0, tk.END)
            show_entries()
        else:
            messagebox.showerror("Erreur", "Échec de l'enregistrement de l'entrée !") 
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de communication avec le serveur : {str(e)}") 

def show_entries():
    global entry_labels
    global scrolling_frame

    server_url = "https://monsite.local/api/get_entries"
    
    try:
        response = session.get(server_url, verify=False)
        if response.status_code == 200:
            entries = response.json().get('entries', [])

            if scrolling_frame is not None:
                scrolling_frame.destroy()

            scrolling_frame = tk.Frame(root)
            canvas = tk.Canvas(scrolling_frame)
            scrollbar = tk.Scrollbar(scrolling_frame, orient="vertical", command=canvas.yview)

            scrollable_frame = tk.Frame(canvas)

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            for index, entry in enumerate(entries):
                entry_label = tk.Label(
                    scrollable_frame,
                    text=f"{entry['name']} - {entry['login']} - {entry['password']}",
                    wraplength=450,
                    justify="left",
                    background="white"
                )
                entry_label.grid(row=index, column=0, sticky="w", padx=10, pady=5)

            scrolling_frame.grid(row=17, column=0, columnspan=2, padx=10, pady=10)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        else:
            messagebox.showerror("Erreur", "Échec de la récupération des entrées !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de communication avec le serveur : {str(e)}") 

def export_entries():
    server_url = "https://monsite.local/api/get_entries"
    
    try:
        response = session.get(server_url, verify=False)
        if response.status_code == 200:
            entries = response.json().get('entries', [])

            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")])

            if file_path:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Nom", "Login", "Mot de passe"])
                    for entry in entries:
                        writer.writerow([entry['name'], entry['login'], entry['password']])
                messagebox.showinfo("Succès", "Les entrées ont été exportées avec succès !")
        else:
            messagebox.showerror("Erreur", "Échec de la récupération des entrées pour l'exportation !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de communication avec le serveur : {str(e)}") 

root = tk.Tk()
root.title("Gestionnaire de mots de passe")
root.geometry("600x500")

police_font = font.Font(family="Helvetica", size=12)

# Label et Entrée pour le nom d'utilisateur
username_label = tk.Label(root, text="Nom d'utilisateur", font=police_font)
username_entry = tk.Entry(root, font=police_font)

# Label et Entrée pour le mot de passe
password_label = tk.Label(root, text="Mot de passe", font=police_font)
password_entry = tk.Entry(root, show='*', font=police_font)

# Bouton pour afficher ou cacher le mot de passe
toggle_button_password = tk.Button(root, text='Afficher le mot de passe', command=toggle_password_connection, cursor="hand2")

# Cases à cocher pour spécifier les caractères du mot de passe
var_digits = tk.BooleanVar(value=True)  # Initialisation à True
digits_checkbox = tk.Checkbutton(root, text="Chiffres", variable=var_digits, font=police_font)

var_uppercase = tk.BooleanVar(value=True)  # Initialisation à True
uppercase_checkbox = tk.Checkbutton(root, text="Majuscules", variable=var_uppercase, font=police_font)

var_lowercase = tk.BooleanVar(value=True)  # Initialisation à True
lowercase_checkbox = tk.Checkbutton(root, text="Minuscules", variable=var_lowercase, font=police_font)

var_special = tk.BooleanVar(value=True)  # Initialisation à True
special_checkbox = tk.Checkbutton(root, text="Caractères spéciaux", variable=var_special, font=police_font)

# Définir la longueur par défaut à 12
length_default = 12
length_label = tk.Label(root, text="Longueur du mot de passe", font=police_font)
length_entry = tk.Entry(root, font=police_font)
length_entry.insert(0, length_default)  # Insérer la valeur par défaut

# Bouton pour générer un mot de passe avec une longueur spécifiée
generate_entry_password_with_length_button = tk.Button(root, text="Générer un mot de passe avec la longueur spécifiée", command=lambda: fill_generated_password_with_length(password_entry, length_entry), cursor="hand2")

# Bouton pour créer un compte
create_account_button = tk.Button(root, text="Créer un compte", command=create_account_button_clicked, cursor="hand2")

# Bouton pour se connecter
login_button = tk.Button(root, text="Se connecter", command=login_button_clicked, cursor="hand2")

# Autres widgets pour le tableau de bord et la gestion des entrées
welcome_label = tk.Label(root, text="Bienvenue dans votre tableau de bord", font=police_font)
logout_button = tk.Button(root, text="Déconnexion", command=logout, cursor="hand2")
export_button = tk.Button(root, text="Exporter les entrées", command=export_entries, cursor="hand2")
search_label = tk.Label(root, text="Recherche :", font=police_font)
search_entry = tk.Entry(root, font=police_font)
entry_name_label = tk.Label(root, text="Nom :", font=police_font)
entry_name_entry = tk.Entry(root, font=police_font)
entry_login_label = tk.Label(root, text="Identifiant :", font=police_font)
entry_login_entry = tk.Entry(root, font=police_font)
entry_password_label = tk.Label(root, text="Mot de passe :", font=police_font)
entry_password_entry = tk.Entry(root, font=police_font)
save_button = tk.Button(root, text="Enregistrer", command=lambda: save_entry(entry_name_entry.get(), entry_login_entry.get(), entry_password_entry.get()), cursor="hand2")

# Label pour le lien vers le site Web
link_label = tk.Label(root, text="Essayer le site Web ?", fg="blue", cursor="hand2", font=police_font)
link_label.grid(row=18, column=0, columnspan=2, pady=5)
link_label.bind("<Button-1>", open_webpage)

# Placement des widgets avec grid
username_label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
username_entry.grid(row=0, column=1, columnspan=2, sticky='w', padx=5, pady=5)
password_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
password_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
toggle_button_password.grid(row=1, column=2, padx=5, pady=5)
digits_checkbox.grid(row=2, column=0, sticky='w', padx=5, pady=5)
uppercase_checkbox.grid(row=3, column=0, sticky='w', padx=5, pady=5)
lowercase_checkbox.grid(row=4, column=0, sticky='w', padx=5, pady=5)
special_checkbox.grid(row=5, column=0, sticky='w', padx=5, pady=5)
length_label.grid(row=7, column=0, sticky='e', padx=5, pady=5)
length_entry.grid(row=7, column=1, sticky='w', padx=5, pady=5)
generate_entry_password_with_length_button.grid(row=8, column=0, columnspan=2, pady=5)
create_account_button.grid(row=9, column=0, pady=5)
login_button.grid(row=9, column=1, pady=5)

# Démarrer l'interface graphique
root.mainloop()
