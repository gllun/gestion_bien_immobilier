import tkinter as tk
import sqlite3
from tkinter.messagebox import *
from tkcalendar import DateEntry
from tkinter import ttk
from datetime import datetime

# Creation de ma base de donnees
try:
    conn = sqlite3.connect('gestion_immo.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS T_GESTIONIMMO(
         ID_GESTIONIMMO INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
         BIEN VARCHAR(12) NOT NULL,
         NATURE_GESTION VARCHAR(9) NOT NULL,
         NO INTEGER CHECK (NO>=1),
         TYPE_VOIE VARCHAR(12) NOT NULL,
         NOM_VOIE VARCHAR(100) NOT NULL,
         CODE_POSTAL INT CHECK(CODE_POSTAL>0),
         COMMUNE VARCHAR(40),
         S_COUVERTE INT CHECK(S_COUVERTE>0),
         S_JARDIN INT NULL,
         NOMBRE_PIECE INT NOT NULL,
         CLASSE_ENERGETIQUE VARCHAR(1) NOT NULL,
         ANNEE_CONSTRUCTION INT NOT NULL,
         DATE_MISE_MARCHE DATE NOT NULL,
         PRIX INT NOT NULL
    )
    ''')
    conn.commit()
finally:
    conn.close()


# Creation Page Class
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


# Page creation inheriting page class
class PageResearch(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        conn_r = sqlite3.connect('gestion_immo.db')
        curseur = conn_r.cursor()
        curseur.execute("SELECT * FROM T_GESTIONIMMO")
        self.result = curseur.fetchall()
        i = 1
        j = 1
        b = 1
        for tuple_bien in self.result:
            e = tk.Label(self, width=10, fg='blue', text=tuple_bien[b])
            e.grid(row=i, column=j, padx=2)
            e = tk.Label(self, width=10, fg='blue', text=tuple_bien[b + 1])
            e.grid(row=i, column=j + 1, padx=2)
            e = tk.Label(self, width=10, fg='blue', text=tuple_bien[b + 5])
            e.grid(row=i, column=j + 2, padx=2)
            e = tk.Label(self, width=10, fg='blue', text=tuple_bien[b + 6])
            e.grid(row=i, column=j + 3, padx=2)
            e = tk.Label(self, width=10, fg='blue', text=tuple_bien[b + 9])
            e.grid(row=i, column=j + 4, padx=2)
            e = tk.Label(self, width=10, fg='blue', text=tuple_bien[b + 10])
            e.grid(row=i, column=j + 5, padx=2)
            e = tk.Label(self, width=10, fg='blue', text=tuple_bien[b + 13])
            e.grid(row=i, column=j + 6, padx=2)
            i += 1
        conn_r.close()

    def refresh_db(self):
        for old_bien in self.grid_slaves():
            old_bien.destroy()

        conn_r = sqlite3.connect('gestion_immo.db')
        curseur = conn_r.cursor()
        curseur.execute("SELECT * FROM T_GESTIONIMMO")
        self.result = curseur.fetchall()
        i = 1
        j = 1
        for tuple_bien in self.result:
            e = tk.Label(self, width=10, fg='blue', text=tuple_bien[j])
            e.grid(row=i, column=j, padx=2)
            e = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 1])
            e.grid(row=i, column=j + 1, padx=2)
            e = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 5])
            e.grid(row=i, column=j + 2, padx=2)
            e = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 6])
            e.grid(row=i, column=j + 3, padx=2)
            e = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 9])
            e.grid(row=i, column=j + 4, padx=2)
            e = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 10])
            e.grid(row=i, column=j + 5, padx=2)
            e = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 13])
            e.grid(row=i, column=j + 6, padx=2)
            i += 1
        conn_r.close()


# Class Enregistrement des données d'un bien(fait)
class PageSave(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.columnconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)

        self.value_bien = tk.StringVar()
        b_appart = tk.Radiobutton(self, text="Appartement", variable=self.value_bien, value='Appartement',
                                  command=self.disableEntryAreaGarden)
        b_house = tk.Radiobutton(self, text="Maison", variable=self.value_bien, value='Maison',
                                 command=self.enableEntryAreaGarden)
        tk.Label(self, text="N°").grid(row=1, column=1)
        self.e_no = tk.Entry(self, bd=5)

        tk.Label(self, text="Type de voie : ").grid(row=2, column=1)
        liste_typewall = ["Rue", "Impasse", "Avenue", "Boulevard", "Allée", "Place"]
        self.listCombo = ttk.Combobox(self, values=liste_typewall, state="readonly")
        self.listCombo.grid(row=2, column=2)

        tk.Label(self, text="Nom de rue : ").grid(row=3, column=1)
        self.e_namewall = tk.Entry(self, bd=5)
        tk.Label(self, text="Code Postale : ").grid(row=4, column=1)
        self.e_postalecode = tk.Entry(self, bd=5)
        tk.Label(self, text="Commune :").grid(row=5, column=1)
        self.e_common = tk.Entry(self, bd=5)
        tk.Label(self, text="Superficie couvert : ").grid(row=6, column=1)
        self.e_areacovered = tk.Entry(self, bd=5)
        tk.Label(self, text="Superficie jardin : ").grid(row=7, column=1)
        self.e_areagarden = tk.Entry(self, bd=5)
        tk.Label(self, text="Nombre de pièce : ").grid(row=8, column=1)
        self.e_numroom = tk.Entry(self, bd=5)
        tk.Label(self, text="Classe énergétique : ").grid(row=9, column=1)
        self.e_energyclass = tk.Entry(self, bd=5)
        tk.Label(self, text="Année de construction : ").grid(row=10, column=1)
        self.e_yearconstruct = tk.Entry(self, bd=5)
        self.value_naturemana = tk.StringVar()
        b_sell = tk.Radiobutton(self, text="Vente", variable=self.value_naturemana, value='Vente')
        b_location = tk.Radiobutton(self, text="Location", variable=self.value_naturemana, value='Location')
        tk.Label(self, text="Date de mise en marche").grid(row=12, column=1)
        self.cal = DateEntry(self, selectmode='day', date_pattern='dd/mm/yyyy')
        tk.Label(self, text="Prix").grid(row=13, column=1)
        self.e_price = tk.Entry(self, bd=5)

        b_appart.grid(row=0, column=1, sticky=tk.NS)
        b_house.grid(row=0, column=2, sticky=tk.NS)
        self.e_no.grid(row=1, column=2)
        self.e_namewall.grid(row=3, column=2)
        self.e_postalecode.grid(row=4, column=2)
        self.e_common.grid(row=5, column=2)
        self.e_areacovered.grid(row=6, column=2)
        self.e_areagarden.grid(row=7, column=2)
        self.e_numroom.grid(row=8, column=2)
        self.e_energyclass.grid(row=9, column=2)
        self.e_yearconstruct.grid(row=10, column=2)
        b_sell.grid(row=11, column=1)
        b_location.grid(row=11, column=2)
        self.cal.grid(row=12, column=2, padx=15)
        self.e_price.grid(row=13, column=2)
        tk.Button(self, text="Enregistrer", command=self.save_data).grid(row=14, column=2)

    # Probleme avec les radio button a verifier et
    def save_data(self):
        db = sqlite3.connect('gestion_immo.db')
        cur = db.cursor()
        if self.value_bien == 'Appartement' or 'Maison':
            bien = self.value_bien.get()
        else:
            return showerror('Erreur', 'Le bien selectionner retourne pas la bonne information. Veuillez fermer puis '
                                       'réouvrir.')
        try:
            no = int(self.e_no.get())
        except ValueError:
            return showerror('Erreur', 'Veuillez écrire un chiffre pour le n° de voie.')
        if self.listCombo.get() not in ["Rue", "Impasse", "Avenue", "Boulevard", "Allée", "Place"]:
            return showerror('Erreur', 'Veuillez selectionner la voie disponible dans la liste.')
        else:
            type_voie = self.listCombo.get()
        if len(self.e_namewall.get()) > 100:
            return showerror('Erreur', "L'adresse entré est trop long. Veuillez réessayer.")
        elif len(self.e_namewall.get()) == 0:
            return showerror('Erreur', "Veuillez entrer une adresse valide.")
        else:
            nom_rue = self.e_namewall.get()
        try:
            code_postale = int(self.e_postalecode.get())
            if len(self.e_postalecode.get()) != 5:
                raise ValueError
        except ValueError:
            return showerror('Erreur', 'Veuillez entrer un code postal valide.')

        if len(self.e_common.get()) > 40:
            return showerror('Erreur', 'Le nom de la commune est trop long. Veuillez réessayer.')
        elif len(self.e_common.get()) == 0:
            return showerror('Erreur', 'Veuillez entrer une commune valide.')
        else:
            commune = self.e_common.get()

        try:
            s_couvert = int(self.e_areacovered.get())
        except ValueError:
            return showerror('Erreur', 'Veuillez entrer des chiffres pour la superficie couverte.')

        if self.value_bien.get() == "Maison":
            try:
                s_jardin = int(self.e_areagarden.get())
            except ValueError:
                return showerror('Erreur', 'Veuillez entrer des chiffres pour la superficie du jardin.')

        try:
            nbre_piece = int(self.e_numroom.get())
        except ValueError:
            return showerror('Erreur', 'Veuillez entrer des chiffres pour le nombre de pièce.')

        if self.e_energyclass.get() not in ["A", "B", "C", "D", "E", "F", "G"]:
            return showerror("Erreur", "La classe energetique n'existe pas . Seul 'A', 'B', 'C', 'D', 'E', 'F', "
                                       "'G' sont acceptable.")
        else:
            c_enerie = self.e_energyclass.get()

        try:
            a_construction = int(self.e_yearconstruct.get())
        except ValueError:
            return showerror('Erreur', "Il y a une erreur sur l'année de construction. Veuillez réessayer.")
        if self.e_yearconstruct.get() is not None:
            if a_construction < 1900 or a_construction > datetime.now().year:
                return showerror('Erreur', "L'année doit être comprise entre 1900 et l'année actuelle.")

        if self.value_naturemana.get() == "Location" or self.value_naturemana.get() == "Achat":
            naturmana = self.value_naturemana.get()
        else:
            return showerror('Erreur', 'Veuillez selectionner soit un "Achat" ou une "Location".')

        try:
            date = self.cal.get_date()
            if date > date.today() or datetime.strptime(date, '%Y-%m-%d'):
                raise ValueError
        except ValueError:
            return showerror('Erreur', 'Il y a une erreur sur la date. Veuillez réessayer.')

        try:
            prix = int(self.e_price.get())
            if prix <= 0:
                raise ValueError
        except ValueError:
            return showerror('Erreur', 'Veuillez entrer des chiffres.')

        cur.execute("""INSERT INTO T_GESTIONIMMO(BIEN, NATURE_GESTION, NO, TYPE_VOIE, NOM_VOIE, 
                    CODE_POSTAL, COMMUNE, S_COUVERTE, S_JARDIN, NOMBRE_PIECE, CLASSE_ENERGETIQUE, ANNEE_CONSTRUCTION,
                    DATE_MISE_MARCHE, PRIX) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (bien, naturmana, no, type_voie,
                                                                                     nom_rue, code_postale, commune,
                                                                                     s_couvert, s_jardin, nbre_piece,
                                                                                     c_enerie, a_construction, date,
                                                                                     prix))
        db.commit()
        # self.refresh_db()
        db.close()
        # Clear the entry (à faire)
        return showinfo('Terminer', 'Le bien a été enregistré!')

    def enableEntryAreaGarden(self):
        self.e_areagarden.configure(state="normal")
        self.e_areagarden.update()

    def disableEntryAreaGarden(self):
        self.e_areagarden.configure(state="disabled")
        self.e_areagarden.update()


class PageMain(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        p_research = PageResearch(self)
        p_save = PageSave(self)
        b_exit = tk.Button(self, text="Fermer", command=self.quit)
        l_title = tk.Label(self, text="Gestion Immobilier", font=42)
        b_research = tk.Button(self, text="Recherche de biens", command=p_research.show)
        b_save = tk.Button(self, text="Enregistrement de biens", command=p_save.show)

        b_exit.pack()
        l_title.pack()
        b_research.pack()
        b_save.pack()


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p_main = PageMain(self)
        p_research = PageResearch(self)
        p_save = PageSave(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p_main.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p_research.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p_save.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Accueil", command=p_main.show)
        b2 = tk.Button(buttonframe, text="Recherche de biens", command=p_research.show)
        b3 = tk.Button(buttonframe, text="Enregistrement de biens", command=p_save.show)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p_main.show()


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("900x650")
    root.mainloop()
