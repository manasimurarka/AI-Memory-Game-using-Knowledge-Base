import numpy as np
import random
import ctypes  # For making prompt
from knowledge_logic import *

class initial():

    def __init__(self, size1, size2, sym):
        self.row = size1
        self.col = size2
        self.sym = sym
        self.sym_grid = np.full((self.row,self.col),"Empty")
        self.grid = []   
                
    #Making symbol grid            
    def symbol_grid(self):  
        s = self.sym*2
        for i in range(self.row):
            for j in range(self.col):
                index = random.randint(0,len(s)-1)
                self.sym_grid[i][j] = s.pop(index)
        return self.sym_grid
    
    #making number grid
    def num_grid(self):     
        num = 0
        for i in range(self.row):
            self.grid.append([])
            for j in range(self.col):
                num += 1
                self.grid[i].append(num)
        return self.grid
    
    #print the grid - mainly for debugging purpose
    def print_grid(self,g):  
        for i in range(self.row):
            for j in range(self.col):
                print(g[i][j],end = "\t")
            print()



class move():

    def __init__(self,size1,size2,num_grid,sym_grid,knowledge):
    
        self.num_grid = num_grid
        self.sym_grid = sym_grid
        self.row = size1
        self.col = size2
        self.sym = set(sym_grid.flatten())
        self.not_matched_sym = list(self.sym)
        self.not_matched_cards = []
        for i in range(len(self.num_grid)):
            self.not_matched_cards.extend(self.num_grid[i])
        self.matched_cards = []
        self.known_cards = []
        self.knowledge = knowledge
        self.discovered_sym = {}
    
    #find index of card
    def card_index(self,card):
        for i in range(self.row):
            try:
                j = self.num_grid[i].index(card)
                return i,j
            except:
                continue
                
    #Check if cards picked by player have saqme symbol or not
    def card_match(self,card_1,card_2):
        c1_i , c1_j = self.card_index(card_1)
        c2_i , c2_j = self.card_index(card_2)
        if self.sym_grid[c1_i][c1_j] == self.sym_grid[c2_i][c2_j]:
            matched_symbol = self.sym_grid[c1_i][c1_j]
            
            #Replacing values of num grid by matched symbols
            self.num_grid[c1_i][c1_j] = self.num_grid[c2_i][c2_j] =  matched_symbol
            
            self.not_matched_sym.remove(matched_symbol)
            self.matched_cards.extend([card_1,card_2])
            
            self.not_matched_cards.remove(card_1)
            self.not_matched_cards.remove(card_2)
            
            self.known_cards.remove(card_1)
            self.known_cards.remove(card_2)
            
            #remove knowledge about extra cards with matched symbol
            for c in self.num_grid:
                if type(c) == int:   
                    a = Symbol(f'card_{c}_{matched_symbol}')
                    self.knowledge.remove(a)
                    
            self.discovered_sym.pop(matched_symbol)
            return "matched"
            
        else:
        
            return self.sym_grid[c1_i][c1_j],self.sym_grid[c2_i][c2_j]

    #return which player has to play
    def player_turn_switch(self, player):
        if player == "User":
            return "AI"
        else:
            return "User"
            
            
    #If game is over or not    
    def terminate(self):
        if self.not_matched_cards==[]:
            return True
        else:
            return False
        
    #If game terminated, print winner      
    def winner(self,winner):
        if winner>0:
            return "AI wins!"
        if winner<0:
            return "User wins!"
        else:
            return "It's a tie!"
            
    # determining the cards to be moved by AI       
    def AI_move(self):
    
        #if only 2 cards remaining -> return those two cards
        if len(self.not_matched_cards)==2:  
            return self.not_matched_cards[0],self.not_matched_cards[1]
        
        #if two cards with same symbol have been revealed then go through knowldedge base two find the two cards
        if 2 in self.discovered_sym.values() :
            for s,v in self.discovered_sym.items():
                if v == 2:
                    for c1 in self.known_cards[::-1]:
                        for c2 in self.known_cards:
                            if c1!=c2:
                                query = And(Symbol(f'card_{c1}_{s}'),Symbol(f'card_{c2}_{s}'))
                                if model_check(self.knowledge, query):
                                    return c1,c2
        
        #Choosing random cards 
        print("AI playing Random Move!\n")
        if len(self.known_cards)>=1:
            return random.choice(list(set(self.not_matched_cards)-set(self.known_cards))), random.choice(self.known_cards)
        else:
            card1 = random.choice(list(set(self.not_matched_cards)))
            card2 = random.choice(list(set(self.not_matched_cards.remove(card1))))
            self.not_matched_cards.append(card1)
            return card1,card2
    
    #add relevant knowledge about the cards picked by player
    def add_knowledge(self, c1, c2):
    
        for c in [c1,c2]:        
            if c not in self.known_cards:
            
                i,j = self.card_index(c)
                self.discovered_sym[self.sym_grid[i][j]] = self.discovered_sym.get(self.sym_grid[i][j],0) + 1
                self.known_cards.append(c)
                
                #removing non relevant knowledge about the card number picked
                for s in self.sym:
                    c_r = Symbol(f'card_{c}_{s}')
                    self.knowledge.remove(c_r)
                
                #adding the new new card and symbol pair to knowledge base
                self.knowledge.add(Symbol(f'card_{c}_{self.sym_grid[i][j]}'))    

#function to get prompt
def prompt(Text,Title):
         ctypes.windll.user32.MessageBoxW(0, Text, Title ,0)                   

 
sym=['#','$','@','%','!','&','^','~','>','?',':','+','-','*','\\','<','=','{}']

#getting input for grid size
size1 = int(input("Choose row length from list [2,3,4]: "))
if size1 == 3:
    size2 = int(input("Choose column height from list [2,4]: "))
else:
    size2 = int(input("Choose column height from list [2,3,4]: "))

#list of cards and symbols to be used
cards = [f'card_{i}' for i in range(1,size1*size2+1)]
sym = sym[0:int(size1*size2/2)]

#calling intial class and creating num_grid and sym_grid
obj = initial(size1, size2, sym)
sym_grid = obj.symbol_grid()
num_grid = obj.num_grid()
obj.print_grid(num_grid)
print()
print()
# obj.print_grid(sym_grid)       

#greating knowledge base and adding knowledge base condition of the game
knowledge = And()

#One symbol One card 
for c in cards:
    a=[Symbol(f"{c}_{s}") for s in sym]
    knowledge.add(InitialOr(a))
# In InitialOr we want only one card symbol combo hence the next function with implication
#Only One symbol per card
for c in cards:
    for s1 in sym:
        for s2 in sym:
            if s1 != s2:
                knowledge.add(Implication(Symbol(f"{c}_{s1}"), Not(Symbol(f"{c}_{s2}"))))    #card_1 symbol_1 => card_1 symbol_2 not possible          


# Two cards per Symbol
for s in sym:
    for c_1 in cards:
        for c_2 in cards:
            if c_1 != c_2: # check for 3 card if and only if index of card 1 and card 2 are not same
                for c_3 in cards:
                    if c_3!= c_2 and c_1 != c_3: # add to K.B if and only if indexes all the 3 cards is different
                        knowledge.add(Implication(And(Symbol(f'{c_1}_{s}'),Symbol(f'{c_2}_{s}')),Not(Symbol(f'{c_3}_{s}'))))    #sym of card_1 = sym of card_2 => card_3 with same sym not possible
                
 
          
#creating object for class move       
play = move(size1,size2,num_grid,sym_grid,knowledge)

#setting intial values of player and winner
winner = 0
player = "User"

while True:
    print("\n\nPlayer: ", player,"\n")
    
    #Take valid card numbers as input for carsd to be revealed
    if player == "User":
        print("\nChoose two cards to reveal: ")
        while True:
            try:
                c1 = int(input("Card 1: "))
                c2 = int(input("Card 2: "))
                if c1 in play.not_matched_cards and c2 in play.not_matched_cards:
                    break
                else:
                    print("Invalid input! Please choose from available cards")
                    obj.print_grid(num_grid)
            except:
                print("Invalid input! Please choose from available cards")
                obj.print_grid(num_grid)
    
    #Choose cards to be moved by AI
    else: 
        c1,c2 = play.AI_move()
        print("Card 1: ", c1)
        print("Card 2: ", c2)
        
    #add_knowledge about cards revealed and check if cards are a match  
    play.add_knowledge(c1,c2)
    match = play.card_match(c1,c2)
    
    if match == "matched":
        if player == "User":winner -=1
        else: winner += 1
        
        #if all cards matched then display winner and terminate game 
        if play.terminate():
            prompt(f'Cards Matched!\n\n{play.winner(winner)}',"Game Over")
            break
            
        prompt(f'{player} moves again!',"Cards matched!")
        print()
        print()
        obj.print_grid(play.num_grid)

    else:
        prompt(f'Cards revealed by {player}:\n\n\tCard {c1}: {match[0]}\n\tCard {c2}: {match[1]}',"Cards Not Matched!")
        player = play.player_turn_switch(player)
    
    
               