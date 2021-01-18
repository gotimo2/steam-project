import os
from tkinter import *  # pylint:disable=unused-wildcard-import
from tkinter import ttk
import steam_games
from steam_games import *  # pylint:disable=unused-wildcard-import
import time

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
"column1", "column2", "column3", "column4", "column5", "column6", "column7", "column8", "column9","column10"), show='headings')
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


tree2




Label(f3, text='geef maximum rating', font=('Helvetica', 12, 'bold italic'), height=1, width=20).place(x=180,y=63)
entry1 = Entry(master=f3)
entry1.place(x=180,y=90)
Label(f3, text='geef minimum rating', font=('Helvetica', 12, 'bold italic'), height=1, width=20).place(x=380,y=63)
entry2 = Entry(master=f3)
entry2.place(x=380,y=90)
Label(f3, text='geef maximum price', font=('Helvetica', 12, 'bold italic'), height=1, width=20).place(x=560,y=63)
entry3 = Entry(master=f3)
entry3.place(x=560,y=90)
Label(f3, text='geef minimum price', font=('Helvetica', 12, 'bold italic'), height=1, width=20).place(x=740,y=63)
entry4 = Entry(master=f3)
entry4.place(x=740,y=90)
Label(f3, text='geef maximum leeftiijd', font=('Helvetica', 12, 'bold italic'), height=1, width=20).place(x=180,y=160)
entry5 = Entry(master=f3)
entry5.place(x=180,y=180)
Label(f3, text='geef minimum leeftiijd', font=('Helvetica', 12, 'bold italic'), height=1, width=20).place(x=400,y=160)
entry6 = Entry(master=f3)
entry6.place(x=400,y=180)
entry7=Entry(master=f4)
entry7.place(x=400,y=180)

def vriendtoevoegen():
    x=random.randrange(0,2)
    if x ==0:
        y='offline'
    if x==1:
        y='online'
    bestand = 'vriendenlijst.json'
    with open(bestand, 'r+') as lezen:
        data = json.load(lezen)
    naam = entry7.get()
    name=entry7.get()
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
        json.dump(data,outfile,indent=4)
button=Button(master=f4,text='geef naam vriend',command=lambda: vriendtoevoegen())
button.place(x=180,y=180)

def makenleeftijdlijsten():
    y = filterByAge(int(entry5.get()),int(entry6.get()))
    x = filterByRating2(y, int(entry1.get()), int(entry2.get()))
    z = quicksort(x, "rating")
    z.reverse()
    namen = []
    rating = []
    for i in z:
        namen.append(i.name)
        rating.append(i.rating)
    plt.figure(figsize=[7, 3])
    namen2 = namen[:20]
    rating2 = rating[:20]
    positie = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, ]
    plt.barh(namen2, rating2)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.tight_layout()
    plt.show()





def makenprijslijsten():
    y = filterByPrice(float(entry3.get()),float(entry4.get()))
    x = filterByRating2(y, float(entry1.get()), float(entry2.get()))
    z = quicksort(x, "rating")
    z.reverse()
    namen = []
    rating = []
    for i in z:
        namen.append(i.name)
        rating.append(i.rating)
    plt.figure(figsize=[7, 3])
    namen2 = namen[:10]
    prijzen2 = rating[:10]
    positie = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ]
    plt.barh(namen2, prijzen2)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.tight_layout()
    plt.show()

def makenprijslijstenmetprijs():
    y = filterByPrice(int(entry3.get()),int(entry4.get()))
    x = filterByRating2(y, int(entry1.get()), int(entry2.get()))
    r=filterByAge(x,int(entry5.get()),int(entry6.get()))
    z = quicksort(r, "price")
    z.reverse()
    namen = []
    prijzen = []
    for i in z:
        namen.append(i.name)
        prijzen.append(i.price)
    plt.figure(figsize=[7, 3])
    namen2=namen[:10]
    prijzen2=prijzen[:10]
    plt.barh(namen2, prijzen2)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.tight_layout()
    plt.show()





button1=Button(master=f3,command=lambda: makenprijslijsten(),text="makenprijslijsten")
button1.pack()
button2=Button(master=f3,command=lambda: makenleeftijdlijsten(),text="makenleeftijdlijsten")
button2.pack()
button3=Button(master=f3,command=lambda: makenprijslijstenmetprijs(),text="makenprijslijstenmetprijs")
button3.pack()

def animate():

    games = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    prijzen = [9.99, 42.00, 25.00, 9.99, 42.00, 25.00, 9.99, 42.00, 25.00, 9.99, 42.00, 25.00, 9.99, 42.00, 25.00,
               9.99, 42.00, 25.00, 9.99, 42.00, 8]
    positie=[1,2,3,4,5,6,7,8,9,10]
    plt.bar(positie,prijzen,width=0.5)
    plt.xticks(positie, games)

    plt.show()




def insertment():
    def tree2insert(naam,name,vriendcode,game1,game1st,game2,game2st,game3,game3st,status):
        tree2.pack(pady=10, padx=10)
        tree2.insert(parent='', index='end', text="game",
                     values=(naam,name,vriendcode,game1,game1st,game2,game2st,game3,game3st,status))
    bestand = 'vriendenlijst.json'
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
        tree2insert(naam,name,vriendcode,game1,game1st,game2,game2st,game3,game3st,status)


insertment()

def refreshvrienden():
    tree2.delete(*tree2.get_children())
    insertment()# leeg de tree
button=Button(master=f4,text='refresh',command=lambda: refreshvrienden())
button.place(y=500,x=500)

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
Label(f3, text='Welkom', font=('Helvetica', 12, 'bold italic'), height=2, width=20).pack()
Button(f3, text='Terug', command=lambda: raise_frame(f1)).pack(pady=10)
Label(f4, text='Welkom', font=('Helvetica', 12, 'bold italic'), height=2, width=20).pack()
Button(f4, text='Terug', command=lambda: raise_frame(f1)).pack(pady=10)

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


    def Refresh_status():
        if AfstandSensor(sr04_trig, sr04_echo) > 70:  # Gebruiker van pc dus status op 'away'
            icon(1)
        else:
            icon(0)
        root.after(10000, Refresh_status)


    Refresh_status()
else:
    pass
if gpioMode:
    clock_pin = 19
    data_pin = 26

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


    def apa102(clock_pin, data_pin):
        l = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        b = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
        rood = [[1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]]
        groen = [[1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]]
        oranje = [[1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 1, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
        uit = [[1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]

        if AfstandSensor(sr04_trig, sr04_echo) < 70:
            apa102_send_bytes(clock_pin, data_pin, l)
            apa102_send_bytes(clock_pin, data_pin, groen * 8)
            apa102_send_bytes(clock_pin, data_pin, b)
        #     elif status == 'offline':
        #         apa102_send_bytes(clock_pin, data_pin, l)
        #         apa102_send_bytes(clock_pin, data_pin, rood * 8)
        #         apa102_send_bytes(clock_pin, data_pin, b)
        elif AfstandSensor(sr04_trig, sr04_echo) > 70:
            apa102_send_bytes(clock_pin, data_pin, l)
            apa102_send_bytes(clock_pin, data_pin, oranje * 8)
            apa102_send_bytes(clock_pin, data_pin, b)


    #     elif status == 'off':
    #         apa102_send_bytes(clock_pin, data_pin, l)
    #         apa102_send_bytes(clock_pin, data_pin, uit * 8)
    #         apa102_send_bytes(clock_pin, data_pin, b)


    def RefreshLEDstrip():
        apa102(clock_pin, data_pin)
        root.after(1000, RefreshLEDstrip)


    RefreshLEDstrip()
else:
    pass

# for i in filterByPrice(12, 10):
#    print(f'{i.name}, {i.price}\n')

# run window
raise_frame(f1)
root.mainloop()
