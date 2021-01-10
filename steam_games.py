
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

def makeList(attribuut):
    #Maakt lijst van gewenst attribuut
    if attribuut == 1: #1 is class price
        lijst = []
        for i in range(len(listOfGames)):
            lijst.append(listOfGames[i].price)
    elif attribuut == 2:
        lijst = []
        for i in range(len(listOfGames)):
            lijst.append(listOfGames[i].rating)
    return lijst


def mean(lst):
    #Geeft gemiddelde van de gegeven lijst
    gemiddelde = sum(lst) / len(lst)
    return round(gemiddelde, 2)

def median(lst):
    #Geeft mediaan van de gegeven lijst
    lst = sorted(lst)
    if len(lst) % 2 == 0:
        index_1 = (len(lst) // 2) - 1
        index_2 = int(-(-len(lst) // 2))
        med = (lst[index_1] + lst[index_2]) / 2
        return round(med, 2)
    else:
        med = lst[len(lst) // 2]
        return round(med, 2)

def q1(lst):
    #Geeft q1 van gegeven van de lijst
    lijst = []
    lst = sorted(lst)
    index_1 = (len(lst) // 2) - 1
    index_2 = int(-(-len(lst) // 2))
    if lst[index_1] == median(lst) and lst[index_2] == median(lst) and len(lst) % 2 == 0:
        lijst.append(lst[index_1])
    for i in lst:
        if i < median(lst):
            lijst.append(i)
    kwartiel_1 = median(lijst)

    return kwartiel_1


def q3(lst):
    #Geeft q3 van gegeven lijst
    lijst = []
    lst = sorted(lst)
    index_1 = (len(lst) // 2) - 1
    index_2 = int(-(-len(lst) // 2))
    if lst[index_1] == median(lst) and lst[index_2] == median(lst) and len(lst) % 2 == 0:
        lijst.append(lst[index_2])
    for i in lst:
        if i > median(lst):
            lijst.append(i)
    kwartiel_3 = median(lijst)

    return kwartiel_3


def var(lst):
    #Geeft variantie van de gegeven lijst
    lijst = []
    for i in lst:
        afwijking = i - mean(lst)
        lijst.append(afwijking)
    kwadraat_lijst = []
    for x in lijst:
        kwadraat = x**2
        kwadraat_lijst.append(kwadraat)
    variantie = mean(kwadraat_lijst)
    return variantie


def std(lst):
    #Geeft standaarddeviatie van de gegeven lijst
    return round(var(lst)**(1/2), 2)


def freq(lst):
    #Geeft dictionary met de elementen als keys en de frequentie als value
    freqs = {}
    for i in lst:
        if i in freqs:
            freqs[i] = freqs[i] + 1
        else:
            freqs[i] = 1
    return freqs


def modes(lst):
    #Geeft gesorteerde lijst van modussen van gegeven lijst
    values = []
    for key, value in freq(lst).items():
        values.append(value)
    maxi = values[0]
    for x in values:
        if x > maxi:
            maxi = x
    modi = []
    for key, value in freq(lst).items():
        if value == maxi:
            modi.append(key)
    return sorted(modi)