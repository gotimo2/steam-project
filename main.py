import json
import os
from tkinter import *  # pylint:disable=unused-wildcard-import
from tkinter import ttk, messagebox
import steam_games
from steam_games import *  # pylint:disable=unused-wildcard-import
import time
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
from matplotlib import rcParams

# import gpio, als het beschikbaar is.
gpioMode = True
try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(0)
except:
    gpioMode = False

# maak window en maak een lokale """kopie""" van listofgames voor makkelijk gebruik en manipulatie
root = Tk()
root.title("Steam Tool")  # zet titel van window naar "Steam Tool"
listOfGames = steam_games.listOfGames


def raise_frame(frame):
    frame.tkraise()


# maak frames
f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)

# refereer naar de frames als "news"
for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, ipady=40, ipadx=35, sticky='news')

# maak canvas
C = Canvas(master=root, bg="blue", height=250, width=300)

# neem photoimage voor later?
filename = PhotoImage(file="steam image3.png")

# maak labels
background_label = Label(master=f1, image=filename)
background_label2 = Label(master=f2, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label2.place(x=0, y=0, relwidth=1, relheight=1)
background_label3 = Label(master=f3, image=filename)
background_label3.place(x=0, y=0, relwidth=1, relheight=1)
background_label4 = Label(master=f4, image=filename)
background_label4.place(x=0, y=0, relwidth=1, relheight=1)
C.pack

# maak label voor naam?
MenuLabel = Label(f1, text='Steam Tool', font=('Helvetica', 12, 'bold italic'), height=2, width=20)
MenuLabel.pack()

# maak menuknoppen
overzichtgames = Button(f1, text='Overzicht games', command=lambda: raise_frame(f2))
statistieken = Button(f1, text='Statistieken', command=lambda: raise_frame(f3))
vriendenlijst = Button(f1, text='Vriendenlijst', command=lambda: raise_frame(f4))
# pack de knoppen - bij maken direct packen is een slecht idee
for i in [overzichtgames, statistieken, vriendenlijst]:
    i.pack(pady=10)


# status weergave
def status_circle(x, y, r, icon_status, status):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    kleur = str
    if status == 'online':  # Checkt wat de status is en past kleur hierop aan (status zelf moet nog geimplenteerd worden)
        kleur = 'green'
    elif status == 'away':
        kleur = 'orange'
    elif status == 'offline':
        kleur = 'red'
    return icon_status.create_oval(x0, y0, x1, y1, fill=kleur)


# gebruiker status canvas
CanvasStatus = Canvas(f1)
CanvasStatus.pack(side=BOTTOM, anchor=SE)
CanvasStatus2 = Canvas(f2)
CanvasStatus2.pack(side=BOTTOM, anchor=SE)
CanvasStatus3 = Canvas(f3)
CanvasStatus3.pack(side=BOTTOM, anchor=SE)
CanvasStatus4 = Canvas(f4)
CanvasStatus4.pack(side=BOTTOM, anchor=SE)


# roept status_circle() aan
def icon(x):
    status = str
    if x == 0:
        status = 'online'
    elif x == 1:
        status = 'away'
    icon1 = (CanvasStatus)
    status_circle(80, 20, 7, icon1, status)
    icon2 = (CanvasStatus2)
    status_circle(80, 20, 7, icon2, status)
    icon3 = (CanvasStatus3)
    status_circle(80, 20, 7, icon3, status)
    icon4 = (CanvasStatus4)
    status_circle(80, 20, 7, icon4, status)


# gebruiker status labels
StatusGebruiker = Label(CanvasStatus, text='Status:')
StatusGebruiker.pack(side=BOTTOM, anchor=SE, pady=10, padx=20)
StatusGebruiker2 = Label(CanvasStatus2, text='Status:')
StatusGebruiker2.pack(side=BOTTOM, anchor=SE, pady=10, padx=20)
StatusGebruiker3 = Label(CanvasStatus3, text='Status:')
StatusGebruiker3.pack(side=BOTTOM, anchor=SE, pady=10, padx=20)
StatusGebruiker4 = Label(CanvasStatus4, text='Status:')
StatusGebruiker4.pack(side=BOTTOM, anchor=SE, pady=10, padx=20)


# dropdown menu status

# functie wanneer je optie kiest in menu
# def function(x):
#     if x == "Online":
#         print("Online")
#     elif x == "Away":
#         print("Away")
#     elif x == "Offline":
#         print("Offline")
#     elif x == "Real-time":
#         print("Real-time")
#
# #optie menu variabel
# optionVar = StringVar()
# #standaard status
# optionVar.set("Online")
#
# #de optie menu
# option = OptionMenu(CanvasStatus, optionVar, "Online","Away","Offline","Real-time", command=function)
# option.pack(side=BOTTOM,  anchor=SE)


# headingfuncties -Tedieus, uitgebreid, alleen nodig want tkinter commands.
# doen wat ze moeten doen tho ¯\_(ツ)_/¯
def name_heading():
    sortByName()
    refreshGames()


def rating_heading():
    sortByRating()
    refreshGames()


def price_heading():
    sortByPrice()
    refreshGames()


def age_heading():
    sortByAge()
    refreshGames()


def releaseDateHeading():
    sortByReleaseDate()
    refreshGames()


def appidHeading():
    sortByAppid()
    refreshGames()


# launch game functie
def launchGame():
    treeSelected = tree.focus()  # pak gefocuste item van de treeview
    valueList = list(tree.item(treeSelected).values())  # maak een list van de values ervan
    currentid = valueList[2][5]  # pak de steamid ervan
    # print(valueList[2][5]) #print de steamid
    os.system(f"start \"\" steam://run/{currentid}")  # open de steam://run voor de gekozen game


def reverseList():
    listOfGames.reverse()
    refreshGames()


# maak tree
# maak tree met scrollbar

tree_scroll = Scrollbar(f2)
tree_scroll.pack(side=RIGHT, fill=Y)
tree = ttk.Treeview(f2, yscrollcommand=tree_scroll.set,
                    column=("column1", "column2", "column3", "column4", "column5", "column6"), show='headings',
                    height=25)
tree_scroll.configure(command=tree.yview)

# configureer tree
tree.heading("#1", text="Naam", command=name_heading)
tree.heading("#2", text="Waardering", command=rating_heading)
tree.heading("#3", text="Prijs", command=price_heading)
tree.heading("#4", text="Leeftijd", command=age_heading)
tree.heading("#5", text="Uitkomstdatum", command=releaseDateHeading)
tree.heading("#6", text="AppID", command=appidHeading)

# plaats tree
tree.pack(pady=10, padx=10)
# maak tree met scrollbar

tree_scroll = Scrollbar(f4)
tree_scroll.pack(side=RIGHT, fill=Y)

tree2 = ttk.Treeview(f4, yscrollcommand=tree_scroll.set, height=25, column=(
    "column1", "column2", "column3", "column4", "column5", "column6", "column7", "column8", "column9", "column10","column11"),
                     show='headings')
tree_scroll.configure(command=tree.yview)
# configureer tree
tree2.heading("#1", text="gebruiker")
tree2.column("#1", minwidth=0, width=75, stretch=NO)
tree2.heading("#2", text="bijnaam")
tree2.column("#2", minwidth=0, width=75, stretch=NO)
tree2.heading("#3", text="vriendcode")
tree2.column("#3", minwidth=0, width=100, stretch=NO)
tree2.heading("#4", text="game")
tree2.column("#4", minwidth=0, width=75, stretch=NO)
tree2.heading("#5", text="speeltijd")
tree2.column("#5", minwidth=0, width=100, stretch=NO)
tree2.heading("#6", text="game ")
tree2.column("#6", minwidth=0, width=75, stretch=NO)
tree2.heading("#7", text="speeltijd")
tree2.column("#7", minwidth=0, width=100, stretch=NO)
tree2.heading("#8", text="game")
tree2.column("#8", minwidth=0, width=75, stretch=NO)
tree2.heading("#9", text="speeltijd")
tree2.column("#9", minwidth=0, width=75, stretch=NO)
tree2.heading("#10", text="status")
tree2.column("#10", minwidth=0, width=75, stretch=NO)
tree2.heading("#11", text="beste vriend?")
tree2.column("#11", minwidth=0, width=75, stretch=NO)

tree2


Label(f3, text='Top games bepaalde leeftijd:',foreground='#ffffff',background='#a52019', font=('Helvetica', 12, 'bold italic'), height=1, width=30).place(x=180,y=0)
Label(f3, text='Voer minimale en maximale rating in',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=1, width=30).place(x=180,y=25)
Label(f3, text='Voer minimale en maximale leeftijd in',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=1, width=30).place(x=180,y=50)
Label(f3, text='Wat is het begingetal  en wat is het eindgetal',foreground='#ffffff',background='#008080',font=('Helvetica', 12, 'bold italic'), height=1, width=35).place(x=180,y=75)
Label(f3, text='Vbld: top 100 begin bij nr 10 en eindig bij nr 30',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=1, width=35).place(x=180,y=100)
Label(f3, text='Klik voor grafiek',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=1, width=35).place(x=180,y=125)
Label(f3, text='Top games bepaalde prijs:',foreground='#ffffff',background='#a52019', font=('Helvetica', 12, 'bold italic'), height=1, width=30).place(x=560,y=0)
Label(f3, text='Voer minimale en maximale prijs in',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=1, width=30).place(x=560,y=25)
Label(f3, text='Voer minimale en maximale rating in',foreground='#ffffff',background='#008080',font=('Helvetica', 12, 'bold italic'), height=1, width=30).place(x=560,y=50)
Label(f3, text='Wat is het begingetal  en wat is het eindgetal',foreground='#ffffff',background='#008080',font=('Helvetica', 12, 'bold italic'), height=1, width=35).place(x=560,y=75)
Label(f3, text='Klik voor grafiek',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=1, width=35).place(x=560,y=100)

Label(f3, text='Top games bepaalde prijs met leeftijdsgrens:',foreground='#ffffff',background='#a52019', font=('Helvetica', 12, 'bold italic'), height=1, width=35).place(x=940,y=0)
Label(f3, text='Voer minimale en maximale prijs in',foreground='#ffffff',background='#008080',font=('Helvetica', 12, 'bold italic'), height=1, width=30).place(x=940,y=25)
Label(f3, text='Voer minimale en maximale leeftijd in',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=1, width=30).place(x=940,y=50)
Label(f3, text='Voer minimale en maximale rating in',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=1, width=30).place(x=940,y=75)
Label(f3, text='Wat is het begingetal  en wat is het eindgetal',foreground='#ffffff',background='#008080',font=('Helvetica', 12, 'bold italic'), height=1, width=35).place(x=940,y=100)
Label(f3, text='Klik voor grafiek',foreground='#ffffff',background='#008080',font=('Helvetica', 12, 'bold italic'), height=1, width=35).place(x=940,y=125)

Label(f3, text='Geef minimum rating',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=1, width=20).place(x=175,y=153)
entry2 = Entry(master=f3)
entry2.place(x=180,y=180)
Label(f3, text='Geef maximum rating',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=1, width=20).place(x=375,y=153)
entry1 = Entry(master=f3)
entry1.place(x=380,y=180)
Label(f3, text='Geef minimum price',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=1, width=20).place(x=560,y=153)
entry4 = Entry(master=f3)
entry4.place(x=560,y=180)
Label(f3, text='Geef maximum price',foreground='#ffffff',background='#008080',font=('Helvetica', 12, 'bold italic'), height=1, width=20).place(x=740,y=153)
entry3 = Entry(master=f3)
entry3.place(x=740,y=180)
Label(f3, text='Geef minimum leeftiijd',foreground='#ffffff',background='#008080',font=('Helvetica', 12, 'bold italic'), height=1, width=20).place(x=180,y=240)
entry6 = Entry(master=f3)
entry6.place(x=180,y=280)
Label(f3, text='Geef maximum leeftiijd',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=1, width=20).place(x=380,y=240)
entry5 = Entry(master=f3)
entry5.place(x=400,y=280)
Label(f3, text='Geef het begingetal',foreground='#ffffff',background='#008080',font=('Helvetica', 12, 'bold italic'), height=1, width=20).place(x=590,y=240)
entry8 = Entry(master=f3)
entry8.place(x=560,y=280)
Label(f3, text='Geef het eindgetal',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=1, width=20).place(x=770,y=240)
entry9 = Entry(master=f3)
entry9.place(x=740,y=280)
Label(f3, text='Klik hier voor de topgames\n voor een bepaalde leeftijd.',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=2, width=21).place(x=180,y=360)
Label(f3, text='Klik hier voor de topgames\n voor een bepaalde prijs.',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=2, width=20).place(x=420,y=360)
Label(f3, text='Klik hier voor de topgames\n voor een bepaalde prijs\n met een leeftijdsgrens.',foreground='#ffffff',background='#008080', font=('Helvetica', 12, 'bold italic'), height=3, width=20).place(x=180,y=480)

#statistiek labels
Label(f3, text='Gemiddelde rating:\n' + str(mean(makeList('rating')))+'\n Meest voorkomende rating:\n'+ str(modes(makeList('rating'))[0])+'\n Standaardeviatie rating:\n' +str(std(makeList('rating')))+'\nVariantie rating:\n'+str(var(makeList('rating')))+'\nMediaan rating:\n'+str(median(makeList('rating'))),foreground='#ffffff',background='#a52019', font=('Helvetica', 12, 'bold italic'), height=10, width=25).place(x=700,y=480)
Label(f3, text='Gemiddelde prijs:\n' + str(mean(makeList('price')))+'\n Meest voorkomende prijs:\n'+ str(modes(makeList('price'))[0])+'\n Standaardeviatie prijs:\n' +str(std(makeList('price')))+'\nVariantie prijs:\n'+str(var(makeList('price')))+'\nMediaan prijs:\n'+str(median(makeList('price'))),foreground='#ffffff',background='#a52019', font=('Helvetica', 12, 'bold italic'), height=10, width=25).place(x=1000,y=480)






def vriendtoevoegen():
    x = random.randrange(0, 2)
    if x == 0:
        y = 'offline'
    if x == 1:
        y = 'online'
    bestand = 'vriendenlijst.json'
    with open(bestand, 'r+') as lezen:
        data = json.load(lezen)
    naam = entry7.get()
    name = entry7.get()
    data.append({
        'naam': naam,
        'name': name,
        'vriendcode': random.randrange(1000000, 10000000),
        'game1': getattr(random.choice(listOfGames), 'name'),
        'game1st': random.randrange(0, 100),
        'game2': getattr(random.choice(listOfGames), 'name'),
        'game2st': random.randrange(0, 100),
        'game3': getattr(random.choice(listOfGames), 'name'),
        'game3st': random.randrange(0, 100),
        'status': y})
    with open(bestand, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    entry7.delete(0, END)
    messagebox.showinfo('Succes', 'Vriend is toegevoegd aan vriendenlijst.')


def addBestFriend():
    treeSelected = tree2.focus()  # pak gefocuste item van de treeview
    valueList2 = list(tree2.item(treeSelected).values())  # maak een list van de values ervan
    bestand = 'bestevrienden.json'
    vriendcodes = []
    with open(bestand, 'r+') as lezen:
        besteVrienden = json.load(lezen)
    for x in range(len(besteVrienden)):
        vriendcodes.append(besteVrienden[x]['vriendcode'])
    if len(besteVrienden) < 4:
        if valueList2[2][2] not in vriendcodes:
            besteVrienden.append({
                'naam': valueList2[2][0],
                'name': valueList2[2][1],
                'vriendcode': valueList2[2][2],
                'game1': valueList2[2][3],
                'game1st': valueList2[2][4],
                'game2': valueList2[2][5],
                'game2st': valueList2[2][6],
                'game3': valueList2[2][7],
                'game3st': valueList2[2][8],
                'status': valueList2[2][9]})
            with open(bestand, 'w') as outfile:
                json.dump(besteVrienden, outfile, indent=4)
            messagebox.showinfo('Succes', 'Vriend is toegevoegd aan je beste vriendenlijst.')
        else:
            messagebox.showinfo('Foutmelding', 'Deze vriend staat al in je beste vriendenlijst.')
    else:
        messagebox.showinfo('Foutmelding',
                            'Je hebt al het maximumaantal (4) beste vrienden in je lijst staan. Verwijder eerst een vriend en probeer het opnieuw.')
if gpioMode:
    def pulse(pin, delay1, delay2):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(delay1)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(delay2)


    def servo_pulse(pin_nr, position):
        pulse(pin_nr, 0.0005 + (position * 0.00002), 0.02)


    def startServo(status):
        if status == 1:
            for i in range(0, 100, 3):
                servo_pulse(servo, i)
        else:
            for i in range(100, 0, -3):
                servo_pulse(servo, i)


def removeBestFriend():
    bestand = 'bestevrienden.json'
    verwijderDoel = tree2.focus()
    valueList = list(tree2.item(verwijderDoel).values())
    verwijder = valueList[2][1]
    with open(bestand, 'r+') as lezen:
        besteVrienden = json.load(lezen)
    lezen.close()
    namen = []
    for b in range(0, len(besteVrienden)):
        namen.append(besteVrienden[b]['naam'])
    print(namen)
    if verwijder in namen:
        for i in range(0, len(besteVrienden)):
            if verwijder == besteVrienden[i]['naam']:
                if gpioMode:
                    messagebox.showinfo('info', 'druk op ok en daarna op de knop om vriend te verwijderen')
                    while True:
                        if GPIO.input(23):
                            del besteVrienden[i]
                            startServo(1)
                            time.sleep(1)
                            startServo(0)
                            break
                        time.sleep(0.1)
                    break
                else:
                    del besteVrienden[i]
                    break
    else:
        messagebox.showinfo('error', 'vriend staat niet in beste vriendenlijst')

    with open(bestand, 'w') as outfile:
        json.dump(besteVrienden, outfile, indent=4)


def makenleeftijdlijsten():
    y = filterByAge(int(entry5.get()),int(entry6.get()))
    x = filterByRating2(y, int(entry2.get()), int(entry1.get()))
    z = quicksort(x, "rating")
    z.reverse()
    namen = []
    rating = []
    for i in z:
        namen.append(i.name)
        rating.append(i.rating)
    plt.figure(figsize=[7, 3])
    namen2 = namen[int(entry8.get()):int(entry9.get())]
    rating2 = rating[int(entry8.get()):int(entry9.get())]
    positie = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, ]
    plt.barh(namen2, rating2)
    plt.xlabel('Rating')
    plt.ylabel('Games')
    plt.title('Top 20 games')
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.tight_layout()
    plt.show()


def makenprijslijsten():
    y = filterByPrice(float(entry4.get()),float(entry3.get()))
    x = filterByRating2(y, float(entry2.get()), float(entry1.get()))
    z = quicksort(x, "rating")
    z.reverse()
    namen = []
    rating = []
    for i in z:
        namen.append(i.name)
        rating.append(i.rating)
    plt.figure(figsize=[7, 3])
    namen2 = namen[int(entry8.get()):int(entry9.get())]
    prijzen2 = rating[int(entry8.get()):int(entry9.get())]
    positie = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ]
    plt.barh(namen2, prijzen2)
    plt.xlabel('Rating')
    plt.ylabel('Games')
    plt.title('Top 20 games')
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.tight_layout()
    plt.show()


def makenprijslijstenmetleeftijd():
    y = filterByPrice(int(entry4.get()),int(entry3.get()))
    x = filterByRating2(y, int(entry2.get()), int(entry1.get()))
    r=filterByAge2(x,int(entry6.get()),int(entry5.get()))
    z = quicksort(r, "price")
    z.reverse()
    namen = []
    prijzen = []
    for i in z:
        namen.append(i.name)
        prijzen.append(i.price)
    plt.figure(figsize=[7, 3])
    namen2=namen[int(entry8.get()):int(entry9.get())]
    prijzen2=prijzen[int(entry8.get()):int(entry9.get())]
    plt.barh(namen2, prijzen2)
    plt.xlabel('Rating')
    plt.ylabel('Games')
    plt.title(
        'Top 20 games for people between the age of' + ' ' + str(entry6.get()) + ' ' + 'and' + ' ' + str(entry5.get()))
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.tight_layout()
    plt.show()



button1=Button(master=f3,command=lambda: makenprijslijsten(),text="Maak prijslijsten")
button1.place(x=470,y=420)
button2=Button(master=f3,command=lambda: makenleeftijdlijsten(),text="Maak leeftijd lijsten")
button2.place(x=220,y=420)
button3=Button(master=f3,command=lambda: makenprijslijstenmetleeftijd(),text="Maak prijslijsten met leeftijd")
button3.place(x=220,y=560)

def animate():
    games = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    prijzen = [9.99, 42.00, 25.00, 9.99, 42.00, 25.00, 9.99, 42.00, 25.00, 9.99, 42.00, 25.00, 9.99, 42.00, 25.00,
               9.99, 42.00, 25.00, 9.99, 42.00, 8]
    positie = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    plt.bar(positie, prijzen, width=0.5)
    plt.xticks(positie, games)

    plt.show()


def insertment():
    def tree2insert(naam,name,vriendcode,game1,game1st,game2,game2st,game3,game3st,status,bestevriend):
        tree2.pack(pady=10, padx=10)
        tree2.insert(parent='', index='end', text="game",
                     values=(naam,name,vriendcode,game1,game1st,game2,game2st,game3,game3st,status,bestevriend))
    bestand = 'vriendenlijst.json'
    bestevrienden='bestevrienden.json'
    with open(bestevrienden, 'r+') as openen:
        bestevriendendata = json.load(openen)
    y=[]
    for a in range(len(bestevriendendata)):
        y.append(bestevriendendata[a]['naam'])
    with open(bestand, 'r+') as lezen:
        vriendendata = json.load(lezen)
    i = vriendendata
    for x in range(len(i)):
        naam = i[x]['naam']
        name=i[x]['name']
        vriendcode = i[x]['vriendcode']
        game1 = i[x]['game1']
        game1st = i[x]['game1st']
        game2 = i[x]['game2']
        game2st = i[x]['game2st']
        game3 = i[x]['game3']
        game3st = i[x]['game3st']
        status = i[x]['status']
        if naam in y:
            bestevriend = 'ja'
        else:
            bestevriend = 'nee'

        tree2insert(naam,name,vriendcode,game1,game1st,game2,game2st,game3,game3st,status,bestevriend)


insertment()


def refreshvrienden():
    tree2.delete(*tree2.get_children())
    insertment()  # leeg de tree


lijstmetgamesvriend1 = ['Cities:Skylines', 'F1 2018', 'We Were Here Together']
lijstmetgamesvriend2 = ['The Forest', 'Hollow Knight', 'F1 2018']
lijstmetgamesvriend3 = ['Portal2', 'Tomb Raider', 'F1 2018']
lijstmetgamesvriend4 = ['Stardew Valley', 'Rust', 'F1 2018']

# plaats tree


#
# tree2insert('Pascal')
# tree2insert('Sven')
# tree2insert('Kyrill')
# tree2insert('David')

##knoppen om te sorteren, --moeten naar heading veranderd worden-- zijn nu naar heading veranderd, dus onnodig. ik hou ze hier gewoon voor het geval dat.
# Button(f2, text='Sorteer op naam', command=sortByName).pack(pady=10)
# Button(f2, text='Sorteer games op uitkomstdatum', command=sortByReleaseDate).pack(pady=10)
# Button(f2, text='Sorteer games op geschikte leeftijd', command=sortByAge).pack(pady=10)
# Button(f2, text='Sorteer games op prijs', command=sortByPrice).pack(pady=10)
# Button(f2, text='Sorteer games op Waardering', command=sortByRating).pack(pady=10)
# Button(f2, text='Sorteer games op datum AppID', command=sortByAppid).pack(pady=10)


# knop voor steam launch en lijst omdraaien
Button(f2, text='Start game', command=launchGame).pack(pady=10, side=BOTTOM)
Button(f2, text='Lijst omkeren', command=reverseList).pack(pady=10)

# knoppen en labels voor welkom en teruggaan
Button(f2, text='Terug', command=lambda: raise_frame(f1)).pack(pady=10)

Button(f3, text='Terug', command=lambda: raise_frame(f1)).pack(pady=10, side=BOTTOM)

Button(f4, text='Terug', command=lambda: raise_frame(f1)).pack(pady=10, side=BOTTOM)
Button(f4, text='Verwijder beste vriend', command=removeBestFriend).pack(pady=10, side=BOTTOM)
Button(f4, text='Voeg toe aan beste vrienden', command=addBestFriend).pack(pady=10, side=BOTTOM)
Button(master=f4, text='Voeg vriend toe:', command=vriendtoevoegen).pack(pady=10, side=BOTTOM)
Button(master=f4, text='Refresh', command=refreshvrienden).pack(pady=10, side=BOTTOM)
entry7 = Entry(master=f4)
entry7.place(x=730, y=736)
entry7.insert(END, 'naam vriend')

filterEntry = Entry(f2)
filterEntry.pack(padx=20, pady=30)


# filterPicker = OptionMenu(f2, 'naam', 'waardering', 'prijs', 'minimumleeftijd', 'appID', 'uitkomstdatum')
# filterPicker.pack(padx = 20, pady = 30)

def refreshGames(refreshList=listOfGames):
    tree.delete(*tree.get_children())  # leeg de tree
    for i in refreshList:  # plaats de list opnieuw
        tree.insert(parent='', index='end', iid=i.appid, text="game",
                    values=(i.name, round(i.rating, 2), i.price, i.required_age, i.release_date, i.appid))


refreshGames()

sortByAppid()
# print(listOfGames[0].name)

# def refreshLabelLoop():
# root.after(50, refreshLabelLoop)

"""""
-----------------------------------------------------------
                                TI COMPONENT CODES
-----------------------------------------------------------
"""""

if gpioMode:
    # Pins voor de sensor
    sr04_trig = 20
    sr04_echo = 21

    GPIO.setup(sr04_trig, GPIO.OUT)
    GPIO.setup(sr04_echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    def AfstandSensor(trig_pin, echo_pin):  # Checkt of gebruiker achter pc zit en past de status aan.
        GPIO.output(trig_pin, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(trig_pin, GPIO.LOW)

        while GPIO.input(echo_pin) == False:
            begin = time.time()

        while GPIO.input(echo_pin) == True:
            eind = time.time()
            tijd = eind - begin
            afstand_cm = tijd * 17165
        return afstand_cm


else:
    pass
if gpioMode:
    clock_pin = 19
    data_pin = 26
    servo = 25
    GPIO.setup(servo, GPIO.OUT)
    GPIO.setup(clock_pin, GPIO.OUT)
    GPIO.setup(data_pin, GPIO.OUT)


    def apa102_send_bytes(clock_pin, data_pin, bytes):
        for byte in bytes:
            for bit in byte:
                if bit == 1:
                    GPIO.output(data_pin, GPIO.HIGH)
                    GPIO.output(clock_pin, GPIO.HIGH)
                    GPIO.output(clock_pin, GPIO.LOW)
                elif bit == 0:
                    GPIO.output(data_pin, GPIO.LOW)
                    GPIO.output(clock_pin, GPIO.HIGH)
                    GPIO.output(clock_pin, GPIO.LOW)


    def apa102(clock_pin, data_pin, x):
        l = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        b = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
        rood = [[1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1]]
        groen = [[1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]]
        oranje = [[1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 1, 1, 1, 1, 1]]
        uit = [[1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]

        if x == 0:
            apa102_send_bytes(clock_pin, data_pin, l)
            apa102_send_bytes(clock_pin, data_pin, groen * 8)
            apa102_send_bytes(clock_pin, data_pin, b)
        #     elif status == 'offline':
        #         apa102_send_bytes(clock_pin, data_pin, l)
        #         apa102_send_bytes(clock_pin, data_pin, rood * 8)
        #         apa102_send_bytes(clock_pin, data_pin, b)
        if x == 1:
            apa102_send_bytes(clock_pin, data_pin, l)
            apa102_send_bytes(clock_pin, data_pin, oranje * 8)
            apa102_send_bytes(clock_pin, data_pin, b)


    #     elif status == 'off':
    #         apa102_send_bytes(clock_pin, data_pin, l)
    #         apa102_send_bytes(clock_pin, data_pin, uit * 8)
    #         apa102_send_bytes(clock_pin, data_pin, b)

    def Refresh_status():
        if AfstandSensor(sr04_trig, sr04_echo) > 70:  # Gebruiker van pc dus status op 'away'
            icon(1)
            apa102(clock_pin, data_pin, 1)
        else:
            icon(0)
            apa102(clock_pin, data_pin, 0)
        root.after(10000, Refresh_status)


    Refresh_status()
else:
    pass

if gpioMode:
    shift_clock_pin = 5
    latch_clock_pin = 6
    data_pin = 13

    GPIO.setup(shift_clock_pin, GPIO.OUT)
    GPIO.setup(latch_clock_pin, GPIO.OUT)
    GPIO.setup(data_pin, GPIO.OUT)


    def checkOnline():
        bestand = 'bestevrienden.json'
        aantal = 0
        with open(bestand, 'r+') as lezen:
            besteVrienden = json.load(lezen)
            lezen.close()
        for i in range(len(besteVrienden)):
            if besteVrienden[i]['status'] == 'online':
                aantal += 1
        print(f'{aantal} vrienden online')
        return aantal


    def hc595(shift_clock_pin, latch_clock_pin, data_pin, value, delay):
        for _ in range(4):
            if value % 2 == 1:
                GPIO.output(data_pin, GPIO.HIGH)
            else:
                GPIO.output(data_pin, GPIO.LOW)
            GPIO.output(shift_clock_pin, GPIO.HIGH)
            GPIO.output(shift_clock_pin, GPIO.LOW)
            value = value // 2

        GPIO.output(latch_clock_pin, GPIO.HIGH)
        GPIO.output(latch_clock_pin, GPIO.LOW)
        time.sleep(delay)


    def aantalOnline():
        aantal = checkOnline()
        delay = 0.1
        if aantal == 0:
            hc595(shift_clock_pin, latch_clock_pin, data_pin, 0, delay)
        elif aantal == 1:
            hc595(shift_clock_pin, latch_clock_pin, data_pin, 8, delay)
        elif aantal == 2:
            hc595(shift_clock_pin, latch_clock_pin, data_pin, 12, delay)
        elif aantal == 3:
            hc595(shift_clock_pin, latch_clock_pin, data_pin, 14, delay)
        elif aantal == 4:
            hc595(shift_clock_pin, latch_clock_pin, data_pin, 15, delay)


    hc595(shift_clock_pin, latch_clock_pin, data_pin, 0, 0.1)

    Button(f4, text='Check aantal online beste vrienden', command=aantalOnline).pack(pady=10, side=BOTTOM)
else:
    pass
# for i in filterByPrice(12, 10):
#    print(f'{i.name}, {i.price}\n')

# run window
raise_frame(f1)
root.mainloop()
