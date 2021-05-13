from math import exp
from os import name, write
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import pandas as pd
import csv
import random
import timeit
import matplotlib.pyplot as plt
import numpy as np
from pandas.core.accessor import register_series_accessor

Dane_g = None

New_Data = {'srednia': {'wynik': [], 'czas': []},
            'min': {'wynik': [], 'czas': []},
            'max': {'wynik': [], 'czas': []},
            'mediana': {'wynik': [], 'czas': []}}

przedzial = {x: 0 for x in range(0,100000, 10000)} # przedzialy od 0 do 1000000 step: 10000 
przedzial.pop(0) # usunięcie 1 elementu (0: 0)

przedzial_zapis = list(przedzial)

with open('init.txt') as f:
    plik = f.readlines()

we = plik[0].rstrip()
wy = plik[1].rstrip()

class MainWindow(Screen):
    def zapisz_nowy(self):
        start = timeit.default_timer()
        # nazwa_w = self.plik_w.text + '.csv'

        with open(wy, 'w', encoding='utf-8') as csvfile: # w-zapis
            writer = csv.writer(csvfile)
            for keys in New_Data.keys():
                writer.writerow([keys])
                for x in range(len(przedzial_zapis)):
                    try:
                        formatted_float = "{:.3f}".format(New_Data[keys]['czas'][x])
                        writer.writerow([przedzial_zapis[x], formatted_float])
                    except:
                        continue

            writer.writerow(['MEDIANA'])
            writer.writerow(New_Data['mediana']['wynik'])
            
        Dane_g.to_csv(wy, encoding='utf-8', index=False, mode='a')
        self.reset()
        stop = timeit.default_timer()
        print('Zapis trwal: ', stop-start, 's')

    # OPERACJE NA DANYCH
    def srednia_arytm(self):
        for key, val in przedzial.items():
            start = timeit.default_timer()
            srednia = sum(Dane_g['Dane'].loc[val: key]) / key
            stop =  timeit.default_timer()
            czas = stop-start
            New_Data['srednia']['czas'].append(czas)
            New_Data['srednia']['wynik'].append(srednia)
        
    def minimum(self):
        for key, val in przedzial.items():
            start = timeit.default_timer()
            res = min(Dane_g['Dane'].loc[val: key])
            stop =  timeit.default_timer()
            czas = stop-start
            New_Data['min']['czas'].append(czas)
            New_Data['min']['wynik'].append(res)

    def maximum(self): 
        for key, val in przedzial.items():
            start = timeit.default_timer()
            res = max(Dane_g['Dane'].loc[val: key])
            stop =  timeit.default_timer()
            czas = stop-start
            New_Data['max']['czas'].append(czas)
            New_Data['max']['wynik'].append(res)

    def mediana(self): 
        for key, val in przedzial.items():
            start = timeit.default_timer()
            s = list(Dane_g['Dane'].loc[val: key])
            s.sort()
            
            if len(s)%2 == 0:
                mediana = (s[int(len(s)/2)] + s[int(len(s)/2)+1])/2
            else:
                mediana = s[int(len(s)/2)]
            stop =  timeit.default_timer()
            czas = stop-start
            New_Data['mediana']['czas'].append(czas)
            New_Data['mediana']['wynik'].append(mediana)


    
    # WYKRESY
    def wykres_sredniej(self):
        try:
            plt.plot(list(przedzial), New_Data['srednia']['czas'], 'bo')
            plt.title('Średnia arytmetyczna')
            plt.xlabel('Wielkość instancji')
            plt.ylabel('Czas [s]')
            z = np.polyfit(list(przedzial), New_Data['srednia']['czas'], 1)
            p = np.poly1d(z)
            plt.plot(list(przedzial), p(list(przedzial)),"r--")
            plt.grid()
            plt.show()
        except:
            wczytaj_dane()

    def wykres_min(self):
        try:
            plt.plot(list(przedzial), New_Data['min']['czas'], 'bo')
            plt.title('Min')
            plt.xlabel('Wielkość instancji')
            plt.ylabel('Czas [s]')
            z = np.polyfit(list(przedzial), New_Data['min']['czas'], 1)
            p = np.poly1d(z)
            plt.plot(list(przedzial), p(list(przedzial)),"r--")
            plt.grid()
            plt.show()
        except:
            wczytaj_dane()

    def wykres_max(self):
        try:
            plt.plot(list(przedzial), New_Data['max']['czas'], 'bo')
            plt.title('Max')
            plt.xlabel('Wielkość instancji')
            plt.ylabel('Czas [s]')
            z = np.polyfit(list(przedzial), New_Data['max']['czas'], 1)
            p = np.poly1d(z)
            plt.plot(list(przedzial), p(list(przedzial)),"r--")
            plt.grid()
            plt.show()
        except:
            wczytaj_dane()

    def wykres_mediana(self):
        try:
            plt.plot(list(przedzial), New_Data['mediana']['czas'], 'bo')
            plt.title('Mediana')
            plt.xlabel('Wielkość instancji')
            plt.ylabel('Czas [s]')
            z = np.polyfit(list(przedzial), New_Data['mediana']['czas'], 1)
            p = np.poly1d(z)
            plt.plot(list(przedzial), p(list(przedzial)),"r--")
            plt.grid()
            plt.show()
        except:
            wczytaj_dane()
            
    def reset(self):
        New_Data.clear()

# Klasa umożliwiająca przechodzenie między oknami Main, AppWin, Create
class WindowManager(ScreenManager):
    pass

# Funkcje wyskakujących okienek (Popup Winow), zawierające dodatkowe informacje o działaniu aplikacji
def brak_pliku():
    pop = Popup(title='Error',
                  content=Label(text='Nie znaleziono pliku!'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

def wczytaj_dane():
    pop = Popup(title='Error',
                  content=Label(text='Wczytaj dane!'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

kv = Builder.load_file("my2.kv")
sm = WindowManager()

# Funkcjonalność przechodzenia między oknami aplikacji
screens = [MainWindow(name='Main')]
for screen in screens:
    sm.add_widget(screen)

start = timeit.default_timer()
try:
    file = pd.read_csv(we)
    Dane_g = file
except:
    brak_pliku()
stop = timeit.default_timer()


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    MyMainApp().run()
