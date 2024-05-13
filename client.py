# client.py

import tkinter as tk
from tkinter import messagebox, font, filedialog
import requests
import pyperclip
import webbrowser
import csv

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

    username_entry.delete(0, tk.END) 
    password_entry.delete(0, tk.END) 

    for label in entry_labels:
        label.destroy()
    entry_labels = []

    if scrolling_frame is not None:
        scrolling_frame.destroy()

    username_label.place(relx=0.5, rely=0.3, anchor='center')
    username_entry.place(relx=0.5, rely=0.35, anchor='center')
    password_label.place(relx=0.5, rely=0.4, anchor='center')
    password_entry.place(relx=0.5, rely=0.45, anchor='center')
    toggle_button_password.place(relx=0.5, rely=0.5, anchor='center')
    create_account_button.place(relx=0.5, rely=0.6, anchor='center')
    login_button.place(relx=0.5, rely=0.55, anchor='center')
    
    welcome_label.pack_forget() 
    logout_button.pack_forget()
    export_button.pack_forget()
    logout_button.place_forget()
    export_button.place_forget()
    entry_name_label.pack_forget()
    entry_name_entry.pack_forget()
    entry_login_label.pack_forget()
    entry_login_entry.pack_forget()
    entry_password_label.pack_forget()
    entry_password_entry.pack_forget()
    save_button.pack_forget()

def get_entries():
    server_url = "https://monsite.local/api/get_entries" 

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
    entries_data = get_entries()
    entry_font = font.Font(family='Helvetica', size=10, weight='bold')

    if entries_data:
        scrolling_frame = tk.Frame(root)
        scrolling_frame.pack(side='bottom')

        canvas = tk.Canvas(scrolling_frame, width=1100, height=600)
        scrollbar = tk.Scrollbar(scrolling_frame, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='n')

        for entry in entries_data:
            entry_frame = tk.Frame(frame)
            entry_frame.pack(fill='x', pady=10)

            name_label = tk.Label(entry_frame, text="Nom", font=entry_font)
            name_label.pack(side='left', padx=(20, 0))
            name_var = tk.StringVar(value=entry['name'])
            name_entry = tk.Entry(entry_frame, textvariable=name_var, state='readonly')
            name_entry.pack(side='left')

            login_label = tk.Label(entry_frame, text="Login", font=entry_font)
            login_label.pack(side='left', padx=(20, 0))
            login_var = tk.StringVar(value=entry['login'])
            login_entry = tk.Entry(entry_frame, textvariable=login_var, state='readonly')
            login_entry.pack(side='left')

            copy_login_button = tk.Button(entry_frame, text="Copier le login", cursor="hand2", command=make_copy_command(entry['login']))
            copy_login_button.pack(side='left')

            password_label = tk.Label(entry_frame, text="Mot de passe", font=entry_font)
            password_label.pack(side='left', padx=(20, 0))
            password_var = tk.StringVar(value=entry['password'])
            password_entry = tk.Entry(entry_frame, textvariable=password_var, state='readonly', show='*')
            password_entry.pack(side='left')

            toggle_entry_password_button = tk.Button(entry_frame, text='Afficher le mot de passe')
            toggle_entry_password_button.config(cursor="hand2", command=make_toggle_password_func(password_entry, toggle_entry_password_button))
            toggle_entry_password_button.pack(side='left')

            copy_password_button = tk.Button(entry_frame, text="Copier le mot de passe", cursor="hand2", command=make_copy_command(entry['password']))
            copy_password_button.pack(side='left')

            delete_entry_button = tk.Button(entry_frame, text='Supprimer l\'entrée', cursor="hand2", command=make_delete_entry_func(entry['id'], entry_frame))
            delete_entry_button.pack(side='left')

            entry_frame.pack(anchor='center')

            separator = tk.Frame(frame, height=2, bg="grey")
            separator.pack(fill='x', pady=(0,10))

            entry_labels.append(entry_frame)

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))
    else:
        messagebox.showinfo("Information", "Aucune entrée disponible.")

def save_entry_details(entry_name, entry_login, entry_password):
    if not entry_name or not entry_login or not entry_password:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs de l'entrée.")
        return

    server_url = "https://monsite.local/api/save_entry"

    data = {'entryName': entry_name, 'entryLogin': entry_login, 'entryPassword': entry_password}
    
    try:
        response = session.post(server_url, json=data, verify=False) 
        
        if response.status_code == 200: 
            messagebox.showinfo("Succès", "Entrée enregistrée avec succès !")

            for entry_label in entry_labels:
                entry_label.destroy()
            entry_labels.clear()

            if scrolling_frame is not None: 
                scrolling_frame.destroy()

            show_entries() 
        else:
            messagebox.showerror("Erreur", "Échec de l'enregistrement de l'entrée !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de communication avec le serveur : {str(e)}") 

def make_delete_entry_func(entry_id, entry_frame):
    def delete_entry():
        server_url = f"https://monsite.local/api/delete_entry/{entry_id}"
        
        if messagebox.askokcancel("Confirmation", "Êtes-vous sûr de vouloir supprimer cette entrée ?"):
            try:
                response = session.delete(server_url, verify=False) 

                if response.status_code == 200: 
                    messagebox.showinfo("Succès", "Entrée supprimée avec succès !") 

                    entry_frame.destroy()
                else:
                    messagebox.showerror("Erreur", "Échec de la suppression de l'entrée !")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur de communication avec le serveur : {str(e)}")

    return delete_entry

def export_to_csv():
    entries = get_entries()
    filename = filedialog.asksaveasfilename(defaultextension='.csv', initialfile='password.csv')

    if not filename:
        return

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = entries[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in entries:
            writer.writerow(entry)

    messagebox.showinfo("Succès", "Les entrées ont été exportées avec succès dans le fichier '{}'.".format(filename))

root = tk.Tk()
root.title("Gestionnaire de mot de passe en ligne")

root.state('zoomed')

police_font = font.Font(family='Helvetica', size=15, weight='bold')

username_label = tk.Label(root, text="Nom d'utilisateur", font=police_font)
username_entry = tk.Entry(root, font=police_font)
password_label = tk.Label(root, text="Mot de passe", font=police_font)
password_entry = tk.Entry(root, show='*', width=20, font=police_font)
toggle_button_password = tk.Button(root, text='Afficher le mot de passe', width=20, cursor="hand2", font=police_font, command=toggle_password_connection)
create_account_button = tk.Button(root, text="Créer un compte", width=20, cursor="hand2", font=police_font, command=create_account_button_clicked)
login_button = tk.Button(root, text="Connexion", width=20, cursor="hand2", font=police_font, command=login_button_clicked)

username_label.place(relx=0.5, rely=0.3, anchor='center')
username_entry.place(relx=0.5, rely=0.35, anchor='center')
password_label.place(relx=0.5, rely=0.4, anchor='center')
password_entry.place(relx=0.5, rely=0.45, anchor='center')
toggle_button_password.place(relx=0.5, rely=0.5, anchor='center')
create_account_button.place(relx=0.5, rely=0.6, anchor='center')
login_button.place(relx=0.5, rely=0.55, anchor='center')

link_label = tk.Label(root, text="Essayer le site Web ?", fg="blue", cursor="hand2", font=police_font)
link_label.pack(side='bottom')
link_label.bind("<Button-1>", open_webpage)

welcome_label = tk.Label(root, text="Bienvenue dans le tableau de bord !")
logout_button = tk.Button(root, text="Déconnexion", cursor="hand2", command=logout)
export_button = tk.Button(root, text="Exporter les données", cursor="hand2", command=export_to_csv)

entry_name_label = tk.Label(root, text="Nom")
entry_name_entry = tk.Entry(root)
entry_login_label = tk.Label(root, text="Login")
entry_login_entry = tk.Entry(root)
entry_password_label = tk.Label(root, text="Mot de passe")
entry_password_entry = tk.Entry(root, show='*')
save_button = tk.Button(root, text="Enregistrer l'entrée", cursor="hand2", command=lambda: save_entry_details(entry_name_entry.get(), entry_login_entry.get(), entry_password_entry.get()))

root.mainloop()
