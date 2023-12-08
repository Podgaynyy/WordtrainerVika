from kivy.config import Config
Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'width', 300)
Config.set('graphics', 'height', 500)

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
import random
from kivy.uix.image import Image



# from kivy.animation import Animation
# from kivy.clock import Clock
# from kivy.config import Config
# from kivy.uix.image import Image
# from kivy.core import audio
# from kivy.core.audio import SoundLoader

# import socket
# sock = socket.socket()
# sock.bind(('', 9090))
# sock.listen(1)


# I set the color constants to then color the text on the buttons (this is optional)




class MainApp(App):
    def build(self):
        # here I add the main and second screens to the manager, this class does nothing else
        sm.add_widget(MainScreen())
        sm.add_widget(SecondScreen())

        return sm  # I return the manager to work with him later

    def abschliessen(*arrgs):
        # schluss() #woerterbuch loeschen
        datei = open('woerterbuch.txt', 'w')
        datei.close()
        MainApp().stop()


liste = []


class MainScreen(Screen):
    def __init__(self):
        super().__init__()



        self.name = 'Main'  # setting the screen name value for the screen manager
        # (it's more convenient to call by name rather than by class)

        main_layout = BoxLayout(orientation='vertical')
        top_layout = AnchorLayout(anchor_x='center', anchor_y ='top', size_hint = (1, .3))
        top_layout.add_widget(Label(text="Bibliothek erstellen", font_size = 60))
        # creating an empty layout that's not bound to the screen

        center_layout = AnchorLayout(anchor_x='center', anchor_y='center',size_hint = (1, .15))
        bl = GridLayout(cols=2, rows=2, padding = 20)
        # erste Gridlayout wird aus zwei spalten in 2te Zeile bl passen 30% gesamtlayout
        bl.add_widget(Label(text="Wort"))
        self.wort = TextInput()
        bl.add_widget(self.wort)
        bl.add_widget(Label(text="Bedeutung"))
        self.bedeutung = TextInput()
        bl.add_widget(self.bedeutung)
        center_layout.add_widget(bl)

        low_layout = AnchorLayout(anchor_x='center', size_hint = (1, .55))
        gl = BoxLayout(orientation='vertical', size_hint = (0.8, 0.8))
        # rest 50% uebernimmt Layout mit 3 Buttons Speichern, Prueffen und Abbrechen
        gl.add_widget(Button(text="Speichern", on_press = self.erschaffeWoerterbuch))
        gl.add_widget(Button(text="Prüfen", on_press=self.to_second_scrn))
        gl.add_widget(Button(text="Abbrechen", on_press = MainApp.abschliessen))
        low_layout.add_widget(gl)

        main_layout.add_widget(top_layout)
        main_layout.add_widget(center_layout)
        main_layout.add_widget(low_layout)

        self.add_widget(main_layout)




    def erschaffeWoerterbuch(self, *args):    # Aufbau eines fremdsprache-deutschen Wörterbuchs
        datei = open('woerterbuch.txt', 'a')
        if self.wort.text == '':
            datei.close()
        elif self.wort.text == ' ':
            datei.close()
        else:
            datei.write(self.wort.text + " " + self.bedeutung.text + "\n")
            self.wort.text = ""
            self.bedeutung.text = ""


    def getListe(self):
        global liste
        datei = open('woerterbuch.txt', 'r', encoding='utf-8')
        wortschatz = datei.readlines()
        datei.close()
        for zeile in wortschatz:
            if zeile == '\n' or zeile == ' \n':
                pass
            else:
                vokabel = zeile.split()
                liste.append(vokabel)

    def to_second_scrn(self, *args):
        self.manager.current = 'Second'  # selecting the screen by name (in this case by name "Second")
        self.getListe()
        return 0  # this line is optional

checkElement = []



class SecondScreen(Screen):
    def __init__(self):
        super().__init__()
    # on this screen, I do everything the same as on the main screen to be able to switch back and forth
        self.name = 'Second'
        second_layout = BoxLayout(orientation='vertical')

        # um in eine Zeile verschiedene Anzahl von Spalten zu haben
        # nehme ich BoxLayout als Grundwerkstoff
        self.topLayout = AnchorLayout(anchor_x='center', anchor_y ='top', size_hint = (1, .25))
        self.blTop = BoxLayout(orientation='vertical', size_hint = (.9,.9))
        self.title2 = Label(text="Wörte lernen", font_size=50, size_hint=(1,.7))
        self.antwort = TextInput(size_hint=(1,.3))          # Feld fuer Antworteingabe
        self.blTop.add_widget(self.title2)
        self.blTop.add_widget(self.antwort)
        self.topLayout.add_widget(self.blTop)

        self.centerLayout = BoxLayout(orientation='vertical', size_hint = (1, .45))
        self.abfrage = Label(font_size=55, size_hint = (1,.3))  # Wird Woerte abgefragt
        self.centerLayout.add_widget(self.abfrage)
        self.abfrage_blank = Label(size_hint = (1,.7))
        self.centerLayout.add_widget(self.abfrage_blank)
        self.richtig = Image(source = 'Right.png', size_hint = (1,.7))
        self.falsch = Image(source = 'NotRight.png', size_hint = (1,.7))

        self.lowLayout = AnchorLayout(anchor_x='center', anchor_y ='bottom', size_hint = (1, .5))
        self.blDown = BoxLayout(orientation='vertical', padding = 5)
        self.blDown.add_widget(Button(text="Prüfen", on_press = self.pruefung))
        self.blDown.add_widget(Button(text="Prüfung Starten", on_press=self.listeChoice))
        self.blDown.add_widget(Button(text="Programm schliessen", on_press=MainApp.abschliessen))
        self.lowLayout.add_widget(self.blDown)

        second_layout.add_widget(self.topLayout)
        second_layout.add_widget(self.centerLayout)
        second_layout.add_widget(self.lowLayout)
        self.add_widget(second_layout)




    def listeChoice(self, *args):
        global checkElement
        if len(liste) != 0:
            checkElement = random.choice(liste)
            self.abfrage.text = "Was bedeutet: " + checkElement[0]
        else:
            self.title2.text = "Abgeschlossen! \n   Alles gelernt."
            self.centerLayout.remove_widget(self.abfrage)


    def pruefung(self, *args):
        global liste
        try:
            if self.antwort.text == checkElement[1]:
                self.title2.text = "Richtig!"
                self.centerLayout.remove_widget(self.falsch)
                self.centerLayout.remove_widget(self.abfrage_blank)
                self.centerLayout.add_widget(self.richtig)
                self.antwort.text = ""
                liste.remove(checkElement)
                self.listeChoice()
            else:
                self.title2.text ="Leider falsch!"
                self.centerLayout.remove_widget(self.richtig)
                self.centerLayout.remove_widget(self.abfrage_blank)
                self.centerLayout.add_widget(self.falsch)
                self.antwort.text = ""
                self.listeChoice()
        except:
            self.title2.text = "Nichts zum Lernen"


    def to_main_scrn(self, *args):  # together with the click of the button, it transmits info about itself.
        # In order not to pop up an error, I add *args to the function
        self.manager.current = 'Main'
        return 0


sm = ScreenManager()  # it's necessary to create a manager variable that will collect screens and manage them

if __name__ == '__main__':
    MainApp().run()