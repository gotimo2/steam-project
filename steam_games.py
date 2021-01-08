
import json
#steam.json importen als dictionary
jsonFile = open('steam.json')
steamDictionary = json.load(jsonFile)
jsonFile.close()
global listOfGames

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

def quicksort(inputList, attribute):
    #attribute = getattr(game, attr)
    if len(inputList) < 2:
        return inputList
    low, middle, high = [], [], []
    pivot = getattr(inputList[len(inputList)//2], attribute)
    for i in inputList:
        n = getattr(i, attribute)
        if pivot > n:
            low.append(i)
        elif pivot == n:
            middle.append(i)
        elif pivot < n:
            high.append(i)
    return quicksort(low, attribute) + middle + quicksort(high, attribute)



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

def findById(id, index = 0):
    try:
        if listOfGames[index].id == id:
            return listOfGames[index]
    except IndexError:
        return
    else:
        return findById(id, index + 1)


def findByName(name, index = 0):
    try:
        if listOfGames[index].name.lower() == name.lower():
            return listOfGames[index]
    except IndexError:
        return
    else:
        return findByName(name, index + 1)
