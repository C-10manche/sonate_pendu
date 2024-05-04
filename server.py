from flask import Flask, render_template, request
from random import randint

playername = ""
lifepoint = 5
word_to_guess = ""
indice = ""
player_guess = ""
result = ""
list_of_words = []

def open_dictionary(): 
    #On récupère chaque phrases du file dictionnaire.txt puis on récupère chaque premier mots
    with open("dictionnaire.txt", "r", encoding="utf-8") as file:
        dictionary = file.read()
        dictionary = dictionary.split()
        
    for phrase in dictionary:
        words = phrase.split(";")
        first_word = words[0]
        list_of_words.append(first_word)
    
    return list_of_words

def remove_accent(word:str):
    #Cette fonction c'est pour ne pas utiliser unidecode qui est une library externe
    #Je vais demander au prof si on peut utiliser unidecode, si il dit oui je supprimerais cette fonction
    
    #J'ai seulement mis les caractères spéciaux qui étaient présent dans le dictionnaire.txt
    a = ['à', 'â']
    e = ['è', 'é', 'ê', 'ë']
    i = ['î', 'ï']
    o = ['ô', 'ö']
    u = ['ù', 'û', 'ü']
    c = ['ç']
    
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

def play_hangman():
    global playername, lifepoint, word_to_guess, indice, player_guess, result
    player_guess = request.form["playerguess"]
    new_indice = []
    
    if player_guess in remove_accent(indice):
        result = "Déjà Trouvé !"
    elif player_guess in word_to_guess: 
        result = "OUI !"         
        for x in range(len(word_to_guess)):
            if player_guess == remove_accent(word_to_guess[x]):
                new_indice.append(word_to_guess[x])
            else :
                new_indice.append(indice[x])                    
        indice = "".join(new_indice)           
    else :
        result = "NON !"
        lifepoint -= 1
    
    if lifepoint <= 0 or "_" not in indice :        
        return render_template("result.html", lifepoint = lifepoint, word_to_guess = word_to_guess)
    else :
        return render_template("play.html", result = result, lifepoint = lifepoint, indice = ' '.join(indice), word_to_guess = ' '.join(word_to_guess))

def reset_game():
    #Réinitialise les variables du jeu à leur valeur initial
    global lifepoint, word_to_guess, indice, result   
    lifepoint = 5
    word_to_guess = get_random_word()
    indice = "_" * len(word_to_guess)
    result = "Cliquez sur les lettres et trouvez le mot caché"
    return render_template("play.html", playername = playername, result = result, lifepoint = lifepoint, indice = ' '.join(indice), word_to_guess = ' '.join(word_to_guess))

app = Flask(__name__)
@app.route("/")
def home(): 
    return render_template("home.html")

@app.route("/play", methods=["POST"])
def play():
    global playername, list_of_words, lifepoint, word_to_guess, indice, player_guess, result 
      
    if request.method == "POST":
        if "playername" in request.form:
            list_of_words = open_dictionary()  
            playername = request.form["playername"] 
            return reset_game()       
        elif "playerguess" in request.form:
            return play_hangman()
        elif "replay" in request.form:
            return reset_game()
    

#flask --app server run
#flask --app server --debug run

#if __name__ == "__main__":
#    app.run(debug=True, host='127.0.0.1', port=5000)
#    list_of_words = open_dictionary()
