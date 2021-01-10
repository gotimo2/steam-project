
import json
#steam.json importen als dictionary
jsonFile = open('steam.json') 
steamDictionary = json.load(jsonFile)
jsonFile.close()

#defineer game object
class game:
    def __init__(self, appid, name, price, release_date, developer, publisher, platforms, required_age, categories, genres, achievements, negative_ratings, positive_ratings, rating):
        self.name = name
        self.price = price
        self.release_date = release_date
        self.developer = developer
        self.rating = rating
        self.positive_ratings = positive_ratings
        self.negative_ratings = negative_ratings
        self.publisher = publisher
        self.appid = appid
        self.platforms = platforms
        self.required_age = required_age
        self.categories = categories
        self.genres = genres
        self.achievements = achievements

#maak lijst met iedere game
listOfGames = []   
for i in steamDictionary:
    listOfGames.append(
    game(
        name = i["name"],
        price = i["price"],
        release_date = i["release_date"],
        developer = i["developer"],
        positive_ratings = i["positive_ratings"],
        negative_ratings = i["negative_ratings"],
        rating = (i["positive_ratings"] / (i["positive_ratings"] + i["negative_ratings"])) * 100,
        publisher = i["publisher"],
        appid = i["appid"],
        platforms = i["platforms"],
        required_age = i["required_age"],
        categories = i["categories"],
        genres = i["genres"],
        achievements = i["achievements"]
    ))
    

#sorteeruncties, iedere functie gebruikt quicksort + een attribuut

#dit is de quicksort functie, dit sorteert.
def quicksort(inputList, attribute): #neem inputlist + een attribuut om de lijst op te sorteren
    if len(inputList) < 2: #als de lijst maar 1 groot is valt er weinig te sorteren en is dat stuk klaar
        return inputList
    low, middle, high = [], [], [] #maak lege lijsten aan
    pivot = getattr(inputList[len(inputList)//2], attribute) #verdeel de lijst in twee en pak het middelste getal als de pivot waarmee andere nummers vergeleken worden
    for i in inputList: #voor iedere game in de lijst
        n = getattr(i, attribute) #pak de waarde van het gekozen attribuut
        if pivot > n: #voeg hem aan de juiste lijst toe
            low.append(i)
        elif pivot == n:
            middle.append(i)
        elif pivot < n:
            high.append(i)
    return quicksort(low, attribute) + middle + quicksort(high, attribute) #blijf dit dan recursief herhalen totdat de lijst gesorteerd is

def sortByName():
    sortedlist = quicksort(listOfGames, 'name')
    listOfGames.clear()
    for i in sortedlist:
        listOfGames.append(i)

def sortByAppid():
    sortedlist = quicksort(listOfGames, 'appid')
    listOfGames.clear()
    for i in sortedlist:
        listOfGames.append(i)

def sortByRating():
    sortedlist = quicksort(listOfGames, 'rating')
    listOfGames.clear()
    for i in sortedlist:
        listOfGames.append(i)

def sortByPrice():
    sortedlist = quicksort(listOfGames, 'price')
    listOfGames.clear()
    for i in sortedlist:
        listOfGames.append(i)
       

def sortByAge():
    sortedlist = quicksort(listOfGames, 'required_age')
    listOfGames.clear()
    for i in sortedlist:
        listOfGames.append(i)

def sortByReleaseDate():
    sortedlist = quicksort(listOfGames, 'release_date')
    listOfGames.clear()
    for i in sortedlist:
        listOfGames.append(i)

#zoekfuncties        
        
def findById(id, index = 0): #neem appid, start bij index 0 als er geen andere index wordt opgegeven
    try:    #kijk of de huidige game het juiste ID heeft
        if listOfGames[index].id == id: #en als hij dat heeft
            return listOfGames[index] #geef de game-object terug die die ID heeft
    except IndexError: #als er een indexerror gebeurt, wat er gebeurt als je verder zoekt dan de lijst is
        return  #geef dan niks terug, want dan zit dat item niet in de lijst
    else: #als er geen indexerror is gebeurd maar het huidige item is niet de goede
        return findById(id, index + 1) #doe dan dezelde funtie met een hogere index, dus bekijk het volgende item


def findByName(name, index = 0): #zelfde
    try: #principe
        if listOfGames[index].name.lower() == name.lower(): #als
            return listOfGames[index] #de 
    except IndexError: #functie
        return #hierboven
    else:
        return findByName(name, index + 1)
