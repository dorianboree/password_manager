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
    webbrowser.open('https://onepass.com/')

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

def create_account(username, password):
    if not check_username(username):
        messagebox.showerror("Erreur", "Le nom d'utilisateur doit comporter entre 8 et 30 caractères et ne doit pas contenir de caractères spéciaux ou de lettre avec accent.")
        return
    if not check_password(password):
        messagebox.showerror("Erreur", "Le mot de passe doit comporter entre 8 et 80 caractères, dont une majuscule, une minuscule, un chiffre et un caractère spécial.")
        return

    server_url = "https://onepass.com/api/create_account"
    
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
    if not check_username(username):
        messagebox.showerror("Erreur", "Le nom d'utilisateur doit comporter entre 8 et 30 caractères et ne doit pas contenir de caractères spéciaux ou de lettre avec accent.")
        return
    if not check_password(password):
        messagebox.showerror("Erreur", "Le mot de passe doit comporter entre 8 et 80 caractères, dont une majuscule, une minuscule, un chiffre et un caractère spécial.")
        return
    
    server_url = "https://onepass.com/api/login" 
    
    data = {'username': username, 'password': password} 
    
    try:
        response = session.post(server_url, json=data, verify=False)
        
        if response.status_code == 200: 
            show_dashboard()
            show_entries() 
        else:
            messagebox.showerror("Erreur", "Échec de la connexion ! Compte inexistant ou mot de passe incorrect.")
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
    username_label.place_forget() 
    username_entry.place_forget() 
    password_label.place_forget() 
    password_entry.place_forget() 
    toggle_button_password.place_forget()
    create_account_button.place_forget() 
    login_button.place_forget() 
    
    welcome_label.pack()
    logout_button.pack(side="top", anchor="ne")
    export_button.pack(side="top", anchor="ne")
    logout_button.place(relx=1, rely=0, anchor="ne")
    export_button.place(relx=0.99, rely=0, x=-logout_button.winfo_reqwidth(), anchor="ne")

    entry_name_label.pack()
    entry_name_entry.pack()
    entry_login_label.pack()
    entry_login_entry.pack()
    entry_password_label.pack()
    entry_password_entry.pack()
    save_button.pack()

    # Ajout des widgets pour la génération de mot de passe
    length_label.pack()
    length_entry.pack()
    include_uppercase_check.pack()
    include_lowercase_check.pack()
    include_digits_check.pack()
    include_special_check.pack()
    show_password_check.pack()
    toggle_button_generated_password.pack()
    password_gen_button.pack()
    password_gen_entry.pack()

    search_label.pack()
    search_entry.pack()
    search_button.pack()

    show_entries()

def logout():
    global entry_labels, scrolling_frame 

    server_url = "https://onepass.com/api/logout" 
    
    try:
        response = session.post(server_url, verify=False)
        if response.status_code == 200:
            messagebox.showinfo("Succès", "Déconnexion réussie !") 
        else:
            messagebox.showerror("Erreur", "Échec de la déconnexion !") 
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de communication avec le serveur : {str(e)}") 

    username_entry.delete(0, tk.END) 
    password_entry.delete(0, tk.END)
    entry_name_entry.delete(0, tk.END) 
    entry_login_entry.delete(0, tk.END) 
    entry_password_entry.delete(0, tk.END) 

    for label in entry_labels:
        label.destroy()
    entry_labels = []

    if scrolling_frame is not None:
        scrolling_frame.destroy()

    for widget in [username_label, username_entry, password_label, password_entry, toggle_button_password, create_account_button, login_button]:
        widget.place(relx=0.5, rely=0.3 + 0.05 * list([username_label, username_entry, password_label, password_entry, toggle_button_password, create_account_button, login_button]).index(widget), anchor='center')

    for widget in [welcome_label, logout_button, export_button, entry_name_label, entry_name_entry, entry_login_label, entry_login_entry, entry_password_label, entry_password_entry, save_button, length_label, length_entry, include_uppercase_check, include_lowercase_check, include_digits_check, include_special_check, show_password_check, toggle_button_generated_password, password_gen_button, password_gen_entry, search_label, search_entry, search_button, password_entry]:
        widget.pack_forget()

    export_button.place_forget()
    logout_button.place_forget()

def get_entries():
    server_url = "https://onepass.com/api/get_entries" 

    try:
        response = session.get(server_url, verify=False) 
        if response.status_code == 200:
            entries_data = response.json().get('entries', [])
            return entries_data 
        else:
            messagebox.showerror("Erreur", "Échec de récupération des entrées du serveur!")
            return []
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de communication avec le serveur: {str(e)}")
        return [] 

def make_copy_command(text):
    return lambda: pyperclip.copy(text) 

def make_toggle_password_func(entry_password_entry, button):
    def toggle_password():
        if entry_password_entry.cget('show') == '': 
            entry_password_entry.config(show='*') 
            button.config(text='Afficher le mot de passe',cursor="hand2")
        else:
            entry_password_entry.config(show='') 
            button.config(text='Cacher le mot de passe', cursor="hand2") 
    return toggle_password

entry_labels = [] 
scrolling_frame = None 

def show_entries():
    global entry_labels, scrolling_frame

    if scrolling_frame is not None:
        scrolling_frame.destroy()

    entries_data = get_entries()
    scrolling_frame = tk.Frame(root)
    scrolling_frame.pack(fill='both', expand=True)

    canvas = tk.Canvas(scrolling_frame)
    canvas.pack(side='left', fill='both', expand=True)

    scrollbar = tk.Scrollbar(scrolling_frame, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')

    canvas.configure(yscrollcommand=scrollbar.set)
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor='nw')

    frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    entry_labels = []

    for entry_data in entries_data:
        entry_name = entry_data.get('entry_name', '')
        entry_login = entry_data.get('entry_login', '')
        entry_password = entry_data.get('entry_password', '')

        entry_frame = tk.Frame(frame)
        entry_frame.pack(fill='x', padx=10, pady=5)

        entry_name_label = tk.Label(entry_frame, text=f'Nom de l\'entrée : {entry_name}', font=font.Font(weight="bold"))
        entry_name_label.pack(side='top', anchor='w')

        entry_login_label = tk.Label(entry_frame, text=f'Login : {entry_login}')
        entry_login_label.pack(side='left')
        copy_button_login = tk.Button(entry_frame, text='Copier le login', command=make_copy_command(entry_login), cursor="hand2")
        copy_button_login.pack(side='left', padx=10)

        entry_password_entry = tk.Entry(entry_frame, show='*', width=30)
        entry_password_entry.insert(0, entry_password)
        entry_password_entry.pack(side='left')
        copy_button_password = tk.Button(entry_frame, text='Copier le mot de passe', command=make_copy_command(entry_password), cursor="hand2")
        copy_button_password.pack(side='left', padx=10)

        toggle_button = tk.Button(entry_frame, text='Afficher le mot de passe', command=make_toggle_password_func(entry_password_entry, toggle_button_password), cursor="hand2")
        toggle_button.pack(side='left', padx=10)

        entry_labels.append(entry_frame)

def generate_password():
    try:
        length = int(length_entry.get())
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer une longueur valide.")
        return

    if length < 8 or length > 80:
        messagebox.showerror("Erreur", "La longueur du mot de passe doit être entre 8 et 80.")
        return

    characters = ""
    if include_uppercase_var.get():
        characters += string.ascii_uppercase
    if include_lowercase_var.get():
        characters += string.ascii_lowercase
    if include_digits_var.get():
        characters += string.digits
    if include_special_var.get():
        characters += "!@#$%^&*()-+?_=,<>/"

    if not characters:
        messagebox.showerror("Erreur", "Veuillez sélectionner au moins un type de caractère.")
        return

    password = ''.join(random.choice(characters) for i in range(length))
    password_gen_entry.delete(0, tk.END)
    password_gen_entry.insert(0, password)

    if not show_password_var.get():
        password_gen_entry.config(show='*')
    else:
        password_gen_entry.config(show='')

def toggle_generated_password():
    if password_gen_entry.cget('show') == '':
        password_gen_entry.config(show='*')
        toggle_button_generated_password.config(text='Afficher le mot de passe')
    else:
        password_gen_entry.config(show='')
        toggle_button_generated_password.config(text='Cacher le mot de passe')

# Widgets for main window
root = tk.Tk()
root.title("OnePass")
root.state('zoomed')

title_label = tk.Label(root, text="OnePass", font=("Helvetica", 24, "bold"))
title_label.pack()

username_label = tk.Label(root, text="Nom d'utilisateur")
username_label.place(relx=0.5, rely=0.3, anchor='center')
username_entry = tk.Entry(root)
username_entry.place(relx=0.5, rely=0.35, anchor='center')

password_label = tk.Label(root, text="Mot de passe")
password_label.place(relx=0.5, rely=0.4, anchor='center')
password_entry = tk.Entry(root, show='*')
password_entry.place(relx=0.5, rely=0.45, anchor='center')

toggle_button_password = tk.Button(root, text='Afficher le mot de passe', command=toggle_password_connection, cursor="hand2")
toggle_button_password.place(relx=0.5, rely=0.5, anchor='center')

create_account_button = tk.Button(root, text="Créer un compte", command=create_account_button_clicked, cursor="hand2")
create_account_button.place(relx=0.5, rely=0.55, anchor='center')

login_button = tk.Button(root, text="Se connecter", command=login_button_clicked, cursor="hand2")
login_button.place(relx=0.5, rely=0.6, anchor='center')

welcome_label = tk.Label(root, text="Bienvenue sur le tableau de bord", font=("Helvetica", 18, "bold"))
logout_button = tk.Button(root, text="Se déconnecter", command=logout, cursor="hand2")
export_button = tk.Button(root, text="Exporter", command=lambda: export_to_csv(get_entries()), cursor="hand2")

entry_name_label = tk.Label(root, text="Nom de l'entrée")
entry_name_entry = tk.Entry(root)

entry_login_label = tk.Label(root, text="Login")
entry_login_entry = tk.Entry(root)

entry_password_label = tk.Label(root, text="Mot de passe")
entry_password_entry = tk.Entry(root, show='*')

save_button = tk.Button(root, text="Enregistrer", command=lambda: save_entry(entry_name_entry.get(), entry_login_entry.get(), entry_password_entry.get()), cursor="hand2")

# Password generation customization
length_label = tk.Label(root, text="Longueur du mot de passe")
length_entry = tk.Entry(root)
length_entry.insert(0, "12")

include_uppercase_var = tk.BooleanVar(value=True)
include_lowercase_var = tk.BooleanVar(value=True)
include_digits_var = tk.BooleanVar(value=True)
include_special_var = tk.BooleanVar(value=True)
show_password_var = tk.BooleanVar(value=False)

include_uppercase_check = tk.Checkbutton(root, text="Inclure des majuscules", variable=include_uppercase_var)
include_lowercase_check = tk.Checkbutton(root, text="Inclure des minuscules", variable=include_lowercase_var)
include_digits_check = tk.Checkbutton(root, text="Inclure des chiffres", variable=include_digits_var)
include_special_check = tk.Checkbutton(root, text="Inclure des caractères spéciaux", variable=include_special_var)
show_password_check = tk.Checkbutton(root, text="Afficher le mot de passe", variable=show_password_var, command=toggle_generated_password)

toggle_button_generated_password = tk.Button(root, text='Cacher le mot de passe', command=toggle_generated_password, cursor="hand2")
password_gen_button = tk.Button(root, text="Générer le mot de passe", command=generate_password, cursor="hand2")
password_gen_entry = tk.Entry(root)

search_label = tk.Label(root, text="Rechercher")
search_entry = tk.Entry(root)
search_button = tk.Button(root, text="Rechercher", command=lambda: search_entries(search_entry.get()), cursor="hand2")

# Functions for password generation

# Functions for password generation
def generate_password():
    try:
        length = int(length_entry.get())
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer une longueur valide.")
        return

    if length < 8 or length > 80:
        messagebox.showerror("Erreur", "La longueur du mot de passe doit être entre 8 et 80.")
        return

    characters = ""
    if include_uppercase_var.get():
        characters += string.ascii_uppercase
    if include_lowercase_var.get():
        characters += string.ascii_lowercase
    if include_digits_var.get():
        characters += string.digits
    if include_special_var.get():
        characters += "!@#$%^&*()-+?_=,<>/"

    if not characters:
        messagebox.showerror("Erreur", "Veuillez sélectionner au moins un type de caractère.")
        return

    password = ''.join(random.choice(characters) for i in range(length))
    password_gen_entry.delete(0, tk.END)
    password_gen_entry.insert(0, password)

    if not show_password_var.get():
        password_gen_entry.config(show='*')
    else:
        password_gen_entry.config(show='')

def toggle_generated_password():
    if password_gen_entry.cget('show') == '':
        password_gen_entry.config(show='*')
        toggle_button_generated_password.config(text='Afficher le mot de passe')
    else:
        password_gen_entry.config(show='')
        toggle_button_generated_password.config(text='Cacher le mot de passe')

# Start the main loop
root.mainloop()
