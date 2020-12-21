from tkinter import * #pylint:disable=unused-wildcard-import
import steam_games
from steam_games import * #pylint:disable=unused-wildcard-import
import time

#maak window en maak een lokale """kopie""" van listofgames voor makkelijk gebruik en manipulatie
window = Tk()
listOfGames = steam_games.listOfGames

#log de games in de huidige volgorde naar log.txt
def logGames():
    with open("log.txt", "w") as file:
        for i in listOfGames:
            file.write(f'{i.name}: {i.price}, {i.release_date} - {round(i.rating, 1)}% positive reviews, ({round(i.required_age, 0)}+) - product {i.appid}\n')

sortByAppid()

print(listOfGames[0].name)

def refreshLabelLoop():
    mainLabel["text"] = f"{listOfGames[0].name} \n €{listOfGames[0].price} \n {round(listOfGames[0].rating, 1)}% positief"
    window.after(50, refreshLabelLoop)
    

#maak window

window.after(50, refreshLabelLoop)
window.config(
    bg="#91a6eb"
)
window.title("Smoke")
window.geometry("800x600")

mainLabel = Label(
    master=window,
    text="",
    font="Aurelio, 22",
    bg="#91a6eb"
)
mainLabel.place(
    x=370,
    y=200,
    anchor="center"
)
logToFileButton = Button(
    master=window,
    text="Download gesorteerde catalogus",
    width=30,
    height=2,
    command=logGames
)

logToFileButton.place(
    x=260,
    y=100
)

sortByNameButton = Button(
    master=window,
    text="Sorteer games op naam",
    height=5,
    width=30,
    command = sortByName
)

sortByNameButton.place(
    x=150,
    y=300
)

sortByReleaseButton = Button(
    master=window,
    text="Sorteer games op uitkomstdatum",
    height=5,
    width=30,
    command = sortByReleaseDate
)

sortByReleaseButton.place(
    x=150,
    y=400
)


sortByAgeButton = Button(
    master=window,
    text="Sorteer games op geschikte leeftijd",
    height=5,
    width=30,
    command=sortByAge
)

sortByAgeButton.place(
    x=150,
    y=500
)

sortByPriceButton = Button(
    master=window,
    text="Sorteer games op prijs",
    height=5,
    width=30,
    command=sortByPrice
)

sortByPriceButton.place(
    x=380,
    y=300
)

sortByRatingButton = Button(
    master=window,
    text="Sorteer games op Waardering",
    height=5,
    width=30,
    command=sortByRating
)

sortByRatingButton.place(
    x=380,
    y=400
)
sortByAppidButton = Button(
    master=window,
    text="Sorteer games op datum toegevoegd",
    height=5,
    width=30,
    command=sortByAppid
)

sortByAppidButton.place(
    x=380,
    y=500
)


#run window
window.mainloop()