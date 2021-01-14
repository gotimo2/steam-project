import os
from tkinter import *  # pylint:disable=unused-wildcard-import
from tkinter import ttk
import steam_games
from steam_games import *  # pylint:disable=unused-wildcard-import
import time
#import RPI.GPIO as GPIO
#GPIO.setmode(GPIO.BCM)
# maak window en maak een lokale """kopie""" van listofgames voor makkelijk gebruik en manipulatie
root = Tk()
root.title("Steam Tool") #zet titel van window naar "Steam Tool"
listOfGames = steam_games.listOfGames

def raise_frame(frame):
    frame.tkraise()

#maak frames
f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)

#refereer naar de frames als "news"
for frame in (f1,f2, f3, f4):
    frame.grid(row=0, column=0, ipady=40, ipadx=35, sticky='news')

#maak canvas
C = Canvas(master=root, bg="blue", height=250, width=300)

#neem photoimage voor later?
filename = PhotoImage(file="steam image3.png")

#maak labels
background_label = Label(master=f1, image=filename)
background_label2 = Label(master=f2, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label2.place(x=0, y=0, relwidth=1, relheight=1)
background_label3 = Label(master=f3, image=filename)
background_label3.place(x=0, y=0, relwidth=1, relheight=1)
background_label4 = Label(master=f4, image=filename)
background_label4.place(x=0, y=0, relwidth=1, relheight=1)
C.pack

#maak label voor naam?
MenuLabel = Label(f1, text='Steam Tool', font=('Helvetica', 12, 'bold italic'), height=2, width=20)
MenuLabel.pack()

#maak menuknoppen
overzichtgames = Button(f1, text='Overzicht games', command=lambda: raise_frame(f2))
statistieken = Button(f1, text='Statistieken', command=lambda: raise_frame(f3))
vriendenlijst = Button(f1, text='Vriendenlijst', command=lambda: raise_frame(f4))
#pack de knoppen - bij maken direct packen is een slecht idee
for i in [overzichtgames, statistieken, vriendenlijst]:
    i.pack(pady=10)

# status weergave
def status_circle(x, y, r, icon_status):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    # if status == 'online': #Checkt wat de status is en past kleur hierop aan (status zelf moet nog geimplenteerd worden)
    #     kleur = 'green'
    # elif status == 'away':
    #     kleur = 'yellow'
    # elif status == 'offline':
    #     kleur = 'white'
    return icon_status.create_oval(x0, y0, x1, y1, fill='green')

#gebruiker status canvas
CanvasStatus = Canvas(f1)
CanvasStatus.pack(side=BOTTOM,  anchor=SE)
CanvasStatus2 = Canvas(f2)
CanvasStatus2.pack(side=BOTTOM, anchor=SE)
CanvasStatus3= Canvas(f3)
CanvasStatus3.pack(side=BOTTOM, anchor=SE)
CanvasStatus4 = Canvas(f4)
CanvasStatus4.pack(side=BOTTOM, anchor=SE)

#roept status_circle() aan
icon1 = (CanvasStatus)
icoon1 = status_circle(70, 20, 7, icon1)
icon2 = (CanvasStatus2)
icoon2 = status_circle(70, 20, 7, icon2)
icon3 = (CanvasStatus3)
icoon3 = status_circle(70, 20, 7, icon3)
icon4 = (CanvasStatus4)
icoon4 = status_circle(70, 20, 7, icon4)

#gebruiker status labels
StatusGebruiker = Label(CanvasStatus, text= 'Status:')
StatusGebruiker.pack(side=BOTTOM, anchor=SE,pady=10,padx=20)
StatusGebruiker2 = Label(CanvasStatus2, text= 'Status:')
StatusGebruiker2.pack(side=BOTTOM, anchor=SE,pady=10,padx=20)
StatusGebruiker3 = Label(CanvasStatus3, text= 'Status:')
StatusGebruiker3.pack(side=BOTTOM, anchor=SE,pady=10,padx=20)
StatusGebruiker4 = Label(CanvasStatus4, text= 'Status:')
StatusGebruiker4.pack(side=BOTTOM, anchor=SE,pady=10,padx=20)

#headingfuncties -Tedieus, uitgebreid, alleen nodig want tkinter commands.
#doen wat ze moeten doen tho ¯\_(ツ)_/¯
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

#launch game functie
def launchGame():
    treeSelected = tree.focus() #pak gefocuste item van de treeview
    valueList = list(tree.item(treeSelected).values()) #maak een list van de values ervan
    currentid = valueList[2][5] #pak de steamid ervan
    #print(valueList[2][5]) #print de steamid
    os.system(f"start \"\" steam://run/{currentid}") #open de steam://run voor de gekozen game

def reverseList():
    listOfGames.reverse()
    refreshGames()

#maak tree
#maak tree met scrollbar

tree_scroll=Scrollbar(f2)
tree_scroll.pack(side=RIGHT,fill=Y)
tree = ttk.Treeview(f2,yscrollcommand=tree_scroll.set, column=("column1", "column2", "column3","column4", "column5", "column6"), show='headings', height=25)
tree_scroll.configure(command=tree.yview)

#configureer tree
tree.heading("#1", text="Naam", command=name_heading)
tree.heading("#2", text="Waardering", command=rating_heading)
tree.heading("#3", text="Prijs", command=price_heading)
tree.heading("#4", text="Leeftijd", command=age_heading)
tree.heading("#5", text="Uitkomstdatum", command=releaseDateHeading)
tree.heading("#6", text="AppID", command=appidHeading)


#plaats tree
tree.pack(pady=10, padx=10)
#maak tree met scrollbar

tree_scroll=Scrollbar(f4)
tree_scroll.pack(side=RIGHT,fill=Y)

tree2= ttk.Treeview(f4,yscrollcommand=tree_scroll.set,height=25, column=("column1", "column2", "column3","column4", "column5", "column6","column7","column8","column9"), show='headings')
tree_scroll.configure(command=tree.yview)
#configureer tree
tree2.heading("#1", text="Naam")
tree2.column("#1", minwidth=0, width=100, stretch=NO)
tree2.heading("#2", text="gebruiker")
tree2.column("#2", minwidth=0, width=75, stretch=NO)

tree2.heading("#3", text="vriendcode")
tree2.column("#3", minwidth=0, width=75, stretch=NO)
tree2.heading("#4", text="game")
tree2.column("#4", minwidth=0, width=100, stretch=NO)
tree2.heading("#5", text="speeltijd")
tree2.column("#5", minwidth=0, width=75, stretch=NO)
tree2.heading("#6", text="game")
tree2.column("#6", minwidth=0, width=100, stretch=NO)
tree2.heading("#7", text="speeltijd ")
tree2.column("#7", minwidth=0, width=75, stretch=NO)
tree2.heading("#8", text="game")
tree2.column("#8", minwidth=0, width=100, stretch=NO)
tree2.heading("#9", text="speeltijd")
tree2.column("#9", minwidth=0, width=75, stretch=NO)



tree2






lijstmetgamesvriend1=['Cities:Skylines','F1 2018','We Were Here Together']
lijstmetgamesvriend2=['The Forest','Hollow Knight','F1 2018']
lijstmetgamesvriend3=['Portal2','Tomb Raider','F1 2018']
lijstmetgamesvriend4=['Stardew Valley','Rust','F1 2018']


vriendenlijst=['Sven' ,'Svenno02',184596,'Cities:Skylines', 1.5,'F1 2018', 2.5, 'Everything', 5]
vriendenlijst2=['Pascal' ,'Pascal134', 174595,   'The Forest', 30, 'Hollow Knight', 0.5, 'F1 2018', 30]
vriendenlijst3=['Kyrill', 'Koraal', 937592,  'Portal2', 21, 'Tomb Raider', 12.5, 'F1 2018', 25]
vriendenlijst4=['David', 'Davito',  248392,  'Stardew Valley', 105, 'Rust', 32.5, 'F1 2018', 104]
lijst=['Pascal','Sven','Kyrill','David']

def insertmentvoortree(vriendenlijst):
    res=(vriendenlijst[0],vriendenlijst[1],vriendenlijst[2],vriendenlijst[3],str(vriendenlijst[4])+' '+'uur',vriendenlijst[5],str(vriendenlijst[6])+' '+'uur',vriendenlijst[7],str(vriendenlijst[8])+' '+'uur')
    return res
#plaats tree
def tree2insert(vriendenlijst):
    tree2.pack(pady=10, padx=10)
    tree2.insert(parent='', index='end', text="game",
                 values=(insertmentvoortree(vriendenlijst)))
    
tree2insert(vriendenlijst)
tree2insert(vriendenlijst2)
tree2insert(vriendenlijst3)
tree2insert(vriendenlijst4)

##knoppen om te sorteren, --moeten naar heading veranderd worden-- zijn nu naar heading veranderd, dus onnodig. ik hou ze hier gewoon voor het geval dat.
#Button(f2, text='Sorteer op naam', command=sortByName).pack(pady=10)
#Button(f2, text='Sorteer games op uitkomstdatum', command=sortByReleaseDate).pack(pady=10)
#Button(f2, text='Sorteer games op geschikte leeftijd', command=sortByAge).pack(pady=10)
#Button(f2, text='Sorteer games op prijs', command=sortByPrice).pack(pady=10)
#Button(f2, text='Sorteer games op Waardering', command=sortByRating).pack(pady=10)
#Button(f2, text='Sorteer games op datum AppID', command=sortByAppid).pack(pady=10)


#knop voor steam launch en lijst omdraaien
Button(f2, text='Start game', command=launchGame).pack(pady=10, side=BOTTOM)
Button(f2, text = 'Lijst omkeren', command=reverseList).pack(pady=10)

#knoppen en labels voor welkom en teruggaan
Button(f2, text='Terug', command=lambda: raise_frame(f1)).pack(pady=10)
Label(f3, text='Welkom', font=('Helvetica', 12, 'bold italic'), height=2, width=20).pack()
Button(f3, text='Terug', command=lambda: raise_frame(f1)).pack(pady=10)

Button(f4, text='Terug', command=lambda: raise_frame(f1)).pack(pady=10)

filterEntry = Entry(f2)
filterEntry.pack(padx = 20, pady = 30)

#filterPicker = OptionMenu(f2, 'naam', 'waardering', 'prijs', 'minimumleeftijd', 'appID', 'uitkomstdatum')
#filterPicker.pack(padx = 20, pady = 30)

def refreshGames():
    tree.delete(*tree.get_children()) #leeg de tree
    for i in listOfGames: #plaats de list opnieuw
        tree.insert(parent='', index='end', iid=i.appid, text="game", values=(i.name, round(i.rating, 2), i.price, i.required_age, i.release_date, i.appid))

refreshGames()

sortByAppid()
#print(listOfGames[0].name)

#def refreshLabelLoop():
    #root.after(50, refreshLabelLoop)

"""""
-----------------------------------------------------------
                                TI COMPONENT CODES
-----------------------------------------------------------
"""""

#def AfstandSensor(): #Checkt of gebruiker achter pc zit en past de status aan.


# run window
raise_frame(f1)
root.mainloop()
