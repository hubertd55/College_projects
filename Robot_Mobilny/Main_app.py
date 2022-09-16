#zaimportowane bilbioteki
from threading import Thread
from tkinter import *
import serial
import keyboard
import time

#Komunikat informujący o uruchomieniu programu
print("STARTUJEMY!")
#nawiązanie komunikacji z portem szeregowym
stm = serial.Serial(port='COM3', baudrate=9600, timeout=0.1)
#komunikat informujący o nawiązaniu komunikacji
print("POłĄCZONO Z ROBOTEM!")

czujniki=['0','0','0','0','0','0']
lewy='0'
prawy='0'
zwrotnasilniki='0'

#definicja funckji aktualizującej informacje o sterowaniu silnikami w GUI
def aktualizacjaBG1():
    #lewy silnik
    if(lewy=='3'):
        mylabel12.config(bg="blue")
    else:
        mylabel12.config(bg="white")

    if (lewy == '2'):
        mylabel13.config(bg="blue")
    else:
        mylabel13.config(bg="white")

    if (lewy == '1'):
        mylabel14.config(bg="blue")
    else:
        mylabel14.config(bg="white")

    #prawy silnik
    if(prawy=='3'):
        mylabel15.config(bg="blue")
    else:
        mylabel15.config(bg="white")

    if (prawy == '2'):
        mylabel16.config(bg="blue")
    else:
        mylabel16.config(bg="white")

    if (prawy == '1'):
        mylabel17.config(bg="blue")
    else:
        mylabel17.config(bg="white")

#definicja funckji aktualizującej informacje o odczytach czujników w GUI
def aktualizacjaBG2():
    #odczyty czujnikow
    if (czujniki[0] == '1'):
        mylabel1.config(bg="green")
    elif (czujniki[0] == '0'):
        mylabel1.config(bg="red")

    if (czujniki[1] == '1'):
        mylabel2.config(bg="green")
    elif (czujniki[1] == '0'):
        mylabel2.config(bg="red")

    if (czujniki[2] == '1'):
        mylabel3.config(bg="green")
    elif (czujniki[2] == '0'):
        mylabel3.config(bg="red")

    if (czujniki[3] == '1'):
        mylabel4.config(bg="green")
    elif (czujniki[3] == '0'):
        mylabel4.config(bg="red")

    if (czujniki[4] == '1'):
        mylabel5.config(bg="green")
    elif (czujniki[4] == '0'):
        mylabel5.config(bg="red")

    if (czujniki[5] == '1'):
        mylabel6.config(bg="green")
    elif (czujniki[5] == '0'):
        mylabel6.config(bg="red")

#utworzenie GUI
window = Tk()
window.title("Centrum Sterowania")
window.geometry('900x600')

#naglowek czujniki
mylabel0 = Label(window, text="Odczyty czujników:",font=("Arial Bold",20))
mylabel0.place(x=330, y=20)
#odczyt czujnika 1
mylabel1 = Label(window, text="D1", font=("Arial Bold", 20), padx=15, pady=5, fg="black", bg="white")
mylabel1.place(x=40, y=100)
# odczyt czujnika 2
mylabel2 = Label(window, text="D2", font=("Arial Bold", 20), padx=15, pady=5, fg="black", bg="white")
mylabel2.place(x=190, y=100)
# odczyt czujnika 3
mylabel3 = Label(window, text="D3", font=("Arial Bold", 20), padx=15, pady=5, fg="black", bg="white")
mylabel3.place(x=340, y=100)
# odczyt czujnika 4
mylabel4 = Label(window, text="D4", font=("Arial Bold", 20), padx=15, pady=5, fg="black", bg="white")
mylabel4.place(x=490, y=100)
# odczyt czujnika 5
mylabel5 = Label(window, text="D5", font=("Arial Bold", 20), padx=15, pady=5, fg="black", bg="white")
mylabel5.place(x=640, y=100)
# odczyt czujnika 6
mylabel6 = Label(window, text="D6", font=("Arial Bold", 20), padx=15, pady=5, fg="black", bg="white")
mylabel6.place(x=790, y=100)

#naglowek silniki
mylabel11 = Label(window, text="Wysterowanie silników:",font=("Arial Bold",20))
mylabel11.place(x=300, y=200)

mylabel12 = Label(window, text="LP", font=("Arial Bold", 20), padx=15, pady=5, fg="black", bg="white")
mylabel12.place(x=300, y=300)

mylabel13 = Label(window, text="LT", font=("Arial Bold", 20), padx=15, pady=5, fg="black", bg="white")
mylabel13.place(x=300, y=500)

mylabel14 = Label(window, text="LS", font=("Arial Bold", 20), padx=15, pady=5, fg="black", bg="white")
mylabel14.place(x=300, y=400)

mylabel15 = Label(window, text="PP", font=("Arial Bold", 20), padx=15, pady=5, fg="black", bg="white")
mylabel15.place(x=500, y=300)

mylabel16 = Label(window, text="PT", font=("Arial Bold", 20), padx=15, pady=5, fg="black", bg="white")
mylabel16.place(x=500, y=500)

mylabel17 = Label(window, text="PS", font=("Arial Bold", 20), padx=15, pady=5, fg="black", bg="white")
mylabel17.place(x=500, y=400)


#utworzenie wątku sterującego robotem
def sterowanie():
    global lewy
    global prawy
    global zwrotnasilniki
    tab = ['~', '0', '0', '0', '#']
    spr='0'
    while True:
        if (keyboard.is_pressed('t') and not (keyboard.is_pressed('g'))):
            tab[1] = '3'  # przod
        elif (keyboard.is_pressed('g') and not (keyboard.is_pressed('t'))):
            tab[1] = '2'  # tylg
        else:
            tab[1] = '1'  # soft hamowanie

        if (keyboard.is_pressed('o') and not (keyboard.is_pressed('k'))):
            tab[2] = '3'  # przod
        elif (keyboard.is_pressed('k') and not (keyboard.is_pressed('o'))):
            tab[2] = '2'  # tylg
        else:
            tab[2] = '1'  # soft hamowanie

        if (tab[1]=='3' and tab[2]=='3'):
            spr='1'
        elif (tab[1]=='3' and tab[2]=='2'):
            spr='2'
        elif (tab[1] == '3' and tab[2] == '1'):
            spr = '3'
        elif (tab[1] == '2' and tab[2] == '3'):
            spr = '4'
        elif (tab[1] == '2' and tab[2] == '2'):
            spr = '5'
        elif (tab[1] == '2' and tab[2] == '1'):
            spr = '6'
        elif (tab[1] == '1' and tab[2] == '3'):
            spr = '7'
        elif (tab[1] == '1' and tab[2] == '2'):
            spr = '8'
        elif (tab[1] == '1' and tab[2] == '1'):
            spr = '9'

        t1 = int(tab[1])
        t2 = int(tab[2])
        t3 = ((t1 + t2) * (t1 + t2) * 177) % 7
        tab[3] = str(t3)

        if(spr!=zwrotnasilniki):
            for i in range(5):
                stm.write(bytes(tab[i], 'utf-8'))
        lewy=tab[1]
        prawy=tab[2]
        aktualizacjaBG1()
        time.sleep(0.01)

#utworzenie wątku odbierającego informacje o odczytach czujników
def odbieranie():
    global czujniki
    global stm
    global zwrotnasilniki
    buff = "00000000"
    while True:
        crc = 0
        start = stm.read()
        try:
            decoded_start = str(start[0:len(start)].decode("utf-8"))
            if (decoded_start == '~'):
                msg = stm.readline()

                try:
                    decoded_bytes = str(msg[0:len(msg)].decode("utf-8"))
                    for j in range(6):
                        crc = crc + int(decoded_bytes[j])

                    if (int(decoded_bytes[6]) == crc):
                        buff = decoded_bytes
                        print("otrzymany komunikat: ", buff)
                    else:
                        print("---")
                except Exception as ex:
                    pass

        except Exception as ex:
            pass

        for k in range(6):
            czujniki[k]=buff[k]
        zwrotnasilniki=buff[7]
        aktualizacjaBG2()
        time.sleep(0.01)

#uruchomienie wątków
Thread(target = sterowanie).start()
Thread(target = odbieranie).start()

#uruchomienie pętli GUI
window.mainloop()