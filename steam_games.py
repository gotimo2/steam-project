
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

def sortByName():
    listOfGames.sort(key=lambda game: game.name)

def sortByAppid():
    listOfGames.sort(key=lambda game: game.appid,)

def sortByRating():
    listOfGames.sort(key=lambda game: game.rating, reverse=True)

def sortByPrice():
    listOfGames.sort(key=lambda game: game.price, reverse=True)

def sortByAge():
    listOfGames.sort(key=lambda game: game.required_age, reverse=True)

def sortByReleaseDate():
    listOfGames.sort(key=lambda game: game.release_date, reverse=True)
