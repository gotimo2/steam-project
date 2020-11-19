from tkinter import * #pylint:disable=unused-wildcard-import
import json

#steam.json importen als dictionary
jsonFile = open('steam.json')
steamDictionary = json.load(jsonFile)
jsonFile.close()

#maak window
window = Tk()


window.configure(
    
)
#run window
window.mainloop()