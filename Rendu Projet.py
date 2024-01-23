import csv
import tkinter as tk
import math

def dataset(file):
    #Ouvrir le fichier csv en mode lecture
    with open(file,'r') as f:
        #Créer un lecteur csv à partir du fichier en spécifiant le délimiteur ';'
        reader = csv.DictReader(f, delimiter=';')

        #Liste vide pour stocker les données
        data = []

        #Parcourir chaque ligne du fichier et les stocker dans la liste sous forme de dictionnaire
        for ligne in reader:
            data.append(ligne)
        
    return data

def calculation(personne):
    # Récupération des données de chaque personne
    amount = int(personne['Amount borrowed'].replace(" ", ""))
    rate = float(personne['Rate'].replace("%", "").replace(",", ".")) / 100
    payment = float(personne['Monthly'].replace(" ", "").replace(",", ".").replace("€", "").replace("-", ""))
    
    # Calculate the loan duration
    monthly_rate = rate / 12
    duration = math.log(payment / (payment - monthly_rate * amount)) / math.log(1 + monthly_rate)
    duration /= 12

    return int(duration)

def save(file, data):

    # Ouvir le fichier en mode écriture
    with open(file, 'w', newline='') as f:
        # Créer un writer avec les en-têtes suivants en spécifiant le délimiteur ';'
        writer = csv.DictWriter(f, fieldnames=['Name', 'Loan period', 'Status'], delimiter=";")

        # Ecriture des données dans le fichier en format csv
        writer.writeheader()
        for personne in data:
            writer.writerow({'Name': personne['Name'], 'Loan period' : personne['Loan period'], 'Status' : personne['Status']})

def application(file):
    # Récupère les données du fichier
    data = dataset(file)

    # Création de la fenêtre
    root = tk.Tk()
    root.title("Application")
    font = 16
    padding = 10
    label = tk.Label(root, text="All requests of brokers for new mortgage", font=("Times", 20, "bold"))
    label.pack()

    for i in range(lenData := len(data)):
        # Format de l'interface en fonction du nombre de personnes
        if lenData > 15:
            font = 10
            padding = 5

            if lenData > 24:
                font = 8
                padding = 3

        # Affiche si une personne est élgible au prêt
        if (status := data[i]["Status"]) == "Invalid":
            tk.Label(root, text=f"{data[i]['Name']:^5}  :  {status:<10}", font=("Times", font), bg='red').pack(pady=padding)
        else:
            tk.Label(root, text=f"{data[i]['Name']:^5}  :  {status:<10}", font=("Times", font), bg='green').pack(pady=padding)

    root.mainloop()

file = "2 - Files\customers.csv"

# Récupère les données du fichier
data = dataset(file)

# Définie si une personne est éligible au prêt
for personne in data:
    duration = calculation(personne)
    personne["Loan period"] = duration

    if duration > 30:
        personne['Status'] = "Invalid"
    else:
        personne['Status'] = "Ok"

fileResultat = "resultats.txt"

# Sauvegarde les données
save(fileResultat, data)

# Démarrage de l'application
application(fileResultat)