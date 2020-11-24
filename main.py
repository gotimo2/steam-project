from tkinter import * #pylint:disable=unused-wildcard-import
import steam_games

listOfGames = steam_games.listOfGames
for i in listOfGames:
    print(i.name)

#maak window
window = Tk()


window.configure(
    
)
#run window
window.mainloop()