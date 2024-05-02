from unidecode import unidecode
from random import random

def get_random_word():
    list_of_words = []
    with open("dictionnaire.txt", "r", encoding="utf-8") as file:
        dictionary = file.read().split()
        
    for phrase in dictionary:
        words = phrase.split(";")
        first_word = words[0]
        list_of_words.append(first_word)

    size = len(list_of_words)
    random_place = int(random()*size) + 1
    random_word = list_of_words[random_place]
    
    return random_word

def play_game():
    hp = 5
    word = get_random_word()
    indice = "_" * len(word)
    print("\nIndice :", indice)
    
    while hp > 0 and "_" in indice:
        player_guess = input("\nSaisis une lettre : ").lower()
        new_indice = []        
        
        if player_guess in unidecode(indice):
            print("\nTu l'as déjà trouvé") 
        elif player_guess in word:
            print("\nOUI!")            
            for x in range(len(word)):
                if player_guess == unidecode(word[x]):
                    new_indice.append(word[x])
                else :
                    new_indice.append(indice[x])                    
            indice = "".join(new_indice)            
        else :
            print("\nNON!")
            hp -= 1
            
        print("\n| Vie :", hp, "| Indice :", indice, " |")
              
    if hp > 0:
        print("\nGagner!\n")
    else:
        print("\nPerdu!\n")