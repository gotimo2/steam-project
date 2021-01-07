from tkinter import *  # pylint:disable=unused-wildcard-import
from tkinter import ttk
import steam_games
from steam_games import *  # pylint:disable=unused-wildcard-import
import time

# maak window en maak een lokale """kopie""" van listofgames voor makkelijk gebruik en manipulatie
root = Tk()
root.title("Steam Tool")
listOfGames = steam_games.listOfGames


def raise_frame(frame):
    frame.tkraise()




f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)



for frame in (f1,f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')


C = Canvas(master=root, bg="blue", height=250, width=300)
filename = PhotoImage(file="steam image3.png")
background_label = Label(master=f1, image=filename)
background_label2 = Label(master=f2, image=filename)

background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label2.place(x=0, y=0, relwidth=1, relheight=1)

background_label3 = Label(master=f3, image=filename)
background_label3.place(x=0, y=0, relwidth=1, relheight=1)

background_label4 = Label(master=f4, image=filename)
background_label4.place(x=0, y=0, relwidth=1, relheight=1)
C.pack



Label(f1, text='Steam Tool', font=('Helvetica', 12, 'bold italic'), height=2, width=20).pack()

overzichtgames = Button(f1, text='Overzicht games', command=lambda: raise_frame(f2)).pack(pady=10)
statistieken = Button(f1, text='Statistieken', command=lambda: raise_frame(f3)).pack(pady=10)
vriendenlijst = Button(f1, text='Vriendenlijst', command=lambda: raise_frame(f4)).pack(pady=10)


tree = ttk.Treeview(f2, column=("column1", "column2", "column3","column4", "column5", "column6"), show='headings')
tree.heading("#1", text="Naam")
tree.heading("#2", text="Waardering")
tree.heading("#3", text="Prijs")
tree.heading("#4", text="Leeftijd")
tree.heading("#5", text="Uitkomstdatum")
tree.heading("#6", text="AppID")

tree.pack(pady=10, padx=10)


Button(f2, text='Sorteer op naam', command=sortByName).pack(pady=10)
Button(f2, text='Sorteer games op uitkomstdatum', command=sortByReleaseDate).pack(pady=10)
Button(f2, text='Sorteer games op geschikte leeftijd', command=sortByAge).pack(pady=10)
Button(f2, text='Sorteer games op prijs', command=sortByPrice).pack(pady=10)
Button(f2, text='Sorteer games op Waardering', command=sortByRating).pack(pady=10)
Button(f2, text='Sorteer games op datum AppID', command=sortByAppid).pack(pady=10)





Button(f2, text='Terug', command=lambda: raise_frame(f1)).pack(pady=10)




Label(f3, text='Welkom', font=('Helvetica', 12, 'bold italic'), height=2, width=20).pack()
Button(f3, text='Terug', command=lambda: raise_frame(f1)).pack(pady=10)

Label(f4, text='Welkom', font=('Helvetica', 12, 'bold italic'), height=2, width=20).pack()
Button(f4, text='Terug', command=lambda: raise_frame(f1)).pack(pady=10)


def refreshGames():
    for i in listOfGames:
        tree.insert(parent='', index='end', iid=i.appid, text="game", values=(i.name, i.rating, i.price, i.required_age, i.release_date, i.appid))


refreshGames()
# log de games in de huidige volgorde naar log.txt zod
def logGames():
    with open("log.txt", "w") as file:
        for i in listOfGames:
            file.write(
                f'{i.name}: {i.price}, {i.release_date} - {round(i.rating, 1)}% positive reviews, ({round(i.required_age, 0)}+) - product {i.appid}\n')


sortByAppid()

print(listOfGames[0].name)


def refreshLabelLoop():
    root.after(50, refreshLabelLoop)




# run window
raise_frame(f1)

root.mainloop()