
import json
import datetime
#steam.json importen als dictionary
jsonFile = open('steam.json') 
steamDictionary = json.load(jsonFile)
jsonFile.close()

currentDate = datetime.datetime.now().strftime("%Y-%m-%d")

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
def regenGameList():
    for i in listOfGames:
        del i
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

regenGameList()

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

#quicksort2, voor als je quicksort op waarden ipv attributen
def quicksort2(inputList): 
    if len(inputList) < 2: 
        return inputList
    low, middle, high = [], [], [] 
    pivot = inputList[len(inputList)//2] 
    for i in inputList: 
        n = i 
        if pivot > n: 
            low.append(i)
        elif pivot == n:
            middle.append(i)
        elif pivot < n:
            high.append(i)
    return quicksort2(low) + middle + quicksort2(high)

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

# legacy logGames() functie
def logGames():
    with open("log.txt", "w") as file:
        for i in listOfGames:
            file.write(
                f'{i.name}: {i.price}, {i.release_date} - {round(i.rating, 1)}% positive reviews, ({round(i.required_age, 0)}+) - product {i.appid}\n')

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

def makeList(attribuut, base=listOfGames):
    newlist = []
    for i in base:
        newlist.append(getattr(i, attribuut))
    return newlist

def mean(lst):
    #Geeft gemiddelde van de gegeven lijst
    gemiddelde = sum(lst) / len(lst)
    return round(gemiddelde, 2)

def median(lst):
    #Geeft mediaan van de gegeven lijst
    lst = quicksort2(lst)
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
    avg = sum(lst) / len(lst)
    totaldiff = 0
    for i in lst:
        totaldiff += (i - avg) ** 2
    return totaldiff / len(lst)

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
    quicksort2(lst)
    modussen = list()
    frequence = freq(lst)
    for i in frequence:
        if frequence.get(i) == max(frequence.values()):
            modussen.append(i)
    return modussen

#filterfuncties

def filterByName(que):
    regenGameList()
    for i in listOfGames:
        if que not in i.name:
            del i

def filterByAppID(que):
    regenGameList()
    for i in listOfGames:
        if i.appid != que:
            del i

def filterByPrice(que_high, que_low = 0):
    regenGameList()
    for i in listOfGames:
        if que_high < i.price or que_low > i.price:
            del i

def filterByRating(que_high, que_low, que_number = 100):
    regenGameList()
    for i in listOfGames:
        if que_high < i.rating or que_low > i.rating or (i.positive_ratings + i.negative_ratings) < que_number:
            del i

def filterByAge(que_high, que_low = 0):
    regenGameList()
    for i in listOfGames:
        if que_high < i.required_age or que_low > i.required_age:
            del i

def filterByRelease(que_low, que_high = currentDate):
    regenGameList()
    for i in listOfGames:
        if que_high < i.release_date or que_low > i.release_date:
            del i
    pass
    
