from pyrebase import *
import matplotlib.pyplot as plt
from tkinter import *
import datetime

#-------------------------------------------- LOGOWANIE DO BAZY DANYCH --------------------------------------------
firebaseConfig={'apiKey': "***",
    'authDomain': "***",
    'databaseURL':"***",
    'projectId': "***",
    'storageBucket': "***",
    'messagingSenderId': "***",
    'appId': "***",
    'measurementId': "***"}

firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()

auth=firebase.auth()


email="***"
password="***"
auth.sign_in_with_email_and_password(email, password)

#--------------------------------------------FUNKCJA GENERUJACA WYKRES-------------------------------------------------------------------

#funkcja, która na podstawie daty i nazwy odczytu generuje jej wykres,
#jesli data jest nieprawidlowa wyswietla informacje o blednej dacie
def dane_pobieranie():
    global var_dzien
    global var_rok
    global var_miesiac
    global var_dzien2
    global var_rok2
    global var_miesiac2
    global var_odczyt

    var_miesiac_convert = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}

    try:
        data1 = datetime.datetime(int(var_rok.get()), int(var_miesiac.get()), int(var_dzien.get()))
        data2 = datetime.datetime(int(var_rok2.get()), int(var_miesiac2.get()), int(var_dzien2.get()))

        if (data2 < data1):
            window_error = Tk()
            window_error.title("ERROR")
            window_error.geometry('570x50')

            mylabel_blad = Label(window_error, text="Komentarz: Upewnij się czy podany zakres dat jest prawidłowy.",font=("Arial Bold", 14),fg="red")
            mylabel_blad.place(x=10, y=10)

            window_error.mainloop()
            return

        x = []
        y = []

        while data1 <= data2:
            try:
                data_string = str(data1)

                dzien_pobrany = data_string[8] + data_string[9]

                miesiac_pobrany = data_string[5] + data_string[6]

                rok_pobrany = data_string[0] + data_string[1] + data_string[2] + data_string[3]

                # dane_pobieranie("2021-May-05","temperatura")
                dzien_data = rok_pobrany + "-" + var_miesiac_convert[miesiac_pobrany] + "-" + dzien_pobrany
                czujnik = var_odczyt.get()

                dzien = db.child(dzien_data).get()
                dane = dzien.val()
                hours = []
                val = []
                indeksyfirebase = []
                readings = []
                xtemp = []

                for (key, value) in dane.items():
                    hours.append(key)
                    val.append(value)

                for j in range(len(val)):
                    indeksyfirebase.append(list(val[j].values()))
                    xtemp2 = var_miesiac_convert[miesiac_pobrany] + "\n" + dzien_pobrany + "\n" + hours[j]
                    xtemp.append(xtemp2)

                for z in range(len(val)):
                    readings.append(indeksyfirebase[z][0][czujnik])

                if (czujnik == "naslonecznienie"):
                    new = []
                    for n in range(len(readings)):
                        new.append((readings[n] * 100) / 4095)
                    readings = new

                x = x + xtemp
                y = y + readings

                data1 = data1 + datetime.timedelta(days=1)
            except:
                data1 = data1 + datetime.timedelta(days=1)

        if (len(x) == 0):
            window_error2 = Tk()
            window_error2.title("ERROR")
            window_error2.geometry('1080x50')

            mylabel_blad2 = Label(window_error2,text="Komentarz: Nie posiadasz dostępu do odczytu zawartości bazy danych lub w bazie nie istnieją odczyty z podanego zakresu.",font=("Arial Bold", 14),fg="red")
            mylabel_blad2.place(x=10, y=10)

            window_error2.mainloop()
            return

        plt.plot(x, y, marker='o', color="red", linewidth=3)
        plt.grid(True)
        plt.legend([czujnik])
        plt.xlabel("Data oraz godzina odczytu")

        if (czujnik == "temperatura"):
            plt.ylabel("°C")
        else:
            plt.ylabel("%")

        plt.show()
    except:
        window_error3 = Tk()
        window_error3.title("ERROR")
        window_error3.geometry('350x50')

        mylabel_blad3 = Label(window_error3,text="Komentarz: Podana data jest błędna.",font=("Arial Bold", 14),fg="red")
        mylabel_blad3.place(x=10, y=10)

        window_error3.mainloop()

#--------------------------------------------FUNKCJA WYSYLAJACA DANE PROBKOWANIA-------------------------------------------------------------------

def dane_probka():
    global var_proba
    data_probka=var_proba.get()
    db.child("Properties").child("TemperaturaON").set(data_probka)

#--------------------------------------------FUNKCJA WYSYLAJACA DANE SILNIKA-------------------------------------------------------------------

def dane_silnik():
    global var_silnik
    data_silnik=var_silnik.get()
    db.child("Properties").child("WentylatorS").set(data_silnik)

#----------------------------------------------------------- GUI -----------------------------------------------------------------------

#-----UTWORZENIE GUI-----
window = Tk()
window.title("Aplikacja - Analizator Powietrza")
window.geometry('1150x650')

#-----NAPISY-----
mylabel_dzien = Label(window, text="Wybierz Dzień:",font=("Arial Bold",18))
mylabel_dzien.place(x=100, y=50)

mylabel_miesiac = Label(window, text="Wybierz Miesiąc:",font=("Arial Bold",18))
mylabel_miesiac.place(x=100, y=200)

mylabel_rok = Label(window, text="Wybierz Rok:",font=("Arial Bold",18))
mylabel_rok.place(x=100, y=350)

mylabel_dzien2 = Label(window, text="Wybierz Dzień:",font=("Arial Bold",18))
mylabel_dzien2.place(x=400, y=50)

mylabel_miesiac2 = Label(window, text="Wybierz Miesiąc:",font=("Arial Bold",18))
mylabel_miesiac2.place(x=400, y=200)

mylabel_rok2 = Label(window, text="Wybierz Rok:",font=("Arial Bold",18))
mylabel_rok2.place(x=400, y=350)

mylabel_odczyt = Label(window, text="Wybierz Czujnik:",font=("Arial Bold",18))
mylabel_odczyt.place(x=700, y=50)

mylabel_od = Label(window, text="Data początkowa:",font=("Arial Bold",14, 'underline italic'))
mylabel_od.place(x=100, y=10)

mylabel_do = Label(window, text="Data końcowa:",font=("Arial Bold",14, 'underline italic'))
mylabel_do.place(x=410, y=10)

mylabel_button = Label(window, text="Aby wygenerować wykres wciśnij przycisk:",font=("Arial Bold",13))
mylabel_button.place(x=700, y=200)

mylabel_czas = Label(window, text="Temperatura włączenia wentylatora:",font=("Arial Bold",18))
mylabel_czas.place(x=700, y=350)

mylabel_czas = Label(window, text="Wybierz poziom prędkości silnika:",font=("Arial Bold",18))
mylabel_czas.place(x=700, y=480)

#-----PRZYCSIK GENERUJACY WYKRES-----
myButton = Button(window, text="Wygeneruj wykres", font=("Arial Bold",20, 'underline italic'), padx=40, pady=20, command=dane_pobieranie, bg="#1ec81e",activebackground="#336633")
myButton.place(x=700, y=225)

#-----PRZYCSIK Zatwierdzający częstotliwość próbkowania-----
myButton2 = Button(window, text="Zatwierdź", font=("Arial Bold",20), padx=6, pady=2, command=dane_probka, bg="#1ec81e",activebackground="#336633")
myButton2.place(x=970, y=400)

#-----PRZYCSIK Zatwierdzający prędkość silnika-----
myButton3 = Button(window, text="Zatwierdź", font=("Arial Bold",20), padx=6, pady=2, command=dane_silnik, bg="#1ec81e",activebackground="#336633")
myButton3.place(x=970, y=530)

#myButton

#-----MENU OPCJONALNE-----
#-----OD-----
#dzien
var_dzien_all=[1,2,3,4,5,6,7,8,9,10,11,
               12,13,14,15,16,17,18,19,20,21,
               22,23,24,25,26,27,28,29,30,31]

var_dzien = IntVar(window)
var_dzien.set(var_dzien_all[0]) # default value

lista_dzien=OptionMenu(window, var_dzien, *var_dzien_all)
lista_dzien.config(font=('arial',(16)),bg="#DCDCDC",activebackground="#96B4B4",width=6)
lista_dzien.place(x=130, y=100)

#miesiac
#var_miesiac_all=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Dec"]
var_miesiac_all=[1,2,3,4,5,6,7,8,9,10,11,12]
var_miesiac = IntVar(window)
var_miesiac.set(var_miesiac_all[0]) # default value

lista_miesiac=OptionMenu(window, var_miesiac, *var_miesiac_all)
lista_miesiac.config(font=('arial',(16)),bg="#DCDCDC",activebackground="#96B4B4",width=6)
#lista_miesiac["menu"].config(bg="RED")
lista_miesiac.place(x=130, y=250)

#rok
var_rok_all=[2022,2021,2020,2019]
var_rok = IntVar(window)
var_rok.set(var_rok_all[0]) # default value

lista_rok=OptionMenu(window, var_rok, *var_rok_all)
lista_rok.config(font=('arial',(16)),bg="#DCDCDC",activebackground="#96B4B4",width=6)
lista_rok.place(x=130, y=400)

#-----DO-----
#dzien
var_dzien_all2=[1,2,3,4,5,6,7,8,9,10,11,
               12,13,14,15,16,17,18,19,20,21,
               22,23,24,25,26,27,28,29,30,31]

var_dzien2 = IntVar(window)
var_dzien2.set(var_dzien_all2[0]) # default value

lista_dzien2=OptionMenu(window, var_dzien2, *var_dzien_all2)
lista_dzien2.config(font=('arial',(16)),bg="#DCDCDC",activebackground="#96B4B4",width=6)
lista_dzien2.place(x=430, y=100)

#miesiac
#var_miesiac_all2=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Dec"]
var_miesiac_all2=[1,2,3,4,5,6,7,8,9,10,11,12]
var_miesiac2 = IntVar(window)
var_miesiac2.set(var_miesiac_all2[0]) # default value

lista_miesiac2=OptionMenu(window, var_miesiac2, *var_miesiac_all2)
lista_miesiac2.config(font=('arial',(16)),bg="#DCDCDC",activebackground="#96B4B4",width=6)
#lista_miesiac["menu"].config(bg="RED")
lista_miesiac2.place(x=430, y=250)

#rok
var_rok_all2=[2022,2021,2020,2019]
var_rok2 = IntVar(window)
var_rok2.set(var_rok_all2[0]) # default value

lista_rok2=OptionMenu(window, var_rok2, *var_rok_all2)
lista_rok2.config(font=('arial',(16)),bg="#DCDCDC",activebackground="#96B4B4",width=6)
lista_rok2.place(x=430, y=400)

#odczyt
var_odczyt_all=["temperatura","wilgotnosc","naslonecznienie"]
var_odczyt = StringVar(window)
var_odczyt.set(var_odczyt_all[0]) # default value

lista_odczyt=OptionMenu(window, var_odczyt, *var_odczyt_all)
lista_odczyt.config(font=('arial',(16)),bg="#DCDCDC",activebackground="#96B4B4",width=12)
lista_odczyt.place(x=695, y=110)

#wlaczenie wentylatora
var_proba_all=[10,12,14,16,18,20,22,24,26,28,30,32,34,36]
var_proba = IntVar(window)
var_proba.set(var_proba_all[0]) # default value

lista_proba=OptionMenu(window, var_proba, *var_proba_all)
lista_proba.config(font=('arial',(16)),bg="#DCDCDC",activebackground="#96B4B4",width=6)
lista_proba.place(x=830, y=400)

#silnik
var_silnik_all=[0,1,2,3]
var_silnik = IntVar(window)
var_silnik.set(var_silnik_all[0]) # default value

lista_silnik=OptionMenu(window, var_silnik, *var_silnik_all)
lista_silnik.config(font=('arial',(16)),bg="#DCDCDC",activebackground="#96B4B4",width=6)
lista_silnik.place(x=830, y=530)

#-----UCRUCHOMIENIE PETLI GUI-----
window.mainloop()
