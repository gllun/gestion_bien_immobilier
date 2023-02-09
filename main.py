import tkinter as tk
import sqlite3
from tkinter.messagebox import *
from tkcalendar import DateEntry
from tkinter import ttk
from tkinter import *
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
    conn.close()
except:
    showerror("Erreur", "Probleme avec la base de données. Contacter le support.")

# Creation Page Class
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()

    def character_limit(self, inp, limit):
        if inp == '' or (len(inp) <= limit and inp.isdigit()):
            return True
        return False

    def character_limit_str(self, inp_str, limit):
        if inp_str == '' or len(inp_str) <= limit:
            return True
        return False

# Page creation inheriting page class
class PageResearch(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        # Text default in the entry
        self.tdefault_e_search = "Commune"
        self.tdefault_e_areamin = "Surface min."
        self.tdefault_e_areamax = "Surface max."
        self.tdefault_e_nbpiecemin = "Nbre de piece min."
        self.tdefault_e_nbpiecemax = "Nbre de piece max."
        self.tdefault_e_yconstructionmin = "Annee de construction min."
        self.tdefault_e_yconstructionmax = "Annee de construction max."
        self.tdefault_e_pricemin = "Prix min."
        self.tdefault_e_pricemax = "Prix max."

        # All the critere for search with button validate
        self.checkb_appart = tk.IntVar(value=False)
        self.cb_appart = tk.Checkbutton(self, text="Appartement", variable=self.checkb_appart, onvalue=True,
                                        offvalue=False)
        self.cb_appart.grid(row=0, column=0)
        self.checkb_house = tk.IntVar(value=False)
        self.cb_house = tk.Checkbutton(self, text="Maison", variable=self.checkb_house,onvalue=True,
                                       offvalue=False)
        self.cb_house.grid(row=1, column=0)
        self.checkb_Location = tk.IntVar(value=False)
        self.cb_Location = tk.Checkbutton(self, text="Location", variable=self.checkb_Location, onvalue=True,
                                          offvalue=False)
        self.cb_Location.grid(row=2, column=0)
        self.checkb_Vente = tk.IntVar(value=False)
        self.cb_Vente = tk.Checkbutton(self, text="Vente", variable=self.checkb_Vente, onvalue=True, offvalue=False)
        self.cb_Vente.grid(row=3, column=0)

        self.e_search = tk.Entry(self, bd=5)
        self.e_search.grid(row=4, column=0)
        self.e_search.insert(0, self.tdefault_e_search)
        self.e_search.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_search, 'e_search'))
        self.e_search.bind("<FocusIn>", lambda event: self.click_allentry(self.e_search))
        self.e_search.configure(fg="gray", validate='key', validatecommand=(self.e_search.register(lambda inp_str: self.character_limit_str(inp_str, 40)), "%P"))

        self.e_areamin = tk.Entry(self, bd=5)
        self.e_areamin.grid(row=5, column=0)
        self.e_areamin.insert(0, self.tdefault_e_areamin)
        self.e_areamin.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_areamin, 'e_areamin'))
        self.e_areamin.bind("<FocusIn>", lambda event: self.click_allentry(self.e_areamin))
        self.e_areamin.configure(fg="gray", validate='key', validatecommand=(self.e_areamin.register(lambda inp: self.character_limit(inp, 5)), "%P"))

        self.e_areamax = tk.Entry(self, bd=5)
        self.e_areamax.grid(row=6, column=0)
        self.e_areamax.insert(0, self.tdefault_e_areamax)
        self.e_areamax.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_areamax, 'e_areamax'))
        self.e_areamax.bind("<FocusIn>", lambda event: self.click_allentry(self.e_areamax))
        self.e_areamax.configure(fg="gray", validate='key', validatecommand=(self.e_areamax.register(lambda inp: self.character_limit(inp, 5)), "%P"))

        self.e_nbpiecemin = tk.Entry(self, bd=5)
        self.e_nbpiecemin.grid(row=7, column=0)
        self.e_nbpiecemin.insert(0, self.tdefault_e_nbpiecemin)
        self.e_nbpiecemin.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_nbpiecemin, 'e_nbpiecemin'))
        self.e_nbpiecemin.bind("<FocusIn>", lambda event: self.click_allentry(self.e_nbpiecemin))
        self.e_nbpiecemin.configure(fg="gray", validate='key', validatecommand=(self.e_nbpiecemin.register(lambda inp: self.character_limit(inp, 3)), "%P"))

        self.e_nbpiecemax = tk.Entry(self, bd=5)
        self.e_nbpiecemax.grid(row=8, column=0)
        self.e_nbpiecemax.insert(0, self.tdefault_e_nbpiecemax)
        self.e_nbpiecemax.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_nbpiecemax, 'e_nbpiecemax'))
        self.e_nbpiecemax.bind("<FocusIn>", lambda event: self.click_allentry(self.e_nbpiecemax))
        self.e_nbpiecemax.configure(fg="gray", validate='key', validatecommand=(self.e_nbpiecemax.register(lambda inp: self.character_limit(inp, 3)), "%P"))

        self.e_yconstructionmin = tk.Entry(self, bd=5)
        self.e_yconstructionmin.grid(row=9, column=0)
        self.e_yconstructionmin.insert(0, self.tdefault_e_yconstructionmin)
        self.e_yconstructionmin.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_yconstructionmin, 'e_yconstructionmin'))
        self.e_yconstructionmin.bind("<FocusIn>", lambda event: self.click_allentry(self.e_yconstructionmin))
        self.e_yconstructionmin.configure(fg="gray", validate='key', validatecommand=(self.e_yconstructionmin.register(lambda inp: self.character_limit(inp, 4)), "%P"))

        self.e_yconstructionmax = tk.Entry(self, bd=5)
        self.e_yconstructionmax.grid(row=10, column=0)
        self.e_yconstructionmax.insert(0, self.tdefault_e_yconstructionmax)
        self.e_yconstructionmax.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_yconstructionmax, 'e_yconstructionmax'))
        self.e_yconstructionmax.bind("<FocusIn>", lambda event: self.click_allentry(self.e_yconstructionmax))
        self.e_yconstructionmax.configure(fg="gray", validate='key', validatecommand=(self.e_yconstructionmax.register(lambda inp: self.character_limit(inp, 4)), "%P"))

        self.e_pricemin = tk.Entry(self, bd=5)
        self.e_pricemin.grid(row=11, column=0)
        self.e_pricemin.insert(0, self.tdefault_e_pricemin)
        self.e_pricemin.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_pricemin, 'e_pricemin'))
        self.e_pricemin.bind("<FocusIn>", lambda event: self.click_allentry(self.e_pricemin))
        self.e_pricemin.configure(fg="gray", validate='key', validatecommand=(self.e_pricemin.register(lambda inp: self.character_limit(inp, 8)), "%P"))

        self.e_pricemax = tk.Entry(self, bd=5)
        self.e_pricemax.grid(row=12, column=0)
        self.e_pricemax.insert(0, self.tdefault_e_pricemax)
        self.e_pricemax.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_pricemax, 'e_pricemax'))
        self.e_pricemax.bind("<FocusIn>", lambda event: self.click_allentry(self.e_pricemax))
        self.e_pricemax.configure(fg="gray", validate='key', validatecommand=(self.e_pricemax.register(lambda inp: self.character_limit(inp, 8)), "%P"))

        self.liste_typeenergie = ["","A", "B", "C", "D", "E", "F","G"]
        self.listComboEnergy = ttk.Combobox(self, values= self.liste_typeenergie, state="readonly")
        self.listComboEnergy.grid(row=13, column=0)

        tk.Button(self, text="Recherche", command= self.search_data_critere).grid(row=15, column=0)

        # Display Data on Tkinter
        conn_r = sqlite3.connect('gestion_immo.db')
        curseur = conn_r.cursor()
        curseur.execute("SELECT * FROM T_GESTIONIMMO")
        self.result = curseur.fetchall()
        self.list_disdata = []
        i = 2
        j = 1
        for tuple_bien in self.result:
            self.l_bien = tk.Label(self, width=10, fg='blue', text=tuple_bien[j])
            self.l_bien.grid(row=i, column=j, padx=2)
            self.l_natureimmo = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 1])
            self.l_natureimmo.grid(row=i, column=j + 1, padx=2)
            self.l_cp = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 5])
            self.l_cp.grid(row=i, column=j + 2, padx=2)
            self.l_commune = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 6])
            self.l_commune.grid(row=i, column=j + 3, padx=2)
            self.l_areacouv = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 7])
            self.l_areacouv.grid(row=i, column=j + 4, padx=2)
            self.l_piece = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 9])
            self.l_piece.grid(row=i, column=j + 5, padx=2)
            self.l_cenergetique = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 10])
            self.l_cenergetique.grid(row=i, column=j + 6, padx=2)
            self.l_anneeconstruct = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 11])
            self.l_anneeconstruct.grid(row=i, column=j + 7, padx=2)
            self.l_prix = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 13])
            self.l_prix.grid(row=i, column=j + 8, padx=2)
            i += 1
            for col in range(9):
                list_label = eval(f"self.l_{['bien', 'natureimmo', 'cp', 'commune', 'areacouv', 'piece', 'cenergetique', 'anneeconstruct', 'prix'][col]}")
                self.list_disdata.append(list_label)
        conn_r.close()

    def refresh_db(self):
        for item in self.list_disdata:
            item.grid_remove()

        conn_r = sqlite3.connect('gestion_immo.db')
        curseur = conn_r.cursor()
        curseur.execute("SELECT * FROM T_GESTIONIMMO")
        self.result = curseur.fetchall()
        i = 1
        j = 1
        for tuple_bien in self.result:
            self.l_bien = tk.Label(self, width=10, fg='blue', text=tuple_bien[j])
            self.l_bien.grid(row=i, column=j, padx=2)
            self.l_natureimmo = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 1])
            self.l_natureimmo.grid(row=i, column=j + 1, padx=2)
            self.l_cp = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 5])
            self.l_cp.grid(row=i, column=j + 2, padx=2)
            self.l_commune = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 6])
            self.l_commune.grid(row=i, column=j + 3, padx=2)
            self.l_areacouv = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 7])
            self.l_areacouv.grid(row=i, column=j + 4, padx=2)
            self.l_piece = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 9])
            self.l_piece.grid(row=i, column=j + 5, padx=2)
            self.l_cenergetique = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 10])
            self.l_cenergetique.grid(row=i, column=j + 6, padx=2)
            self.l_anneeconstruct = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 11])
            self.l_anneeconstruct.grid(row=i, column=j + 7, padx=2)
            self.l_prix = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 13])
            self.l_prix.grid(row=i, column=j + 8, padx=2)
            i += 1
            for col in range(9):
                list_label = eval(f"self.l_{['bien', 'natureimmo', 'cp', 'commune', 'areacouv', 'piece', 'cenergetique', 'anneeconstruct', 'prix'][col]}")
                self.list_disdata.append(list_label)
        conn_r.close()

    def search_data_critere(self):
        # Delete data principal on the app
        for item in self.list_disdata:
            item.grid_remove()

        # Display data searchH
        search = self.e_search.get()
        cb_appart = self.checkb_appart.get()
        cb_maison = self.checkb_house.get()
        cb_location = self.checkb_Location.get()
        cb_vente = self.checkb_Vente.get()
        minarea = self.e_areamin.get()
        maxarea = self.e_areamax.get()
        minnbpiece = self.e_nbpiecemin.get()
        maxnbpiece = self.e_nbpiecemax.get()
        yearconstructionmin = self.e_yconstructionmin.get()
        yearconstructionmax = self.e_yconstructionmax.get()
        prixmin = self.e_pricemin.get()
        prixmax = self.e_pricemax.get()
        classeenergie = self.listComboEnergy.get()

        query = "SELECT * FROM T_GESTIONIMMO"
        if cb_appart or cb_maison or cb_location or cb_vente or search or minarea or maxarea or minnbpiece \
                or maxnbpiece or yearconstructionmin or yearconstructionmax or classeenergie or prixmin or prixmax:
                #or date_s:
            query += " WHERE"
        if cb_appart:
            query += " BIEN = 'Appartement' AND"
        if cb_maison:
            query += " BIEN = 'Maison' AND"
        if cb_location:
            query += " NATURE_GESTION = 'Location' AND"
        if cb_vente:
            query += " NATURE_GESTION = 'Vente' AND"
        if search and search != 'Commune':
            query += " COMMUNE LIKE '" + search.upper() + "%' AND"
        if minarea and minarea != 'Surface min.':
            query += " S_COUVERTE >= '" + minarea + "' AND"
        if maxarea and maxarea != 'Surface max.':
            query += " S_COUVERTE <= '" + maxarea + "' AND"
        if minnbpiece and minnbpiece != 'Nbre de piece min.':
            query += " NOMBRE_PIECE >= '" + minnbpiece + "' AND"
        if maxnbpiece and maxnbpiece != 'Nbre de piece max.':
            query += " NOMBRE_PIECE <= '" + maxnbpiece + "' AND"
        if yearconstructionmin and yearconstructionmin != 'Annee de construction min.':
            query += " ANNEE_CONSTRUCTION >= '" + yearconstructionmin + "' AND"
        if yearconstructionmax and yearconstructionmax != 'Annee de construction max.':
            query += " ANNEE_CONSTRUCTION <= '" + yearconstructionmax + "' AND"
        if classeenergie:
            query += " CLASSE_ENERGETIQUE = '" + classeenergie + "' AND"
        if prixmin and prixmin != 'Prix min.':
            query += " PRIX >= '" + prixmin + "' AND"
        if prixmax and prixmax != 'Prix max.':
            query += " PRIX <= '" + prixmax + "' AND"

        query = query.rstrip("AND")
        query = query.rstrip("WHERE")
        print(query)
        conn_r = sqlite3.connect('gestion_immo.db')
        curseur = conn_r.cursor()
        curseur.execute(query)
        self.result = curseur.fetchall()
        if len(self.result) == 0:
            notresult = tk.Label(self, width=15, fg='black', text='Aucun Resultat', font=("Bold", 30))
            notresult.grid(row=2, column=1)
            self.list_disdata.append(notresult)
        else:
            i = 2
            j = 1
            for tuple_bien in self.result:
                self.l_bien = tk.Label(self, width=10, fg='blue', text=tuple_bien[j])
                self.l_bien.grid(row=i, column=j, padx=2)
                self.l_natureimmo = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 1])
                self.l_natureimmo.grid(row=i, column=j + 1, padx=2)
                self.l_cp = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 5])
                self.l_cp.grid(row=i, column=j + 2, padx=2)
                self.l_commune = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 6])
                self.l_commune.grid(row=i, column=j + 3, padx=2)
                self.l_areacouv = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 7])
                self.l_areacouv.grid(row=i, column=j + 4, padx=2)
                self.l_piece = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 9])
                self.l_piece.grid(row=i, column=j + 5, padx=2)
                self.l_cenergetique = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 10])
                self.l_cenergetique.grid(row=i, column=j + 6, padx=2)
                self.l_anneeconstruct = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 11])
                self.l_anneeconstruct.grid(row=i, column=j + 7, padx=2)
                self.l_prix = tk.Label(self, width=10, fg='blue', text=tuple_bien[j + 13])
                self.l_prix.grid(row=i, column=j + 8, padx=2)
                for col in range(9):
                    list_label = eval(f"self.l_{['bien', 'natureimmo', 'cp', 'commune', 'areacouv', 'piece', 'cenergetique', 'anneeconstruct', 'prix'][col]}")
                    self.list_disdata.append(list_label)
                i += 1
        conn_r.close()

    def reset_allentry(self, event_resetentry, txt):
        entry_str = f"self.tdefault_{txt}"
        entry_default = eval(entry_str)
        if event_resetentry.get() == '':
            event_resetentry.delete(0, END)
            event_resetentry.insert(0, entry_default)
            event_resetentry.configure(fg="gray")

    def click_allentry(self, event_clickentry):
        if event_clickentry.get() == 'Surface min.' or 'Commune' or 'Surface max.' or 'Nbre de piece min.' or 'Nbre de piece max.' or 'Annee de construction min.' or 'Annee de construction max.' or 'Prix min.' or 'Prix max.':
            event_clickentry.delete(0, END)
            event_clickentry.insert(0, '')
            event_clickentry.configure(fg="black")

# Class Enregistrement des données d'un bien
class PageSave(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.researchpage = PageResearch()
        self.columnconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)

        self.value_bien = tk.StringVar(None, "VB")
        b_appart = tk.Radiobutton(self, text="Appartement", variable=self.value_bien, value='Appartement',
                                  command=self.disableEntryAreaGarden)
        b_house = tk.Radiobutton(self, text="Maison", variable=self.value_bien, value='Maison',
                                 command=self.enableEntryAreaGarden)
        tk.Label(self, text="N°").grid(row=1, column=1)
        self.e_no = tk.Entry(self, bd=5)
        self.e_no.config(validate='key', validatecommand=(self.e_no.register(lambda inp: self.character_limit(inp, 5)), "%P"))

        tk.Label(self, text="Type de voie : ").grid(row=2, column=1)
        self.liste_typewall = ["Rue", "Impasse", "Avenue", "Boulevard", "Allée", "Place"]
        self.listCombo = ttk.Combobox(self, values=self.liste_typewall, state="readonly")
        self.listCombo.grid(row=2, column=2)

        tk.Label(self, text="Nom de rue : ").grid(row=3, column=1)
        self.e_namewall = tk.Entry(self, bd=5)
        self.e_namewall.config(validate='key', validatecommand=(self.e_namewall.register(lambda inp_str: self.character_limit_str(inp_str, 100)), "%P"))
        tk.Label(self, text="Code Postale : ").grid(row=4, column=1)
        self.e_postalecode = tk.Entry(self, bd=5)
        self.e_postalecode.config(validate='key', validatecommand=(self.e_postalecode.register(lambda inp: self.character_limit(inp, 5)), "%P"))
        tk.Label(self, text="Commune :").grid(row=5, column=1)
        self.e_common = tk.Entry(self, bd=5)
        self.e_common.config(validate='key', validatecommand=(self.e_common.register(lambda inp_str: self.character_limit_str(inp_str, 40)), "%P"))
        tk.Label(self, text="Superficie couvert : ").grid(row=6, column=1)
        self.e_areacovered = tk.Entry(self, bd=5)
        self.e_areacovered.config(validate='key', validatecommand=(self.e_areacovered.register(lambda inp: self.character_limit(inp, 5)), "%P"))
        tk.Label(self, text="Superficie jardin : ").grid(row=7, column=1)
        self.e_areagarden = tk.Entry(self, bd=5)
        self.e_areagarden.config(validate='key', validatecommand=(self.e_areagarden.register(lambda inp: self.character_limit(inp, 5)), "%P"))
        tk.Label(self, text="Nombre de pièce : ").grid(row=8, column=1)
        self.e_numroom = tk.Entry(self, bd=5)
        self.e_numroom.config(validate='key', validatecommand=(self.e_numroom.register(lambda inp: self.character_limit(inp, 3)), "%P"))
        tk.Label(self, text="Classe énergétique : ").grid(row=9, column=1)
        self.liste_typeenergie = ["", "A", "B", "C", "D", "E", "F", "G"]
        self.listComboEnergy = ttk.Combobox(self, values=self.liste_typeenergie, state="readonly")


        tk.Label(self, text="Année de construction : ").grid(row=10, column=1)
        self.e_yearconstruct = tk.Entry(self, bd=5)
        self.e_yearconstruct.config(validate='key', validatecommand=(self.e_yearconstruct.register(lambda inp: self.character_limit(inp, 4)), "%P"))
        self.value_naturemana = tk.StringVar(None, "VN")
        b_sell = tk.Radiobutton(self, text="Vente", variable=self.value_naturemana, value='Vente')
        b_location = tk.Radiobutton(self, text="Location", variable=self.value_naturemana, value='Location')
        tk.Label(self, text="Date de mise en marche").grid(row=12, column=1)
        self.cal = DateEntry(self, selectmode='day', date_pattern='dd/mm/yyyy')
        tk.Label(self, text="Prix").grid(row=13, column=1)
        self.e_price = tk.Entry(self, bd=5)
        self.e_price.config(validate='key', validatecommand=(self.e_price.register(lambda inp: self.character_limit(inp, 8)), "%P"))

        b_appart.grid(row=0, column=1, sticky=tk.NS)
        b_house.grid(row=0, column=2, sticky=tk.NS)
        self.value_bien.set("VB")
        self.e_no.grid(row=1, column=2)
        self.e_namewall.grid(row=3, column=2)
        self.e_postalecode.grid(row=4, column=2)
        self.e_common.grid(row=5, column=2)
        self.e_areacovered.grid(row=6, column=2)
        self.e_areagarden.grid(row=7, column=2)
        self.e_numroom.grid(row=8, column=2)
        self.listComboEnergy.grid(row=9, column=2)
        self.e_yearconstruct.grid(row=10, column=2)
        b_sell.grid(row=11, column=1)
        b_location.grid(row=11, column=2)
        self.value_bien.set("VN")
        self.cal.grid(row=12, column=2, padx=15)
        self.e_price.grid(row=13, column=2)
        tk.Button(self, text="Enregistrer", command=self.save_data).grid(row=14, column=2)

    def save_data(self):
        db = sqlite3.connect('gestion_immo.db')

        if self.value_bien.get() not in ['Appartement', 'Maison']:
            return showerror('Erreur', 'Veuillez selectionner soit un "Appartement" ou une "Maison".')
        else:
            bien = self.value_bien.get()

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

        s_jardin = None
        if self.value_bien.get() in 'Maison' and self.e_areagarden.get().isnumeric():
            s_jardin = self.e_areagarden.get()
        elif self.value_bien.get() in 'Maison' and self.e_areagarden.get().isnumeric() != True:
            return showerror('Erreur', 'Veuillez entrer des chiffres pour la superficie du jardin.')

        try:
            nbre_piece = int(self.e_numroom.get())
        except ValueError:
            return showerror('Erreur', 'Veuillez entrer des chiffres pour le nombre de pièce.')

        if self.listComboEnergy.get() not in ["A", "B", "C", "D", "E", "F", "G"]:
            return showerror("Erreur", "La classe energetique n'existe pas . Seul 'A', 'B', 'C', 'D', 'E', 'F', "
                                       "'G' sont acceptable.")
        else:
            c_energie = self.listComboEnergy.get()

        try:
            a_construction = int(self.e_yearconstruct.get())
        except ValueError:
            return showerror('Erreur', "Il y a une erreur sur l'année de construction. Veuillez réessayer.")
        if self.e_yearconstruct.get() is not None:
            if a_construction < 1900 or a_construction > datetime.now().year:
                return showerror('Erreur', "L'année doit être comprise entre 1900 et l'année actuelle.")

        if self.value_naturemana.get() not in ["Location", "Vente"]:
            return showerror('Erreur', 'Veuillez selectionner soit une "Location" ou une "Vente".')
        else:
            naturmana = self.value_naturemana.get()

        try:
            date = self.cal.get()
            datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            return showerror('Erreur', 'Il y a une erreur sur la date. Veuillez réessayer.')

        try:
            prix = int(self.e_price.get())
            if prix <= 0:
                raise ValueError
        except ValueError:
            return showerror('Erreur', 'Veuillez entrer des chiffres.')

        cur = db.cursor()
        cur.execute("""INSERT INTO T_GESTIONIMMO(BIEN, NATURE_GESTION, NO, TYPE_VOIE, NOM_VOIE, 
                    CODE_POSTAL, COMMUNE, S_COUVERTE, S_JARDIN, NOMBRE_PIECE, CLASSE_ENERGETIQUE, ANNEE_CONSTRUCTION,
                    DATE_MISE_MARCHE, PRIX) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (bien, naturmana, no, type_voie,
                                                                                     nom_rue, code_postale, commune,
                                                                                     s_couvert, s_jardin, nbre_piece,
                                                                                     c_energie, a_construction, date,
                                                                                     prix))
        db.commit()
        db.close()
        self.researchpage.refresh_db()

        # Clear the entry
        self.value_bien.set("VB")
        self.value_naturemana.set("VN")
        self.listComboEnergy.set('')
        self.listCombo.set('')
        today = datetime.now().date()
        self.cal.set_date(today)
        list_data = [self.e_no, self.e_namewall, self.e_postalecode, self.e_common, self.e_areacovered, self.e_areagarden,
         self.e_numroom, self.e_price, self.e_yearconstruct]

        for item in list_data :
            item.delete(0, END)
            item.insert(0, '')

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
    root.wm_geometry("1000x650")
    root.mainloop()
