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
        self.font = pygame.font.SysFont("Comic Sans", 26)
        self.image = None
        self.rect  = None

    def update(self, *newTime):
        global WIDTH
        if newTime:
            self.timeLeft = newTime
        elif self.timeLeft > 0.0333:
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

class queenCheck(Rule):

    err_msg = "Failure to say 'god save the queen'."

    def check(self):
        if discard.discard[0].face == 'queen':
            if inputBox.textBuffer != 'god save the queen':
                return [curPlayer]
        return []

class aceCheck(Rule):

    err_msg = "Failure to say 'zing'."

    def check(self):
        if discard.discard[0].face == 'ace':
            if inputBox.textBuffer != 'zing':
                return [curPlayer]
        return []

class kingCheck(Rule):

    @property
    def err_msg(self):
        return "failure to say 'king of %s'" % self.suit

    def check(self):
        if discard.discard[0].face == 'king':
            if inputBox.textBuffer != 'king of ' + discard.discard[0].suit:
                self.suit = discard.discard[0].suit
                return [curPlayer]
        return []

class jackCheck(Rule):

    err_msg = "failure to declare a suit." 

    def check(self):
        if discard.discard[0].face == 'jack':
            if inputBox.textBuffer not in Cards.suits:
                return [curPlayer]
        return []

class sevenCheck(Rule):

    @property
    def err_msg(self):
        return "Failure to say 'have a %snice day'." % ("very " * self.count)

    def check(self):
        self.count = 0
        for i in discard.discard:
            if i.face == "seven":
                self.count += 1
        if discard.discard[0].face == 'seven':
            if inputBox.textBuffer != "have a %snice day" % ("very " * self.count):
                return [curPlayer]
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
        if self.timeLeft > .0333:
            self.timeLeft -= 1/30.0
        else:
            self.timeLeft = 0
            self.image = pygame.Surface((0,0))

class textBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont('Comic Sans', 18)
        self.textBuffer = ""
        self.image = None
        self.rect = None

    def addText(self,text):
        self.textBuffer += text

    def update(self):
        self.image = self.font.render(self.textBuffer, True, (0,0,0))
        self.rect = self.image.get_rect()
        self.rect.left = 20
        self.rect.top = HEIGHT/2+125

pygame.init()
pygame.font.init()

deck = Deck()
discard = Stack()
timer = Timer()
texter = msgDisplay()
inputBox = textBox()

discard.placeCard(deck.drawCard())

players = [Player([deck.drawCard() for i in range(6)]) for i in range(min(4,input("How many players are there? ")))]

suitChecker = validityCheck()
cardCountChecker = cardCountCheck()
aceChecker = aceCheck()
sevenChecker = sevenCheck()
jackChecker = jackCheck()
queenChecker = queenCheck()
kingChecker = kingCheck()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
background = pygame.Surface((WIDTH,HEIGHT))

bgcolor = (rnd.randrange(0,255),rnd.randrange(0,255),rnd.randrange(0,255))
nplayers = len(players)
playerTurn = 0
curPlayer = players[playerTurn]

clock   = pygame.time.Clock()
sprites = pygame.sprite.Group(deck, discard, timer, texter, inputBox)

checkRules = False
hasPlayed  = False
running = True
knockCount = 0

while running:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            for i in range(len(curPlayer.cards)):
                if curPlayer.cards[i].rect.collidepoint(pygame.mouse.get_pos()) and not hasPlayed: # check rules if we selected a card
                    discard.placeCard(curPlayer.cards.pop(i))
                    checkRules = True
                    hasPlayed  = True
                    knockCount = 0
                    timer.timeLeft = 5
                    break
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if timer.timeLeft > 0 and event.key in range(K_a,K_z+1) + [K_SPACE]: # inputting a rule response
                inputBox.addText(chr(event.key))
            elif timer.timeLeft > 0 and event.key is K_BACKSPACE: # backspace
                inputBox.textBuffer = inputBox.textBuffer[:-1]
            elif not hasPlayed:  # Knock
                checkRules = False
                hasPlayed = False
                knockCount += 1
                playerTurn = (playerTurn + 1) % nplayers
                curPlayer = players[playerTurn]
                if knockCount == len(players):
                    knockCount = 0
                    discard.placeCard(deck.drawCard())

    if checkRules and timer.timeLeft == 0:
        Rules().check()
        inputBox.textBuffer = []
        checkRules = False
        hasPlayed = False
        playerTurn = (playerTurn + 1) % nplayers
        curPlayer = players[playerTurn]

    background.fill(bgcolor)
    sprites.update()
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
