import pygame, random as rnd
from pygame.locals import *

WIDTH = 800
HEIGHT = 800

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

    def __repr__(self):
        return "<Card (%s of %s)>" % (self.face, self.suit)

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
        self.image = pygame.Surface((73,123))
        self.rect = self.image.get_rect()
        self.rect.left = WIDTH/2+2
        self.rect.centery = HEIGHT/2

    def placeCard(self, card):
        self.discard.insert(0, card)
        self.image = card.image

    def returnCard(self):
        card = self.discard.pop(0)
        self.image = self.discard[0].image
        return card

class Deck(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.cards = [Card(Cards.suits[i],Cards.faces[j]) for i in range(4) for j in range(13)]
        self.image = pygame.image.load("cardback.jpg")
        self.rect = self.image.get_rect()
        self.rect.right = WIDTH/2-2
        self.rect.centery = HEIGHT/2

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
            for player in rule.check():
                texter.setText("Player %i: %s" % (playerTurn+1, rule.err_msg))
                player.cards.append(deck.drawCard())

class Rule(object):

    err_msg = "Failure to follow rules."
    
    def __init__(self):
        Rules.rules.append(self)
        
    def check(self):
        return []

class validityCheck(Rule):

    err_msg = "Neither suit or face value match."
    
    def check(self):
        if len(discard.discard) < 2:
            return []
        if discard.discard[0].suit != discard.discard[1].suit:
            if discard.discard[0].face != discard.discard[1].face:
                curPlayer.cards.append(discard.returnCard())
                return [players[playerTurn]]
        return []

class cardCountCheck(Rule):
    
    err_msg = "You have too many cards. You lose."

    def check(self):
        if len(curPlayer.cards) == 11:
            return [players.pop(playerTurn)]
        elif len(curPlayer.cards) == 0:
            running = False
            texter.setText("Player %i is the winner!" % playerTurn)
        return []

class msgDisplay(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.timeLeft = 0
        self.image = pygame.Surface((0,0))
        self.rect = self.image.get_rect()
        self.font = pygame.font.SysFont('Comic Sans', 30)

    def setText(self, text, time=3):
        self.image = self.font.render(text,True,(0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        self.timeLeft = time

    def update(self):
        if self.timeLeft > 0:
            self.timeLeft -= 1/30.0
        else:
            self.image = pygame.Surface((0,0))

pygame.init()
pygame.font.init()

deck = Deck()
discard = Stack()
timer = Timer()
texter = msgDisplay()

discard.placeCard(deck.drawCard())

players = [Player([deck.drawCard() for i in range(6)]) for i in range(min(4,input("How many players are there? ")))]

suitChecker = validityCheck()
cardCountChecker = cardCountCheck()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
background = pygame.Surface((WIDTH,HEIGHT))

bgcolor = (rnd.randrange(0,255),rnd.randrange(0,255),rnd.randrange(0,255))
nplayers = len(players)
playerTurn = 0
curPlayer = players[playerTurn]

clock   = pygame.time.Clock()
sprites = pygame.sprite.Group(deck, discard, timer, texter)

nextTurn = True
running = True
knockCount = 0

while running:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            for i in range(len(curPlayer.cards)):
                if curPlayer.cards[i].rect.collidepoint(pygame.mouse.get_pos()):
                    discard.placeCard(curPlayer.cards.pop(i))
                    nextTurn = False
                    knockCount = 0
                    break
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            else:
                nextTurn = True
                knockCount += 1
                playerTurn = (playerTurn + 1) % nplayers
                curPlayer = players[playerTurn]
                if knockCount == len(players):
                    knockCount = 0
                    discard.placeCard(deck.drawCard())

    if not nextTurn:
        Rules().check()
        nextTurn = True
        playerTurn = (playerTurn + 1) % nplayers
        curPlayer = players[playerTurn]

    sprites.update()
    background.fill(bgcolor)
    sprites.draw(background)
    
    rect = pygame.rect.Rect(0,140,79,123)
    
    for i in range(len(curPlayer.cards)):
        curPlayer.cards[i].rect = rect.copy()
        background.blit(curPlayer.cards[i].image,rect)
        rect.left += 80
        
    screen.blit(background, (0,0))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
