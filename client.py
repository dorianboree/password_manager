# client.py
import tkinter as tk
from tkinter import messagebox
import requests
import pyperclip

session = requests.Session()

def create_account(username, password):
    if not username or not password: 
        messagebox.showerror("Erreur", "Veuillez saisir un nom d'utilisateur et un mot de passe.")
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
    if not username or not password: 
        messagebox.showerror("Erreur", "Veuillez saisir un nom d'utilisateur et un mot de passe.") 
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
        toggle_button_password.config(text='Afficher le mot de passe')
    else:
        password_entry.config(show='') 
        toggle_button_password.config(text='Cacher le mot de passe')

def toggle_password_entry(entry_password_entry):
    if entry_password_entry.cget('show') == '':
        entry_password_entry.config(show='*') 
        toggle_button_password.config(text='Afficher le mot de passe')
    else:
        entry_password_entry.config(show='') 
        toggle_button_password.config(text='Cacher le mot de passe')

def show_dashboard():
    username_label.pack_forget() 
    username_entry.pack_forget() 
    password_label.pack_forget() 
    password_entry.pack_forget() 
    toggle_button_password.pack_forget()
    login_button.pack_forget() 
    create_account_button.pack_forget() 
    
    welcome_label.pack()
    logout_button.pack(side="top", anchor="ne")
    entry_button.pack() 

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

    username_label.pack() 
    username_entry.pack()
    password_label.pack()
    password_entry.pack() 
    toggle_button_password.pack() 
    login_button.pack()
    create_account_button.pack() 
    
    welcome_label.pack_forget() 
    logout_button.pack_forget()
    entry_button.pack_forget()
    spacer.pack_forget()

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
            button.config(text='Afficher le mot de passe')
        else:
            entry_password_entry.config(show='') 
            button.config(text='Cacher le mot de passe') 
    return toggle_password

entry_labels = [] 
scrolling_frame = None 
spacer = None 

def show_entries():
    global entry_labels, scrolling_frame, spacer
    entries_data = get_entries() 

    if entries_data:
        if spacer is not None: 
            spacer.destroy()

        spacer = tk.Label(root, height=20) 
        spacer.pack()

        scrolling_frame = tk.Frame(root, width=1050, height=800)
        scrolling_frame.pack(side='bottom')

        canvas = tk.Canvas(scrolling_frame, width=1050, height=800)
        scrollbar = tk.Scrollbar(scrolling_frame, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        for entry in entries_data:
            entry_frame = tk.Frame(frame)
            entry_frame.pack(fill='x')

            name_label = tk.Label(entry_frame, text="Nom :")
            name_label.pack(side='left')

            name_var = tk.StringVar(value=entry['name'])
            name_entry = tk.Entry(entry_frame, textvariable=name_var, state='readonly')
            name_entry.pack(side='left')

            login_label = tk.Label(entry_frame, text="Login :")
            login_label.pack(side='left')
            login_var = tk.StringVar(value=entry['login'])
            login_entry = tk.Entry(entry_frame, textvariable=login_var, state='readonly')
            login_entry.pack(side='left')

            copy_login_button = tk.Button(entry_frame, text="Copier le login", command=make_copy_command(entry['login']))
            copy_login_button.pack(side='left')

            password_label = tk.Label(entry_frame, text="Mot de passe :")
            password_label.pack(side='left')
            password_var = tk.StringVar(value=entry['password'])
            password_entry = tk.Entry(entry_frame, textvariable=password_var, state='readonly', show='*')
            password_entry.pack(side='left')

            toggle_entry_password_button = tk.Button(entry_frame, text='Afficher le mot de passe')
            toggle_entry_password_button.config(command=make_toggle_password_func(password_entry, toggle_entry_password_button))
            toggle_entry_password_button.pack(side='left')

            copy_password_button = tk.Button(entry_frame, text="Copier le mot de passe", command=make_copy_command(entry['password']))
            copy_password_button.pack(side='left')

            delete_entry_button = tk.Button(entry_frame, text='Supprimer l\'entrée', command=make_delete_entry_func(entry['id'], entry_frame))
            delete_entry_button.pack(side='left')

            entry_frame.pack(anchor='center')

            entry_labels.append(entry_frame)

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))
    else:
        messagebox.showinfo("Information", "Aucune entrée disponible.")

def save_entry():
    entry_window = tk.Toplevel(root)
    entry_window.title("Nouvelle Entrée")

    entry_name_label = tk.Label(entry_window, text="Nom de l'entrée :")
    entry_name_entry = tk.Entry(entry_window)
    entry_login_label = tk.Label(entry_window, text="Nom d'utilisateur :")
    entry_login_entry = tk.Entry(entry_window)
    entry_password_label = tk.Label(entry_window, text="Mot de passe :")
    entry_password_entry = tk.Entry(entry_window, show='*')

    toggle_button_password = tk.Button(entry_window, text='Afficher le mot de passe', width=20, command=lambda: toggle_password_entry(entry_password_entry))

    save_button = tk.Button(entry_window, text="Enregistrer", command=lambda: save_entry_details(entry_name_entry.get(), entry_login_entry.get(), entry_password_entry.get(), entry_window))

    entry_name_label.grid(row=0, column=0, padx=10, pady=5)
    entry_name_entry.grid(row=0, column=1, padx=10, pady=5)
    entry_login_label.grid(row=1, column=0, padx=10, pady=5)
    entry_login_entry.grid(row=1, column=1, padx=10, pady=5)
    entry_password_label.grid(row=2, column=0, padx=10, pady=5)
    entry_password_entry.grid(row=2, column=1, padx=10, pady=5)
    toggle_button_password.grid(row=3, column=0, columnspan=2, pady=10)
    save_button.grid(row=4, column=0, columnspan=2, pady=10)

def save_entry_details(entry_name, entry_login, entry_password, entry_window):
    if not entry_name or not entry_login or not entry_password:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs de l'entrée.")
        return

    server_url = "https://monsite.local/api/save_entry"

    data = {'entryName': entry_name, 'entryLogin': entry_login, 'entryPassword': entry_password}
    
    try:
        response = session.post(server_url, json=data, verify=False) 
        
        if response.status_code == 200: 
            messagebox.showinfo("Succès", "Entrée enregistrée avec succès !")
            
            entry_window.destroy()

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


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
                                                                                # Création de la fenêtre principale
root = tk.Tk()
root.title("Gestionnaire de mot de passe en ligne")

# Définir la taille de la fenêtre
window_width = 1000
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Création des widgets
username_label = tk.Label(root, text="Nom d'utilisateur :")
password_label = tk.Label(root, text="Mot de passe :")
username_entry = tk.Entry(root)
password_entry = tk.Entry(root, show='*', width=20)
toggle_button_password = tk.Button(root, text='Afficher le mot de passe', width=20, command=toggle_password_connection)
login_button = tk.Button(root, text="Connexion", command=login_button_clicked)
create_account_button = tk.Button(root, text="Créer un compte", command=create_account_button_clicked)

# Utilisation de pack pour placer les widgets de la page de connexion et les centrer
username_label.pack(pady=10)
username_entry.pack(pady=10)
password_label.pack(pady=10)
password_entry.pack(pady=10)
toggle_button_password.pack(pady=10)
login_button.pack(pady=10)
create_account_button.pack(pady=10)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
                                                                                # Création du tableau de bord

# Création des widgets du tableau de bord
welcome_label = tk.Label(root, text="Bienvenue dans le tableau de bord !")
logout_button = tk.Button(root, text="Déconnexion", command=logout)
entry_button = tk.Button(root, text="Ajouter une entrée", command=save_entry)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Boucle principale de la fenêtre
root.mainloop()
