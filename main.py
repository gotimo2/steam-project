from tkinter import * #pylint:disable = unused-wildcard-import
import json

jsonFile = open('steam.json')
steamDictionary = json.load(jsonFile)
jsonFile.close()
window = Tk()

window.mainloop()