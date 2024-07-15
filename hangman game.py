import math
import random
word = ["Snake", "water","gun"]
print("words are :" ,word )
rnd = math.floor(random.random()*3)
new_word = word[rnd]
a = 5
while(a>=0):
    inp = input('Guess the word')
    print("your word is: ",inp)
    if(inp==new_word):
        print("Suceed ou Win")
        break
    if(a>0):
        print("Now you have",a ,"Trial Left")
    else:
        print("My Word is: ",new_word)
        print("***---You lose---***")
    a = a-1
