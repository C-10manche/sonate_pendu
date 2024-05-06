from flask import Flask, render_template, request
from random import randint

playername = ""
lifepoint = 5
word_to_guess = ""
indice = ""
playerguess = ""
result = ""
list_of_words = []
wrong_guess =[]
good_guess =[]

def open_dictionary(): 
    #On récupère chaque phrases du file dictionnaire.txt puis on récupère chaque premier mots
    with open("dictionnaire.txt", "r", encoding="utf-8") as file:
        dictionary = file.readlines()
        
    for phrase in dictionary:
        words = phrase.split(";")
        first_word = words[0]
        list_of_words.append(first_word)
    
    return list_of_words

def remove_accent(word:str):    
    a = ["à", "â"]
    e = ["è", "é", "ê"]
    i = ["î", "ï"]
    o = ["ô"]
    u = ["ù", "û"]
    c = ["ç"]
    
    word = word.lower()
    new_word = ""
    
    for letter in word:
        if letter in a:
            new_word += "a"
        elif letter in e:
            new_word += "e"
        elif letter in i:
            new_word += "i"
        elif letter in o:
            new_word += "o"
        elif letter in u:
            new_word += "u"
        elif letter in c:
            new_word += "c"
        else:
            new_word += letter

    return new_word


def get_random_word():
    size = len(list_of_words)
    random_place = randint(0, size-1)
    random_word = list_of_words[random_place]    
    return random_word

def verify_game_status():
    #Check si le jeu doit continuer     
    if lifepoint <= 0 or "_" not in indice :      
        return render_template("result.html", lifepoint = lifepoint, word_to_guess = word_to_guess)
    else :                
        if app.debug:
            return render_template("play.html", result = result, lifepoint = lifepoint, indice = indice, word_to_guess = word_to_guess, good_guess = good_guess, wrong_guess = wrong_guess)
        else:
            return render_template("play.html", result = result, lifepoint = lifepoint, indice = indice, word_to_guess = " ", good_guess = good_guess, wrong_guess = wrong_guess)

def verify_guess():
    global playername, lifepoint, word_to_guess, playerguess, result
    playerguess = request.form["playerguess"]
    
    #Check si le joueur a bien deviné la lettre
    if playerguess in (good_guess or wrong_guess):
        #On a ajouté cette ligne pour éviter au joueur de perdre des points de vie si il refresh sa page
        result = "Vous avez déjà utilisé cette lettre !"           
    elif playerguess in remove_accent(word_to_guess):
        result = "OUI !"
        update_indice()
        good_guess.append(playerguess)
    else :
        result = "NON !"
        lifepoint -= 1
        wrong_guess.append(playerguess)
        

def update_indice():
    global indice    
    new_indice = []
    
    #Met à jour l'indice        
    for x in range(len(word_to_guess)):
        if playerguess == remove_accent(word_to_guess[x]):
            new_indice.append(word_to_guess[x])
        else :
            new_indice.append(indice[x])                    
    indice = "".join(new_indice)
    

def reset_game():
    global list_of_words, lifepoint, word_to_guess, indice, playerguess, result, wrong_guess
    
    #Réinitialise les variables du jeu à leur valeur initial
    lifepoint = 5
    word_to_guess = get_random_word()
    good_guess.clear()
    wrong_guess.clear()
    indice = "_" * len(word_to_guess)
    result = "Cliquer sur les lettres pour trouver le mot caché"

def register():    
    global playername, list_of_words
    list_of_words = open_dictionary()  
    playername = request.form["playername"] 
    reset_game()       

app = Flask(__name__)
@app.route("/")
def home(): 
    return render_template("home.html")

@app.route("/play", methods=["POST"])
def play():
    global playername, list_of_words
       
    #Gère les actions du joueur
    if request.method == "POST":
        if "playername" in request.form:
            register()    
        elif "playerguess" in request.form:
            verify_guess()
        elif "replay" in request.form:
            reset_game()
                       
    return verify_game_status()

#flask --app server run
#flask --app server --debug run
