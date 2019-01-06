from IPython.display import clear_output
import random

suits = ('Hearts',' Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
playing = True
amount = 100

class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        pass
    
    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
                pass
    
    def __str__(self):
        deck_list = ''
        for card in self.deck:
            deck_list += str(card) + ", "
        return deck_list
    
    def __len__(self):
        return len(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return (self.deck.pop(0))
        pass

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces        
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == "Ace":
            self.aces += 1
        pass
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
    
    def __str__(self):
        player_hand = ''
        for card in self.cards:
            player_hand += str(card) + ", "
        return player_hand

class Chips:
    
    def __init__(self,total):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
        pass
    
    def lose_bet(self):
        self.total -= self.bet
        pass        

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("please enter your bet "))
        except:
            print("Please enter only whole numbers")
        else:
            if chips.bet > chips.total:
                print("you don't have enough chips. please enter a smaller amount")
            else:
                break
    pass

def hit(deck,hand):
        hand.add_card(deck.deal())
        hand.adjust_for_ace()

    #Need to add Aces check

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    result = input("Hit or Stand: ").lower()
    if result == "hit":
        hit(deck,hand)
    else:
        playing = False

def show_some(player,dealer):
    print("player hand is: " + str(player))
    #dealer_string = str(dealer)
    #dealer_split = dealer_string.split(',')
    #print("dealer hand is: " + str(dealer_split[1:]))
    print("dealer hand is: " + str(dealer.cards[1]))
    pass
    
def show_all(player,dealer):
    print(f"player hand is: {player}. Hand value is {player.value}")
    print(f"dealer hand is: {dealer}. Hand value is {dealer.value}")
    
    pass

###Player lost####
def player_busts(player,chips):
    if player.value > 21:
        chips.lose_bet()
        print("Busted! you've lost. Dealer wins.")
        return True
    pass

####Player Won###
def player_wins(player,dealer,chips):
    if (dealer.value < player.value):
        chips.win_bet()
        print("Yeah baby! Player won!")
        return True
    pass

####Player Won###
def dealer_busts(dealer,chips):
    if dealer.value > 21:
        chips.win_bet()
        print("Yeah baby! Player won! Dealer Busted!")
        return True
    pass

###Player lost####    
def dealer_wins(player,dealer,chips):
    if dealer.value > player.value:
        chips.lose_bet()
        print("You've lost! Dealer Won!")
        return True
    pass
    
def push(player,dealer):
    if dealer.value == player.value:
        print("Push me to somewhere please")
        return True
    pass

while True:
    # Print an opening statement
    clear_output()
    print("Welcome to my first Python Blackjack game!")


    # Create & shuffle the deck, deal two cards to each player
    game = True
    mydeck = Deck()
    mydeck.shuffle()
    liran = Hand()
    mydealer = Hand()
    liran.add_card(mydeck.deal())
    liran.add_card(mydeck.deal())
    mydealer.add_card(mydeck.deal())
    mydealer.add_card(mydeck.deal())
     
    # Set up the Player's chips
    liran_chips = Chips(amount)
    
    # Prompt the Player for their bet
    take_bet(liran_chips)
    
    # Show cards (but keep one dealer card hidden)\
    show_some(liran,mydealer)    

    
    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(mydeck,liran)
        
        # Show cards (but keep one dealer card hidden)
        show_some(liran,mydealer)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if (player_busts(liran,liran_chips)):
            game = False
            break
        
    #break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    while (mydealer.value < 17):
        hit(mydeck,mydealer)
    
    
        # Show all cards
    show_all(liran,mydealer)
    
        # Run different winning scenarios
    while game:
        if player_wins(liran,mydealer,liran_chips):
            game = False
        elif dealer_busts(mydealer,liran_chips):
            game = False
        elif dealer_wins(liran,mydealer,liran_chips):
            game = False
        elif push(liran,mydealer):
            game = False
        
    
    # Inform Player of their chips total 
    print(f"Your chips total is: {liran_chips.total}")
    
    # Ask to play again

    again = input("do you want to play again? ").lower()
    if again == 'yes':
        amount = liran_chips.total
        playing = True
    else:
        break        