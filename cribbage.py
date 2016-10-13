from random import shuffle
from random import randint
import copy
import collections
import itertools
from itertools import groupby
import time

cards = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
player1Hand = []
player2Hand = []
player3Hand = []
player4Hand = []
player1HandDup = []
player2HandDup = []
cribHand = []
flipCard = ""
deck = []
player1Score = 0
player2Score = 0
player3Score = 0
player4Score = 0
player1HandCount = 0
player2HandCount = 0
cribCount = 0
player1HandPegs = 0
player2HandPegs = 0
player1TotalPegs = 0
player2TotalPegs = 0
dealer = 0
player = 0
playCount = 0

def setup():
    global humanPlayers
    humanPlayers = input("Please enter the number of human players: ")
    for i in range(0,humanPlayers):
        print "Human " + str(i + 1) + " is player " + str(i + 1)
    global compPlayers
    compPlayers = input("Please enter the number of computer players: ")
    for i in range(0,compPlayers):
        print "The computer is player " + str(i + 2)
    global totalPlayers
    totalPlayers = humanPlayers + compPlayers

    for i in cards:
        for j in suits:
            deck.append(i + " of " + j)

    shuffle(deck)
#only works for 2player
def cutForDeal():
    global dealer
    global player
    if totalPlayers is 2:
        #TODO
        if humanPlayers is 2:
            humanZero = input("Human 0: Please pick a card to cut (0-51): ")
            humanZeroCard = getCard(deck[humanZero])
            humanOne = input("Human 1: Please pick a card to cut (0-51): ")
            humanOneCard = getCard(deck[humanOne])
            #Human 1 won cut
            if cards.index(humanOneCard) > cards.index(humanZeroCard):
                dealer = 2
                print "\nHuman 1 won the cut, you will deal first and have the crib first"
                player = 1
            #Human 0 won cut
            else:
                dealer = 1
                print "\nHuman 0 won the cut, you will deal first and have the crib first"
                player = 2
        else:
            userCut = input("Human: Please pick a card to cut (0-51): ")
            userCutCard = getCard(deck[userCut])
            if compPlayers > 0:
                compCut = randint(0,51)
                compCutCard = getCard(deck[compCut])
            #comp won cut
            if cards.index(compCutCard) > cards.index(userCutCard):
                dealer = 2
                print "\nComputer won the cut, it will deal first and it will have the crib first"
                player = 1
            #human won cut
            else:
                dealer = 1
                print "\nHuman won the cut, you will deal first and have the crib first"
                player = 2
    return dealer
#only works for 2player -- TODO Need to add Nibs scoring
def dealCards():
    global flipCard
    if totalPlayers is 2:
        odd = False
        #used to alternate card dealing
        if dealer is 1:
            odd = True
        for i in deck:
            if len(player1Hand) < 6 or len(player2Hand) < 6:
                #Deal to player 2 first
                if odd:
                    player2Hand.append(i)
                    odd = False
                else:
                    player1Hand.append(i)
                    odd = True
            #Get the flip card after ppl have hands
            elif len(player1Hand) == 6 and len(player2Hand) == 6 and flipCard is not None:
                flipCard = i
#Flip dealer and reset hand based vars
def swapDealer():
    global dealer
    global player
    global player1Hand
    global player2Hand
    global player1HandPegs
    global player2HandPegs
    global cribHand
    if dealer is 1:
        dealer = 2
    elif dealer is 2:
        dealer = 1
    if player is 1:
        player = 2
    elif player is 2:
        player = 1
    player1Hand = []
    player2Hand = []
    cribHand = []
    playCount = 0
    player1HandCount = 0
    player2HandCount = 0
    player1HandPegs = 0
    player2HandPegs = 0
    print "\n***Player " + str(dealer) + " is now the dealer and gets the crib***"
#impl bubble sort
def sortHand(hand):
    for passnum in range(len(hand)-1, 0 , -1):
        for i in range(passnum):
            card1 = getCard(hand[i])
            card2 = getCard(hand[i + 1])
            if cards.index(card1) >= cards.index(card2):
                temp = hand[i]
                hand[i] = hand[i+1]
                hand[i+1] = temp
    return hand
def throwToCrib():
    global player1Score
    global player2Score
    global player1HandPegs
    global player2HandPegs
    global player1TotalPegs
    global player2TotalPegs
    print "\n" + str(player1Hand)
    thrownCard1 = input("Throw some cards, Human! Pick 1-6 as to which card you would like to throw. ") - 1
    cribHand.append(player1Hand[thrownCard1])
    player1Hand.pop(thrownCard1)
    print "\n" + str(player1Hand)
    thrownCard2 = input("One more, Human! Pick 1-5 as to which other card you would like to throw. ") - 1
    cribHand.append(player1Hand[thrownCard2])
    player1Hand.pop(thrownCard2)

    #TODO: Make this AI ridden
    compThrown1 = randint(0,len(player2Hand)-1)
    cribHand.append(player2Hand[thrownCard1])
    player2Hand.pop(compThrown1)
    compThrown2 = randint(0,len(player2Hand)-1)
    cribHand.append(player2Hand[thrownCard2])
    player2Hand.pop(compThrown2)

    print "\n***Flip card is the " + flipCard + "***"
    if getCard(flipCard) == "Jack":
        print "\n~~~~~~~~~~~~Player " + str(dealer) + " got Nibs! 2 points for them~~~~~~~~~~~~"
        if dealer is 1:
            player1Score += 2
            player1HandPegs += 2
            player1TotalPegs += 2
        elif dealer is 2:
            player2Score += 2
            player2HandPegs += 2
            player2TotalPegs += 2

#TODO Scoring pairs and runs
def playGame():
    print "\nTime to play the game!"
    global playCount
    global player
    global player1Score
    global player2Score
    global player1HandPegs
    global player2HandPegs
    global player1TotalPegs
    global player2TotalPegs
    lastPlayed = ""
    handOver = False
    player1HandDup = copy.deepcopy(player1Hand)
    player2HandDup = copy.deepcopy(player2Hand)
    played = False
    playCount = 0
    while not handOver:
        print "\n***Count is at " + str(playCount) + "***"
        if player is 1:
            if player1HandDup:
                legalCards = getLegalCards(player1HandDup, playCount)
                if playCount is 31:
                    print "\n~~~~~~~~~~~~Player 2 hit 31! 2 points for them~~~~~~~~~~~~"
                    player2Score += 2
                    player2HandPegs += 2
                    player2TotalPegs += 2
                    playCount = 0
                elif len(legalCards) is not 0:
                    if playCount is 15:
                        print "\n~~~~~~~~~~~~Player 2 hit 15! 2 points for them~~~~~~~~~~~~"
                        player2Score += 2
                        player2HandPegs += 2
                        player2TotalPegs += 2
                    print "\nLegal Cards: " + str(legalCards)
                    playedCard = input("Play a card, Human! Pick 1-" + str(len(legalCards)) + " as to which card you would like to play. ") - 1
                    playedValue = getCardValue(player1HandDup[playedCard])
                    playCount += int(playedValue)
                    indexInDup = player1HandDup.index(legalCards[playedCard])
                    if lastPlayed:
                        if getCard(legalCards[playedCard]) is getCard(lastPlayed):
                            print "\n~~~~~~~~~~~~Player 1 played a pair! 2 points for them~~~~~~~~~~~~"
                            player1Score += 2
                            player1HandPegs += 2
                            player1TotalPegs += 2
                    lastPlayed = legalCards[playedCard]
                    player1HandDup.pop(indexInDup)
                    player = 2
                else:
                    if playCount is 15:
                        print "\n~~~~~~~~~~~~Player 2 hit 15! 2 points for them~~~~~~~~~~~~"
                        player2Score += 2
                        player2HandPegs += 2
                        player2TotalPegs += 2
                        lastPlayed = ""
                        break
                    print "\n~~~~~~~~~~~~Player 2 gets a go!~~~~~~~~~~~~"
                    player2Score += 1
                    player2HandPegs += 1
                    player2TotalPegs += 1
                    playCount = 0
                    player = 1
                    lastPlayed = ""
            else:
                if not player2HandDup:
                    if playCount is 15:
                        print "\n~~~~~~~~~~~~Player 2 hit 15! 2 points for them~~~~~~~~~~~~"
                        player2Score += 2
                        player2HandPegs += 2
                        player2TotalPegs += 2
                        break
                        lastPlayed = ""
                    print "\n~~~~~~~~~~~~Player 2 gets a go!~~~~~~~~~~~~"
                    print "\n***Hand over***"
                    player2Score += 1
                    player2HandPegs += 1
                    player2TotalPegs += 1
                    handOver = True
        elif player is 2:
            if player2HandDup:
                legalCards = getLegalCards(player2HandDup, playCount)
                if playCount is 31:
                    print "\n~~~~~~~~~~~~Player 1 hit 31! 2 points for them~~~~~~~~~~~~"
                    player1Score += 2
                    player1HandPegs += 2
                    player1TotalPegs += 2
                    playCount = 0
                elif len(legalCards) is not 0:
                    if playCount is 15:
                        print "\n~~~~~~~~~~~~Player 1 hit 15! 2 points for them~~~~~~~~~~~~"
                        player1Score += 2
                        player1HandPegs += 2
                        player1TotalPegs += 2
                    playedCard = randint(0,len(legalCards)-1)
                    playedValue = getCardValue(legalCards[playedCard])
                    print "\nThe computer played the " + str(legalCards[playedCard])
                    playCount += int(playedValue)
                    indexInDup = player2HandDup.index(legalCards[playedCard])
                    if lastPlayed:
                        if getCard(legalCards[playedCard]) is getCard(lastPlayed):
                            print "\n~~~~~~~~~~~~Player 2 played a pair! 2 points for them~~~~~~~~~~~~"
                            player2Score += 2
                            player2HandPegs += 2
                            player2TotalPegs += 2
                    lastPlayed = legalCards[playedCard]
                    player2HandDup.pop(indexInDup)
                    player = 1
                else:
                    if playCount is 15:
                        print "\n~~~~~~~~~~~~Player 2 hit 15! 2 points for them~~~~~~~~~~~~"
                        player1Score += 2
                        player1HandPegs += 2
                        player1TotalPegs += 2
                        lastPlayed = ""
                        break
                    print "\n~~~~~~~~~~~~Player 1 gets a go!~~~~~~~~~~~~"
                    player1Score += 1
                    player1HandPegs += 1
                    player1TotalPegs += 1
                    playCount = 0
                    player = 2
                    lastPlayed = ""
            else:
                if not player1HandDup:
                    if playCount is 15:
                        print "\n~~~~~~~~~~~~Player 2 hit 15! 2 points for them~~~~~~~~~~~~"
                        player1Score += 2
                        player1HandPegs += 2
                        player1TotalPegs += 2
                        break
                        lastPlayed = ""
                    print "\n~~~~~~~~~~~~Player 1 gets a go!~~~~~~~~~~~~"
                    print "\n***Hand over***"
                    player1Score += 1
                    player1HandPegs += 1
                    player1TotalPegs += 1
                    handOver = True

    print "\nHand is over, time to count your cards!"

def countCards():
    global player1Hand
    global player2Hand
    global cribHand
    global player1HandCount
    global player2HandCount
    global cribCount
    player1HandCount = 0
    player2HandCount = 0
    #human count
    player1Hand.append(flipCard)
    player1Hand = sortHand(player1Hand)
    print "Player 1 hand: " + str(player1Hand)
    guessedPoints = input("How many points do you think are in your hand? ")
    score(player1Hand, 1, False)
    if guessedPoints is player1HandCount:
        print "\n***You got it!***\n"
    else:
        print "\n***Actually, you scored " + str(player1HandCount) + "***\n"
    #comp count
    player2Hand.append(flipCard)
    player2Hand = sortHand(player2Hand)
    print "Player 2 hand: " + str(player2Hand)
    score(player2Hand, 2, False)
    #crib count
    cribHand.append(flipCard)
    if dealer is 1:
        tmpP1Score1 = copy.deepcopy(player1Score)
        cribHand = sortHand(cribHand)
        print "\nCrib hand: " + str(cribHand)
        guessedPoints = input("How many points do you think are in the crib? ")
        score(cribHand, 1, True)
        tmpP1Score2 = copy.deepcopy(player1Score)
        cribDiff = tmpP1Score2 - tmpP1Score1
        if guessedPoints is cribDiff:
            print "\n***You got it!***"
        else:
            print "\n***Actually, you scored " + str(cribDiff) + "***"
    elif dealer is 2:
        tmpP1Score1 = copy.deepcopy(player2Score)
        cribHand = sortHand(cribHand)
        print "\nCrib hand: " + str(cribHand)
        score(cribHand, 2, True)
        tmpP1Score2 = copy.deepcopy(player2Score)
def score(hand, player, cribHand):
    searchForPairs(hand, player)
    searchForRuns(hand, player)
    searchForFlush(hand, player, cribHand)
    searchForNobs(hand, player)
    searchFor15s(hand, player)
def searchForPairs(hand, player):
    pairHand = copy.deepcopy(hand)
    #print "in pairs"
    global player1Score
    global player2Score
    global player1HandCount
    global player2HandCount
    cards = []
    for i in range(len(pairHand)):
        cards.append(getCard(pairHand[i]))
    #For player 1
    if player == 1:
        pairs = [len(list(group)) for key, group in groupby(cards)]
        for i in range(len(pairs)):
            if pairs[i] == 2:
                print "Pair for 2"
                player1Score += 2
                player1HandCount += 2
            elif pairs[i] == 3:
                print "Triple for 6"
                player1Score += 6
                player1HandCount += 6
            elif pairs[i] == 4:
                print "Quad for 12"
                player1Score += 12
                player1HandCount += 12
    #For player 2
    if player == 2:
        pairs = [len(list(group)) for key, group in groupby(cards)]
        for i in range(len(pairs)):
            if pairs[i] == 2:
                print "Pair for 2"
                player2Score += 2
                player2HandCount += 2
            elif pairs[i] == 3:
                print "Triple for 6"
                player2Score += 6
                player2HandCount += 6
            elif pairs[i] == 4:
                print "Quad for 12"
                player2Score += 12
                player2HandCount += 12
#TODO: Support run of 5. May need 5 first, then 4, then 3
def searchForRuns(hand, player):
    runHand = copy.deepcopy(hand)
    #print "in runs"
    global player1Score
    global player2Score
    global player1HandCount
    global player2HandCount
    foundRunOf5 = False
    foundRunOf4 = False
    cards = []
    for i in range(len(runHand)):
        cards.append(getRunValue(runHand[i]))
    #For player 1
    if player == 1:
        checked = []
        dups = []
        multiplier = 1
        #Remove dups
        for e in cards:
            if e not in checked:
                checked.append(e)
            else:
                dups.append(e)
        for i in range(0,len(checked)-4):
            if (checked[i]) + 1 == (checked[i+1]):
                if (checked[i+1]) + 1 == (checked[i+2]):
                    if (checked[i+2]) + 1 == (checked[i+3]):
                        if (checked[i+3]) + 1 == (checked[i+4]):
                            print "Run of 5, for 5"
                            foundRunOf5 = True
                            player1Score += (5 * multiplier)
                            player1HandCount += (5 * multiplier)
        for i in range(0,len(checked)-3):
            if not foundRunOf5:
                if (checked[i]) + 1 == (checked[i+1]):
                    if (checked[i+1]) + 1 == (checked[i+2]):
                        if (checked[i+2]) + 1 == (checked[i+3]):
                            foundRunOf4 = True
                            for j in range(0,3):
                                if checked[i+j] in dups:
                                    multiplier *= 2
                            for i in range(multiplier):
                                print "Run of 4, for 4"
                            player1Score += (4 * multiplier)
                            player1HandCount += (4 * multiplier)
        for i in range(0,len(checked)-2):
            if not foundRunOf5:
                if not foundRunOf4:
                    if (checked[i]) + 1 == (checked[i+1]):
                        if (checked[i+1]) + 1 == (checked[i+2]):
                            for j in range(0,3):
                                if checked[i+j] in dups:
                                    multiplier *= 2
                            for i in range(multiplier):
                                print "Run of 3, for 3"
                            player1Score += (3 * multiplier)
                            player1HandCount += (3 * multiplier)
    #For player 2
    if player == 2:
        checked = []
        dups = []
        multiplier = 1
        #Remove dups
        for e in cards:
            if e not in checked:
                checked.append(e)
            else:
                dups.append(e)
        for i in range(0,len(checked)-4):
            if (checked[i]) + 1 == (checked[i+1]):
                if (checked[i+1]) + 1 == (checked[i+2]):
                    if (checked[i+2]) + 1 == (checked[i+3]):
                        if (checked[i+3]) + 1 == (checked[i+4]):
                            print "Run of 5, for 5"
                            foundRunOf5 = True
                            player2Score += (5 * multiplier)
                            player2HandCount += (5 * multiplier)
        for i in range(0,len(checked)-3):
            if not foundRunOf5:
                if (checked[i]) + 1 == (checked[i+1]):
                    if (checked[i+1]) + 1 == (checked[i+2]):
                        if (checked[i+2]) + 1 == (checked[i+3]):
                            foundRunOf4 = True
                            for j in range(0,3):
                                if checked[i+j] in dups:
                                    multiplier *= 2
                            for i in range(multiplier):
                                print "Run of 4, for 4"
                            player2Score += (4 * multiplier)
                            player2HandCount += (4 * multiplier)
        for i in range(0,len(checked)-2):
            if not foundRunOf5:
                if not foundRunOf4:
                    if (checked[i]) + 1 == (checked[i+1]):
                        if (checked[i+1]) + 1 == (checked[i+2]):
                            for j in range(0,3):
                                if checked[i+j] in dups:
                                    multiplier *= 2
                            for i in range(multiplier):
                                print "Run of 3, for 3"
                            player2Score += (3 * multiplier)
                            player2HandCount += (3 * multiplier)
def searchForFlush(hand, player, crib):
    flushHand = copy.deepcopy(hand)
    global player1Score
    global player2Score
    global player1HandCount
    global player2HandCount
    #print "in flush"
    cards = []
    flipCardIndex = flushHand.index(flipCard)
    flushHand.pop(flipCardIndex)
    for i in range(len(flushHand)):
        cards.append(getSuit(flushHand[i]))
    #Fro crib
    if cribHand:
        if cards[1:] == cards[:-1]:
            if getSuit(flipCard) == cards[0]:
                print "Flush for 5"
                if player == 1:
                    player1Score += 5
                    player1Score += 5
                if player == 2:
                    player2Score += 5
                    player2HandCount += 5
    #For player 1
    if player == 1:
        if cards[1:] == cards[:-1]:
            if getSuit(flipCard) == cards[0]:
                print "Flush for 5"
                player1Score += 1
                player1HandCount += 1
            else:
                print "Flush for 4"
                player1Score += 4
                player1HandCount += 4
    #For player 2
    if player == 2:
        if cards[1:] == cards[:-1]:
            if getSuit(flipCard) == cards[0]:
                print "Flush for 5"
                player2Score += 1
                player2HandCount += 1
            else:
                print "Flush for 4"
                player2Score += 4
                player2HandCount += 4
def searchForNobs(hand, player):
    nobHand = copy.deepcopy(hand)
    global player1Score
    global player2Score
    global player1HandCount
    global player2HandCount
    #print "in nobs"
    cards = []
    flipCardIndex = nobHand.index(flipCard)
    nobHand.pop(flipCardIndex)
    for i in range(len(nobHand)):
        if getCard(nobHand[i]) == "Jack":
            cards.append(getSuit(nobHand[i]))
    #For player 1
    if player == 1:
        if getSuit(flipCard) in cards:
            print "Nobs for 1"
            player1Score += 1
            player1HandCount += 1
    #For player 2
    if player == 2:
        if getSuit(flipCard) in cards:
            print "Nobs for 1"
            player2Score += 1
            player2HandCount += 1
def searchFor15s(hand, player):
    fifteeenHand = copy.deepcopy(hand)
    global player1Score
    global player2Score
    global player1HandCount
    global player2HandCount
    #print "in 15s"
    cards = []
    for i in range(len(fifteeenHand)):
        cards.append(getCardValue(fifteeenHand[i]))
    #For player 1
    if player == 1:
        arr = filter(lambda v: sum(v) == 15, powerset(cards))
        for i in range(len(arr)):
            print "15 for 2"
            player1Score += 2
            player1HandCount += 2
    #For player 2
    if player == 2:
        arr = filter(lambda v: sum(v) == 15, powerset(cards))
        for i in range(len(arr)):
            print "15 for 2"
            player2Score += 2
            player2HandCount += 2

def powerset(l):
    return itertools.chain.from_iterable((itertools.combinations(l, i) for i in range(len(l)+1)))
def getCard(card):
    arr = card.split(" of ")
    return arr[0]
def getSuit(card):
    arr = card.split(" of ")
    return arr[1]
def getCardValue(card):
    arr = card.split(" of ")
    if arr[0] == 'Ace':
        value = 1
    elif arr[0] == 'Jack':
        value = 10
    elif arr[0] == 'Queen':
        value = 10
    elif arr[0] == 'King':
        value = 10
    else:
        value = int(arr[0])
    return value
def getRunValue(card):
    arr = card.split(" of ")
    if arr[0] == "Ace":
        value = 1
    elif arr[0] == "Jack":
        value = 11
    elif arr[0] == "Queen":
        value = 12
    elif arr[0] == "King":
        value = 13
    else:
        value = (int)(arr[0])
    return value
def getLegalCards(hand, count):
    retHand = []
    for i in range(len(hand)):
        if count + int(getCardValue(hand[i])) <= 31:
            retHand.append(getCard(hand[i]) + " of " + getSuit(hand[i]))
    return retHand

setup()
dealer = cutForDeal()
while player1Score < 121 and player2Score < 121:
    dealCards()
    player1Hand = sortHand(player1Hand)
    player2Hand = sortHand(player2Hand)
    throwToCrib()
    playGame()
    countCards()
    print "\nPlayer 1 pegs THAT HAND: " + str(player1HandPegs)
    print "Player 1 overall pegs: " + str(player1TotalPegs)
    print "Player 1 points THAT HAND: " + str(player1HandCount)
    print "Player 1 overall points: " + str(player1Score)
    print "\nPlayer 2 pegs THAT HAND: " + str(player2HandPegs)
    print "Player 2 overall pegs: " + str(player2TotalPegs)
    print "Player 2 points THAT HAND: " + str(player2HandCount)
    print "Player 2 overall points: " + str(player2Score)
    for i in range(0,7):
        print "\nShuffling the deck..."
        time.sleep(1)
        shuffle(deck)
    swapDealer()
print "\n***GAME OVER***"
if player1Score >= 121:
    print "\n***Player 1 wins!!!***"
elif player2Score >= 121:
    print "\n***Player 2 wins!!!***"
