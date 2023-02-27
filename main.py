import tkinter as tk
import sqlite3
from tkinter.messagebox import *
from tkcalendar import DateEntry
from tkinter import ttk
from tkinter import *
from datetime import datetime
from tkinter import Canvas
from PIL import Image, ImageTk

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
        self.notresult = None
        self.canvas = Canvas(self, bg="#FFFFFF", height=770, width=1450, bd=0, highlightthickness=0, relief="ridge")

        self.canvas.place(x=0, y=0)

        #Charge img         
        self.img_house = Image.open(
            "../gestion_bien_immobilier-master/house.jpg")
        self.img_house = self.img_house.resize((239, 150), Image.ANTIALIAS)
        self.img_house = ImageTk.PhotoImage(self.img_house)

        self.img_building = Image.open(
            "../gestion_bien_immobilier-master/building.jpg")
        self.img_building = self.img_building.resize((239, 150), Image.ANTIALIAS)
        self.img_building = ImageTk.PhotoImage(self.img_building)

        self.canvas.create_rectangle(
            0.0,
            28.0,
            1450.0,  # PARTI COULEUR DU CORPS DU TEXTE
            1052.0,
            fill="#6FCF97",
            outline="")

        self.canvas.create_rectangle(0, 0, 480, 119, fill="#219653", outline="", tags="rec_main")
        self.canvas.create_text(230.00, 55.00, text="Accueil", font=("Ink Free", '22'), tags="rec_main")
        # self.canvas.tag_bind("rec_main", "<Button-1>", self.show_main)

        self.canvas.create_rectangle(480, 0, 960, 119, fill="#27AE60", outline="", tags="rec_save")
        self.canvas.create_text(715.00, 55.00, text="Enregistrement de bien", font=("Ink Free", '22'), tags="rec_save")
        # self.canvas.tag_bind("rec_save", "<Button-1>", self.show_save)

        self.canvas.create_rectangle(960, 0, 1450, 119, fill="#6FCF97", outline="", tags="rec_research")
        self.canvas.create_text(1200, 55, text="Recherche de bien", font=("Ink Free", '22'), tags="rec_research")
        # self.canvas.tag_bind("rec_research", "<Button-1>", self.show_research)

        self.canvas.create_rectangle(230, 770, 0, 119, fill="#5EBD85", outline="")

        # Display Data on Tkinter
        conn_r = sqlite3.connect('gestion_immo.db')
        curseur = conn_r.cursor()
        curseur.execute("SELECT * FROM T_GESTIONIMMO")
        self.result = curseur.fetchall()
        self.list_disdata = []

        if len(self.result) == 0:
            self.notresult = self.canvas.create_text(530, 220, text="Aucun Résultat",
                                                      font=("Lobster", '36'))
            self.list_disdata.append(self.notresult)
        else:
            j = 1
        b_rec = 150
        d_rec = 430
        a_rec = 300
        c_rec = 540
        img_x = 420
        img_y = 226
        txt_x = 480
        txt_y = 410
        nb_row = 1
        for tuple_bien in self.result:
            self.l_rec = self.canvas.create_rectangle(a_rec, b_rec, c_rec, d_rec, fill="")
            if tuple_bien[1] == "Maison":
                self.l_img = self.canvas.create_image(img_x, img_y, image=self.img_house)
            elif tuple_bien[1] == "Appartement":
                self.l_img = self.canvas.create_image(img_x, img_y, image=self.img_building)
            self.l_bien = self.canvas.create_text(txt_x-125, txt_y-90, text=tuple_bien[j], font=("Lobster", '12'))  # L1
            self.l_commune = self.canvas.create_text(txt_x, txt_y-90, text=tuple_bien[j + 6], font=("Lobster", '12'))  # L1
            self.l_areacouv = self.canvas.create_text(txt_x-140, txt_y-60, text=tuple_bien[j + 7], font=("Lobster", '12'))  # L2
            self.l_piece = self.canvas.create_text(txt_x, txt_y-60, text=tuple_bien[j + 9], font=("Lobster", '12'))  # L2
            self.l_cenergetique = self.canvas.create_text(txt_x-128, txt_y-30, text="Classe E. : "+ tuple_bien[j + 10], font=("Lobster", '12'))  # L3
            self.l_anneeconstruct = self.canvas.create_text(txt_x, txt_y-30, text=tuple_bien[j + 11], font=("Lobster", '12'))  # L3
            self.l_natureimmo = self.canvas.create_text(txt_x-138, txt_y, text=tuple_bien[j + 1], font=("Lobster", '12'))  # L4
            self.l_prix = self.canvas.create_text(txt_x, txt_y, text=tuple_bien[j + 13], font=("Lobster", '12'))  # L4
            a_rec += 270
            c_rec += 270
            img_x += 270
            txt_x += 270
            if nb_row == 4:
                b_rec += 310
                d_rec += 310
                img_x = 420
                img_y += 310
                txt_x = 480
                txt_y += 310
                a_rec = 300
                c_rec = 540
                nb_row = 1
            else:
                nb_row += 1

            for col in range(10):
                list_label = eval(
                    f"self.l_{['rec','img','bien', 'natureimmo', 'commune', 'areacouv', 'piece', 'cenergetique', 'anneeconstruct', 'prix',][col]}")
                self.list_disdata.append(list_label)
        conn_r.close()

        # Text default in the entry
        self.tdefault_e_search = "Entrer Ville"
        self.tdefault_e_areamin = "Min"
        self.tdefault_e_areamax = "Max"
        self.tdefault_e_nbpiecemin = "Min"
        self.tdefault_e_nbpiecemax = "Max"
        self.tdefault_e_yconstructionmin = "Min"
        self.tdefault_e_yconstructionmax = "Max"
        self.tdefault_e_pricemin = "Min"
        self.tdefault_e_pricemax = "Max"

        # All the critere for search with button validate
        self.checkb_appart = tk.IntVar(value=False)
        self.cb_appart = tk.Checkbutton(self, text="Appartement", variable=self.checkb_appart, onvalue=True, offvalue=False, 	
bg='#5EBD85',activebackground='#5EBD85',font=('Arial', 13))
        self.cb_appart.place(x=10, y=230)
        self.checkb_house = tk.IntVar(value=False)  
        self.cb_house = tk.Checkbutton(self, text="Maison", variable=self.checkb_house,onvalue=True, offvalue=False, 	
bg='#5EBD85',activebackground='#5EBD85',font=('Arial', 13))
        self.cb_house.place(x=140, y=230)
        self.checkb_Location = tk.IntVar(value=False)
        self.cb_Location = tk.Checkbutton(self, text="Location", variable=self.checkb_Location, onvalue=True, offvalue=False, 	
bg='#5EBD85',activebackground='#5EBD85',font=('Arial', 13))
        self.cb_Location.place(x=10, y=260)
        self.checkb_Vente = tk.IntVar(value=False)

        self.cb_Vente = tk.Checkbutton(self, text="Vente", variable=self.checkb_Vente, onvalue=True, offvalue=False, 	
bg='#5EBD85',activebackground='#5EBD85',font=('Arial', 13))
        self.cb_Vente.place(x=140, y=260)   

        self.frame_recherche = tk.Frame(self, bg='#54AA77')
        self.frame_recherche.place(x=0, y=119,width=230,height=100)    

        # LABELS       

        self.label_ville = tk.Label(self, text="Recherche", font=('Ink Free', 19), fg="white", bg='#54AA77')
        self.label_ville.place(x=60, y=152) 
        self.label_ville = tk.Label(self, text="Ville", font=('Arial', 11), fg="black", bg='#5EBD85')
        self.label_ville.place(x=13, y=293)

            
        self.label_ville = tk.Label(self, text="Surface", font=('Arial', 11), fg="black", bg='#5EBD85')
        self.label_ville.place(x=13, y=353)
        
        self.label_ville = tk.Label(self, text="Nombre de pièces", font=('Arial', 11), fg="black", bg='#5EBD85')
        self.label_ville.place(x=13, y=413)

        self.label_ville = tk.Label(self, text="Année de construction", font=('Arial', 11), fg="black", bg='#5EBD85')
        self.label_ville.place(x=13, y=473)

        self.label_ville = tk.Label(self, text="Prix", font=('Arial', 11), fg="black", bg='#5EBD85')
        self.label_ville.place(x=13, y=533)

        self.label_ville = tk.Label(self, text="Classe énergetique", font=('Arial', 11), fg="black", bg='#5EBD85')
        self.label_ville.place(x=13, y=593)

        self.e_search = tk.Entry(self, bd=0)
        self.e_search.place(x=13, y=313, height=40, width=200)
        self.e_search.insert(0, self.tdefault_e_search)
        self.e_search.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_search, 'e_search'))
        self.e_search.bind("<FocusIn>", lambda event: self.click_allentry(self.e_search))
        self.e_search.configure(bd=3,font=('Arial', 11),width=27,fg="gray", validate='key', validatecommand=(self.e_search.register(lambda inp_str: self.character_limit_str(inp_str, 40)), "%P"))
        
        self.e_areamin = tk.Entry(self, bd=5)
        self.e_areamin.place(x=13, y=373, height=40, width=90)
        self.e_areamin.insert(0, self.tdefault_e_areamin)
        self.e_areamin.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_areamin, 'e_areamin'))
        self.e_areamin.bind("<FocusIn>", lambda event: self.click_allentry(self.e_areamin))
        self.e_areamin.configure(bd=3,font=('Arial', 11),width=27,fg="gray", validate='key', validatecommand=(self.e_areamin.register(lambda inp: self.character_limit(inp, 5)), "%P"))

        self.e_areamax = tk.Entry(self, bd=5)
        self.e_areamax.place(x=122, y=373, height=40, width=90)
        self.e_areamax.insert(0, self.tdefault_e_areamax)
        self.e_areamax.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_areamax, 'e_areamax'))
        self.e_areamax.bind("<FocusIn>", lambda event: self.click_allentry(self.e_areamax))
        self.e_areamax.configure(bd=3,font=('Arial', 11),width=27,fg="gray", validate='key', validatecommand=(self.e_areamax.register(lambda inp: self.character_limit(inp, 5)), "%P"))

        self.e_nbpiecemin = tk.Entry(self, bd=5)
        self.e_nbpiecemin.place(x=13, y=433, height=40, width=90)
        self.e_nbpiecemin.insert(0, self.tdefault_e_nbpiecemin)
        self.e_nbpiecemin.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_nbpiecemin, 'e_nbpiecemin'))
        self.e_nbpiecemin.bind("<FocusIn>", lambda event: self.click_allentry(self.e_nbpiecemin))
        self.e_nbpiecemin.configure(bd=3,font=('Arial', 11),width=27,fg="gray", validate='key', validatecommand=(self.e_nbpiecemin.register(lambda inp: self.character_limit(inp, 3)), "%P"))

        self.e_nbpiecemax = tk.Entry(self, bd=5)
        self.e_nbpiecemax.place(x=122, y=433, height=40, width=90)
        self.e_nbpiecemax.insert(0, self.tdefault_e_nbpiecemax)
        self.e_nbpiecemax.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_nbpiecemax, 'e_nbpiecemax'))
        self.e_nbpiecemax.bind("<FocusIn>", lambda event: self.click_allentry(self.e_nbpiecemax))
        self.e_nbpiecemax.configure(bd=3,font=('Arial', 11),width=27,fg="gray", validate='key', validatecommand=(self.e_nbpiecemax.register(lambda inp: self.character_limit(inp, 3)), "%P"))

        self.e_yconstructionmin = tk.Entry(self, bd=5)
        self.e_yconstructionmin.place(x=13, y=493, height=40, width=90)
        self.e_yconstructionmin.insert(0, self.tdefault_e_yconstructionmin)
        self.e_yconstructionmin.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_yconstructionmin, 'e_yconstructionmin'))
        self.e_yconstructionmin.bind("<FocusIn>", lambda event: self.click_allentry(self.e_yconstructionmin))
        self.e_yconstructionmin.configure(bd=3,font=('Arial', 11),width=27,fg="gray", validate='key', validatecommand=(self.e_yconstructionmin.register(lambda inp: self.character_limit(inp, 4)), "%P"))

        self.e_yconstructionmax = tk.Entry(self, bd=5)
        self.e_yconstructionmax.place(x=122, y=493, height=40, width=90)
        self.e_yconstructionmax.insert(0, self.tdefault_e_yconstructionmax)
        self.e_yconstructionmax.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_yconstructionmax, 'e_yconstructionmax'))
        self.e_yconstructionmax.bind("<FocusIn>", lambda event: self.click_allentry(self.e_yconstructionmax))
        self.e_yconstructionmax.configure(bd=3,font=('Arial', 11),width=27,fg="gray", validate='key', validatecommand=(self.e_yconstructionmax.register(lambda inp: self.character_limit(inp, 4)), "%P"))

        self.e_pricemin = tk.Entry(self, bd=5)
        self.e_pricemin.place(x=13, y=553, height=40, width=90)
        self.e_pricemin.insert(0, self.tdefault_e_pricemin)
        self.e_pricemin.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_pricemin, 'e_pricemin'))
        self.e_pricemin.bind("<FocusIn>", lambda event: self.click_allentry(self.e_pricemin))
        self.e_pricemin.configure(bd=3,font=('Arial', 11),width=27,fg="gray", validate='key', validatecommand=(self.e_pricemin.register(lambda inp: self.character_limit(inp, 8)), "%P"))

        self.e_pricemax = tk.Entry(self, bd=5)
        self.e_pricemax.place(x=122, y=553, height=40, width=90)
        self.e_pricemax.insert(0, self.tdefault_e_pricemax)
        self.e_pricemax.bind("<FocusOut>", lambda event: self.reset_allentry(self.e_pricemax, 'e_pricemax'))
        self.e_pricemax.bind("<FocusIn>", lambda event: self.click_allentry(self.e_pricemax))
        self.e_pricemax.configure(bd=3,font=('Arial', 11),width=27,fg="gray", validate='key', validatecommand=(self.e_pricemax.register(lambda inp: self.character_limit(inp, 8)), "%P"))

        self.liste_typeenergie = ["","A", "B", "C", "D", "E", "F","G"]
        self.listComboEnergy = ttk.Combobox(self, values= self.liste_typeenergie, state="readonly")
        self.listComboEnergy.place(x=13, y=620,width=200)

        tk.Button(self, text="Chercher", command= self.search_data_critere).place(x=67, y=670,height=45,width=90)

    def refresh_db(self):
        # Delete data principal on the app
        for item in self.list_disdata:
            self.canvas.delete(item)

        conn_r = sqlite3.connect('gestion_immo.db')
        curseur = conn_r.cursor()
        curseur.execute("SELECT * FROM T_GESTIONIMMO")
        self.result = curseur.fetchall()
        
        if len(self.result) == 0:
            self.notresult = self.canvas.create_text(530, 220, text="Aucun Résultat",
                                                      font=("Lobster", '36'))
            self.list_disdata.append(self.notresult)
        else:
            j = 1
        b_rec = 150
        d_rec = 430
        a_rec = 300
        c_rec = 540
        img_x = 420
        img_y = 226
        txt_x = 480
        txt_y = 410
        nb_row = 1
        for tuple_bien in self.result:
            self.l_rec = self.canvas.create_rectangle(a_rec, b_rec, c_rec, d_rec, fill="")
            if tuple_bien[1] == "Maison":
                self.l_img = self.canvas.create_image(img_x, img_y, image=self.img_house)
            elif tuple_bien[1] == "Appartement":
                self.l_img = self.canvas.create_image(img_x, img_y, image=self.img_building)
            self.l_bien = self.canvas.create_text(txt_x-125, txt_y-90, text=tuple_bien[j], font=("Lobster", '12'))  # L1
            self.l_commune = self.canvas.create_text(txt_x, txt_y-90, text=tuple_bien[j + 6], font=("Lobster", '12'))  # L1
            self.l_areacouv = self.canvas.create_text(txt_x-140, txt_y-60, text=tuple_bien[j + 7], font=("Lobster", '12'))  # L2
            self.l_piece = self.canvas.create_text(txt_x, txt_y-60, text=tuple_bien[j + 9], font=("Lobster", '12'))  # L2
            self.l_cenergetique = self.canvas.create_text(txt_x-128, txt_y-30, text="Classe E. : "+ tuple_bien[j + 10], font=("Lobster", '12'))  # L3
            self.l_anneeconstruct = self.canvas.create_text(txt_x, txt_y-30, text=tuple_bien[j + 11], font=("Lobster", '12'))  # L3
            self.l_natureimmo = self.canvas.create_text(txt_x-138, txt_y, text=tuple_bien[j + 1], font=("Lobster", '12'))  # L4
            self.l_prix = self.canvas.create_text(txt_x, txt_y, text=tuple_bien[j + 13], font=("Lobster", '12'))  # L4
            a_rec += 270
            c_rec += 270
            img_x += 270
            txt_x += 270
            if nb_row == 4:
                b_rec += 310
                d_rec += 310
                img_x = 420
                img_y += 310
                txt_x = 480
                txt_y += 310
                a_rec = 300
                c_rec = 540
                nb_row = 1
            else:
                nb_row += 1

            for col in range(10):
                list_label = eval(
                    f"self.l_{['rec','img','bien', 'natureimmo', 'commune', 'areacouv', 'piece', 'cenergetique', 'anneeconstruct', 'prix',][col]}")
                self.list_disdata.append(list_label)
        conn_r.close()

    def search_data_critere(self):
        # Delete data principal on the app
        for item in self.list_disdata:
            self.canvas.delete(item)


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
        if search and search != 'Entrer Ville':
            query += " COMMUNE LIKE '" + search.upper() + "%' AND"
        if minarea and minarea != 'Min':
            query += " S_COUVERTE >= '" + minarea + "' AND"
        if maxarea and maxarea != 'Max':
            query += " S_COUVERTE <= '" + maxarea + "' AND"
        if minnbpiece and minnbpiece != 'Min':
            query += " NOMBRE_PIECE >= '" + minnbpiece + "' AND"
        if maxnbpiece and maxnbpiece != 'Max':
            query += " NOMBRE_PIECE <= '" + maxnbpiece + "' AND"
        if yearconstructionmin and yearconstructionmin != 'Min':
            query += " ANNEE_CONSTRUCTION >= '" + yearconstructionmin + "' AND"
        if yearconstructionmax and yearconstructionmax != 'Max':
            query += " ANNEE_CONSTRUCTION <= '" + yearconstructionmax + "' AND"
        if classeenergie:
            query += " CLASSE_ENERGETIQUE = '" + classeenergie + "' AND"
        if prixmin and prixmin != 'Min':
            query += " PRIX >= '" + prixmin + "' AND"
        if prixmax and prixmax != 'Max':
            query += " PRIX <= '" + prixmax + "' AND"

        query = query.rstrip("AND")
        query = query.rstrip("WHERE")
        print(query)
        conn_r = sqlite3.connect('gestion_immo.db')
        curseur = conn_r.cursor()
        curseur.execute(query)
        self.result = curseur.fetchall()
        if len(self.result) == 0:
            self.notresult = self.canvas.create_text(530, 220, text="Aucun Résultat",
                                                      font=("Lobster", '36'))
            self.list_disdata.append(self.notresult)
        else:
            j = 1
        b_rec = 150
        d_rec = 430
        a_rec = 300
        c_rec = 540
        img_x = 420
        img_y = 226
        txt_x = 480
        txt_y = 410
        nb_row = 1
        for tuple_bien in self.result:
            self.l_rec = self.canvas.create_rectangle(a_rec, b_rec, c_rec, d_rec, fill="")
            if tuple_bien[1] == "Maison":
                self.l_img = self.canvas.create_image(img_x, img_y, image=self.img_house)
            elif tuple_bien[1] == "Appartement":
                self.l_img = self.canvas.create_image(img_x, img_y, image=self.img_building)
            self.l_bien = self.canvas.create_text(txt_x-125, txt_y-90, text=tuple_bien[j], font=("Lobster", '12'))  # L1
            self.l_commune = self.canvas.create_text(txt_x, txt_y-90, text=tuple_bien[j + 6], font=("Lobster", '12'))  # L1
            self.l_areacouv = self.canvas.create_text(txt_x-140, txt_y-60, text=tuple_bien[j + 7], font=("Lobster", '12'))  # L2
            self.l_piece = self.canvas.create_text(txt_x, txt_y-60, text=tuple_bien[j + 9], font=("Lobster", '12'))  # L2
            self.l_cenergetique = self.canvas.create_text(txt_x-128, txt_y-30, text="Classe E. : "+ tuple_bien[j + 10], font=("Lobster", '12'))  # L3
            self.l_anneeconstruct = self.canvas.create_text(txt_x, txt_y-30, text=tuple_bien[j + 11], font=("Lobster", '12'))  # L3
            self.l_natureimmo = self.canvas.create_text(txt_x-138, txt_y, text=tuple_bien[j + 1], font=("Lobster", '12'))  # L4
            self.l_prix = self.canvas.create_text(txt_x, txt_y, text=tuple_bien[j + 13], font=("Lobster", '12'))  # L4
            a_rec += 270
            c_rec += 270
            img_x += 270
            txt_x += 270
            if nb_row == 4:
                b_rec += 310
                d_rec += 310
                img_x = 420
                img_y += 310
                txt_x = 480
                txt_y += 310
                a_rec = 300
                c_rec = 540
                nb_row = 1
            else:
                nb_row += 1

            for col in range(10):
                list_label = eval(
                    f"self.l_{['rec','img','bien', 'natureimmo', 'commune', 'areacouv', 'piece', 'cenergetique', 'anneeconstruct', 'prix',][col]}")
                self.list_disdata.append(list_label)
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

        self.canvas = Canvas(self, bg="#FFFFFF", height=770, width=1450, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.researchpage = PageResearch()
        self.columnconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)

        self.canvas.create_rectangle(
            0.0,
            28.0,
            1450.0,  # PARTIE COULEUR DU CORPS
            1052.0,
            fill="#27AE60",
            outline="")


        self.canvas.create_rectangle(0, 0, 480, 119, fill="#219653", outline="", tags="rec_main")
        self.canvas.create_text(230.00, 55.00, text="Accueil", font=("Ink Free", '22'), tags="rec_main")
        self.canvas.tag_bind("rec_main", "<Button-1>", MainView.show_main)

        self.canvas.create_rectangle(480, 0, 960, 119, fill="#27AE60", outline="", tags="rec_save")
        self.canvas.create_text(715.00, 55.00, text="Enregistrement de bien", font=("Ink Free", '22'), tags="rec_save")
        self.canvas.tag_bind("rec_save", "<Button-1>", MainView.show_save)

        self.canvas.create_rectangle(960, 0, 1450, 119, fill="#6FCF97", outline="", tags="rec_research")
        self.canvas.create_text(1200, 55, text="Recherche de bien", font=("Ink Free", '22'), tags="rec_research")
        self.canvas.tag_bind("rec_research", "<Button-1>", MainView.show_research)

        self.value_bien = tk.StringVar(None, "VB")
        b_appart = tk.Radiobutton(self, text="Appartement", variable=self.value_bien, value='Appartement',
                                  command=self.disableEntryAreaGarden,bg='#27ae60',activebackground='#27ae60',font=('Arial', 13)).place(x=600,y=220)
        b_house = tk.Radiobutton(self, text="Maison", variable=self.value_bien, value='Maison',
                                 command=self.enableEntryAreaGarden,bg='#27ae60',activebackground='#27ae60',font=('Arial', 13)).place(x=750,y=220)
        tk.Label(self, text="N° :", font=('Arial', 11), fg="black", bg='#27ae60').place(x=570,y=260)
        self.e_no = tk.Entry(self, bd=3,font=('Arial', 11),width=29,fg="gray")
        self.e_no.config(validate='key', validatecommand=(self.e_no.register(lambda inp: self.character_limit(inp, 5)), "%P"))

        tk.Label(self, text="Type de voie : ", font=('Arial', 11), fg="black", bg='#27ae60').place(x=503,y=290)
        self.liste_typewall = ["Rue", "Impasse", "Avenue", "Boulevard", "Allée", "Place"]
        self.listCombo = ttk.Combobox(self, values=self.liste_typewall, state="readonly")
        self.listCombo.place(y=292,x=650)

        tk.Label(self, text="Nom de rue : ", font=('Arial', 11), fg="black", bg='#27ae60').place(x=508,y=320)
        self.e_namewall = tk.Entry(self, bd=3,font=('Arial', 11),width=29,fg="gray")
        self.e_namewall.config(validate='key', validatecommand=(self.e_namewall.register(lambda inp_str: self.character_limit_str(inp_str, 100)), "%P"))
        tk.Label(self, text="Code Postale : ", font=('Arial', 11), fg="black", bg='#27ae60').place(x=496,y=350)
        self.e_postalecode = tk.Entry(self, bd=3,font=('Arial', 11),width=29,fg="gray")
        self.e_postalecode.config(validate='key', validatecommand=(self.e_postalecode.register(lambda inp: self.character_limit(inp, 5)), "%P"))
        tk.Label(self, text="Commune :", font=('Arial', 11), fg="black", bg='#27ae60').place(x=514,y=380)
        self.e_common = tk.Entry(self, bd=3,font=('Arial', 11),width=29,fg="gray")
        self.e_common.config(validate='key', validatecommand=(self.e_common.register(lambda inp_str: self.character_limit_str(inp_str, 40)), "%P"))
        tk.Label(self, text="Superficie couvert : ", font=('Arial', 11), fg="black", bg='#27ae60').place(x=465,y=410)
        self.e_areacovered = tk.Entry(self, bd=3,font=('Arial', 11),width=29,fg="gray")
        self.e_areacovered.config(validate='key', validatecommand=(self.e_areacovered.register(lambda inp: self.character_limit(inp, 5)), "%P"))
        tk.Label(self, text="Superficie jardin : ", font=('Arial', 11), fg="black", bg='#27ae60').place(x=477,y=440)
        self.e_areagarden = tk.Entry(self, bd=3,font=('Arial', 11),width=29,fg="gray")
        self.e_areagarden.config(validate='key', validatecommand=(self.e_areagarden.register(lambda inp: self.character_limit(inp, 5)), "%P"))
        tk.Label(self, text="Nombre de pièce : ", font=('Arial', 11), fg="black", bg='#27ae60').place(x=470,y=470)
        self.e_numroom = tk.Entry(self, bd=3,font=('Arial', 11),width=29,fg="gray")
        self.e_numroom.config(validate='key', validatecommand=(self.e_numroom.register(lambda inp: self.character_limit(inp, 3)), "%P"))
        tk.Label(self, text="Classe énergétique : ", font=('Arial', 11), fg="black", bg='#27ae60').place(x=455,y=500)
        self.liste_typeenergie = ["", "A", "B", "C", "D", "E", "F", "G"]
        self.listComboEnergy = ttk.Combobox(self, values=self.liste_typeenergie, state="readonly")


        tk.Label(self, text="Année de construction : ", font=('Arial', 11), fg="black", bg='#27ae60').place(x=436,y=530)
        self.e_yearconstruct = tk.Entry(self, bd=3,font=('Arial', 11),width=29,fg="gray")
        self.e_yearconstruct.config(validate='key', validatecommand=(self.e_yearconstruct.register(lambda inp: self.character_limit(inp, 4)), "%P"))
        self.value_naturemana = tk.StringVar(None, "VN")
        b_sell = tk.Radiobutton(self, text="Vente", variable=self.value_naturemana, value='Vente',highlightthickness=0,bg='#27ae60',activebackground='#27ae60',font=('Arial', 13))
        b_location = tk.Radiobutton(self, text="Location", variable=self.value_naturemana, value='Location',bg='#27ae60',activebackground='#27ae60',font=('Arial', 13))
        tk.Label(self, text="Date de mise en marche :", font=('Arial', 11), fg="black", bg='#27ae60').place(x=420,y=560)
        self.cal = DateEntry(self, selectmode='day', date_pattern='dd/mm/yyyy')
        tk.Label(self, text="Prix :", font=('Arial', 11), fg="black", bg='#27ae60').place(x=556,y=590)
        self.e_price = tk.Entry(self, bd=3,font=('Arial', 11),width=29,fg="gray")
        self.e_price.config(validate='key', validatecommand=(self.e_price.register(lambda inp: self.character_limit(inp, 8)), "%P"))

        
        self.value_bien.set("VB")
        self.e_no.place(y=258,x=600)
        self.e_namewall.place(y=318,x=600)
        self.e_postalecode.place(y=348,x=600)
        self.e_common.place(y=378,x=600)
        self.e_areacovered.place(y=408,x=600)
        self.e_areagarden.place(y=438,x=600)
        self.e_numroom.place(y=468,x=600)
        self.listComboEnergy.place(y=501,x=650  )
        self.e_yearconstruct.place(y=528,x=600)
        b_sell.place(x=600,y=180)
        b_location.place(x=750,y=180)
        self.value_bien.set("VN")
        self.cal.place(y=562,x=675)
        self.e_price.place(y=588,x=600)
        tk.Button(self, text="Enregistrer", command=self.save_data).place(y=628,x=677,height=45,width=90)

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


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.canvas = Canvas(self, bg="#FFFFFF", height=770, width=1450, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        self.p_main = PageMain(self)
        self.p_research = PageResearch(self)
        self.p_save = PageSave(self)

        self.canvas.create_rectangle(
            0.0,
            28.0,
            1450.0,  # PARTI COULEUR DU CORPS DU TEXTE
            1052.0,
            fill="#219653",
            outline="")

        self.canvas.create_rectangle(0, 0, 489, 119, fill="#219653", outline="", tags="rec_main")
        self.canvas.create_text(230.00, 55.00, text="Accueil", font=("Ink Free", '22'), tags="rec_main")
        self.canvas.tag_bind("rec_main", "<Button-1>", self.show_main)

        self.canvas.create_rectangle(489, 0, 970, 119, fill="#27AE60", outline="", tags="rec_save")
        self.canvas.create_text(715.00, 55.00, text="Enregistrement de bien", font=("Ink Free", '22'), tags="rec_save")
        self.canvas.tag_bind("rec_save", "<Button-1>", self.show_save)

        self.canvas.create_rectangle(970, 0, 1450, 119, fill="#6FCF97", outline="", tags="rec_research")
        self.canvas.create_text(1200, 55, text="Recherche de bien", font=("Ink Free", '22'), tags="rec_research")
        self.canvas.tag_bind("rec_research", "<Button-1>", self.show_research)

        self.canvas.create_text(655.00, 450.00, text="Bienvenue sur votre logiciel de gestion de bien",
                                font=('Ink Free', '30'))

    def show_main(self, event= None):
        PageMain(self).pack(side="top", fill="both", expand=True)
        PageResearch(self).pack_forget()
        self.p_save.pack_forget()

    def show_research(self, event= None):
        self.p_main.pack_forget()
        self.p_research.pack(side="top", fill="both", expand=True)
        self.p_save.pack_forget()

    def show_save(self, event= None):
        self.p_main.pack_forget()
        self.p_research.pack_forget()
        self.p_save.pack(side="top", fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1450x770")
    root.resizable(False, False)
    root.mainloop()