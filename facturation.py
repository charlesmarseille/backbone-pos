from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
#import os



class MainScreen(TabbedPanel):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.graph = plt.figure(dpi=200,figsize=(8,6))
        self.path = '/stats/'
        self.facture=[]

        # Liste des catégories et produits vendus
        self.liste_categories = []
        self.infos_inventaire = ['Produits', 'Prix', 'Taxable', 'Stocks']
        menu_path = 'Inventaire.xlsx'
        self.menu = self.lecture_inventaire(menu_path)

        # Initialisation du menu de vente sur l'application
        self.creer_menu_app()


    ### Graphique et stats
    #Sauvegarde des graphiques

    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def enregistrer_image(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9),
                            pos_hint={'x': 0,'y': 0})
        self._popup.open()

    def save(self, path, filename):
        print(path+'/'+filename)
        plt.savefig(path+'/'+filename)
        self.dismiss_popup()



    def changer_image(self, event):
        if event.text == 'semaine':
            valeurs=np.array(pd.read_csv('stats.csv', usecols=(0,1))).T
            self.graph = plt.plot(valeurs[0],valeurs[1])

        if event.text == 'mois':
            valeurs=np.array(pd.read_csv('stats.csv', usecols=(0,2)))
            self.graph = plt.plot(valeurs[0],valeurs[1])

        if event.text == 'année':
            valeurs=np.array(pd.read_csv('stats.csv', usecols=(0,3)))
            self.graph = plt.plot(valeurs[0],valeurs[1])

        plt.savefig(event.text + '.png')
        self.ids.graphique.source = event.text + '.png'


    def creer_menu_app(self):
        dropdown_list = []
        for i in range(len(self.liste_categories)):
            nouveau_bouton = Button(text=self.liste_categories[i], size_hint_x=None, width=100)
            print (self.ids.MV)
            self.ids.MV.add_widget(nouveau_bouton)

            for j in range(len(self.menu[self.liste_categories[i]]['Produits'])):
                dropdown_list.append(DropDown())
                bouton_item = Button(text=self.menu[self.liste_categories[i]]['Produits'][j], on_release=self.ajouter_au_panier,
                    size_hint_y = None, height = 40)
                bouton_item.bind(on_release=dropdown_list[i].dismiss)
                dropdown_list[i].add_widget(bouton_item)

            nouveau_bouton.bind(on_release = dropdown_list[i].open)


    def ajouter_au_panier(self, event):
        self.facture.append(np.array([event.text[0:10],event.text[1]]))
        print (self.facture)



    def lecture_inventaire(self, menu_path):
        # Lecture de l'inventaire (fichier excel)
        menu = {}
        excel_file = pd.ExcelFile(menu_path)

        # Création du dictionnaire contenant l'inventaire
        for sheet_name in excel_file.sheet_names:
            self.liste_categories.append(sheet_name)
            menu[sheet_name] = {}
            liste_produits = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=(1), header=None,
                na_values=('NaN'), true_values=('oui'), false_values=('non'))
            for i in range(len(self.infos_inventaire)):
                menu[sheet_name][self.infos_inventaire[i]] = []
                for j in range(len(liste_produits[i])):
                    menu[sheet_name][self.infos_inventaire[i]].append(liste_produits[i][j])

        return menu


class BoutonMenuVente(Button):
    pass

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class FacturationApp(App):
    def build(self):
        return MainScreen()


Factory.register('MainScreen', cls=MainScreen)
Factory.register('SaveDialog', cls=SaveDialog)


if __name__ == '__main__':
    FacturationApp().run()