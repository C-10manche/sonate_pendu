from flask import Flask, render_template, request
from unidecode import unidecode
from random import random


playername = ""
lifepoint = 5
word_to_guess = ""
indice = ""
player_guess = ""
result = ""
list_of_words = []

def open_dictionary():
    global list_of_words
    with open("dictionnaire.txt", "r", encoding="utf-8") as file:
        dictionary = file.read().split()        
    for phrase in dictionary:
        words = phrase.split(";")
        first_word = words[0]
        list_of_words.append(first_word)

def get_random_word():
    size = len(list_of_words)
    random_place = int(random()*size) + 1
    random_word = list_of_words[random_place]    
    return random_word

def reset_game():
    global lifepoint, word_to_guess, indice, result   
    lifepoint = 5
    word_to_guess = get_random_word()
    indice = "_" * len(word_to_guess)
    result = ""

app = Flask(__name__)
@app.route("/", methods=["GET","POST"])
def home():
    global playername
    if request.method == "POST":
        playername = request.form["playername"]
        reset_game()
        return render_template("play.html", playername = playername, result = result, lifepoint = lifepoint, indice = ' '.join(indice), word_to_guess = ' '.join(word_to_guess)) 
    
    return render_template("home.html")

@app.route("/play", methods=["GET","POST"])
def play():
    global playername, lifepoint, word_to_guess, indice, player_guess, result   
      
    if request.method == "POST":
        player_guess = request.form["playerguess"]
        new_indice = []
        if player_guess in unidecode(indice):
            result = "Déjà Trouvé !"
        elif player_guess in word_to_guess: 
            result = "OUI !"         
            for x in range(len(word_to_guess)):
                if player_guess == unidecode(word_to_guess[x]):
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
    elif request.method == "GET":
        reset_game()
        return render_template("play.html", result = result, lifepoint = lifepoint, indice = ' '.join(indice), word_to_guess = ' '.join(word_to_guess))        
    


if __name__ == "__main__":
    open_dictionary()
    app.run(debug=True, host='127.0.0.1', port=5000)