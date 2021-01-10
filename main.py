import os
from tkinter import *  # pylint:disable=unused-wildcard-import
from tkinter import ttk
import steam_games
from steam_games import *  # pylint:disable=unused-wildcard-import
import time

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

Label(f4, text='Welkom', font=('Helvetica', 12, 'bold italic'), height=2, width=20).pack()
Button(f4, text='Terug', command=lambda: raise_frame(f1)).pack(pady=10)



def refreshGames():
    tree.delete(*tree.get_children()) #leeg de tree
    for i in listOfGames: #plaats de list opnieuw
        tree.insert(parent='', index='end', iid=i.appid, text="game", values=(i.name, round(i.rating, 2), i.price, i.required_age, i.release_date, i.appid))


refreshGames()
# log de games in de huidige volgorde naar log.txt zod
def logGames():
    with open("log.txt", "w") as file:
        for i in listOfGames:
            file.write(
                f'{i.name}: {i.price}, {i.release_date} - {round(i.rating, 1)}% positive reviews, ({round(i.required_age, 0)}+) - product {i.appid}\n')


sortByAppid()

#print(listOfGames[0].name)


#def refreshLabelLoop():
    #root.after(50, refreshLabelLoop)


# run window
raise_frame(f1)

root.mainloop()
