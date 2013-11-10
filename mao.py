import pygame, random as rnd
from pygame.locals import *

WIDTH = 800
HEIGHT = 500

def genImages():
    s = pygame.image.load("cards.png")
    for i in range(len(Cards.suits)):
        for j in range(len(Cards.faces)):
            img = pygame.Surface((79,123))
            img.blit(s, (0,0), area=(j*79,i*123,79,123))
            pygame.image.save(img, Cards.faces[j]+Cards.suits[i]+".jpg")

class Cards:
    suits = ("clubs","diamonds","hearts","spades")
    faces = ("ace","2","3","4","5","6","7","8","9","10","jack","queen","king")

class Card(pygame.sprite.Sprite):
    def __init__(self, suit, face):
        pygame.sprite.Sprite.__init__(self)
        self.suit = suit
        self.face = face
        self.image = pygame.image.load(face+suit+".jpg")
        self.rect = self.image.get_rect()

class Timer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.timeLeft = 0
        self.font = pygame.font.SysFont("Comic Sans", 18)
        self.image = None
        self.rect  = None

    def update(self, *newTime):
        global WIDTH
        if newTime:
            self.timeLeft = newTime
        elif self.timeLeft > 0:
            self.timeLeft -= 1/30.0
        else:
            self.timeLeft = 0
        text = str(round(self.timeLeft, 2))
        text = text + "0"*(2-len(text.split(".")[1]))
        self.image = self.font.render(text,True,(0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH-self.rect.width

class Stack(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.discard = []
        self.image = pygame.Surface((10,10))
        self.rect = self.image.get_rect()

    def placeCard(self, card):
        self.discard.insert(0, card)

class Deck(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.cards = [Card(Cards.suits[i],Cards.faces[j]) for i in range(4) for j in range(13)]
        self.image = pygame.image.load("cardback.jpg")
        self.rect = self.image.get_rect()

    def drawCard(self):
        index = rnd.randrange(len(self.cards))
        card  = self.cards.pop(index)
        if not len(self.cards):
            self.cards = discard.discard
            discard.discard = []
        return card

class Player:
    def __init__(self, cards):
        self.cards = cards

class Rules:
    rules = []

    def check(self):
        for rule in self.rules:
            for player in rule().check():
                print "Player %i: %s" % (playerTurn, rule.err_msg)
                player.cards.append(deck.drawCard())

class Rule(object):

    err_msg = "Failure to follow rules."
    
    def __init__(self):
        Rules.rules.append(self)
        
    def check(self):
        return []

class suitCheck(Rule):

    err_msg = "Suits do not match."
    
    def check(self):
        if discard.discard[0].suit != discard.discard[1].suit:
            if faceChecker.check()[0] == players[playerTurn]:
                return [players[playerTurn]]

class faceCheck(Rule):

    def check(self):
        if discard.discard[0].face != discard.discard[1].face:
            return [players[playerTurn]]

class cardCountCheck(Rule):

    err_msg = "You have too many cards. You lose."

    def check(self):
        if len(players[playerTurn].cards) == 11:
            return [players.pop(playerTurn)]

pygame.init()
pygame.font.init()

deck = Deck()
discard = Stack()
timer = Timer()

players = [Player([deck.drawCard() for i in range(6)]) for i in range(input("How many players are there? "))]
           
screen = pygame.display.set_mode((WIDTH,HEIGHT))
background = pygame.Surface((WIDTH,HEIGHT))

bgcolor = (rnd.randrange(0,255),rnd.randrange(0,255),rnd.randrange(0,255))
nplayers = len(players)
playerTurn = 0

clock   = pygame.time.Clock()
sprites = pygame.sprite.Group(deck, discard, timer)

running = True

while running:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == K_DOWN:
            if event.key == K_ESCAPE:
                running = False
            
    sprites.update()
    background.fill(bgcolor)
    sprites.draw(background)
    
    curPlayer = players[playerTurn]
    rect = [0,HEIGHT-130,79,123]
    
    for i in range(len(curPlayer.cards)):
        background.blit(curPlayer.cards[i].image,rect)
        rect[0] += 80
        
    screen.blit(background, (0,0))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
