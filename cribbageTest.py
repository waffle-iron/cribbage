from random import shuffle
from random import randint
import copy
import collections
import itertools
from itertools import groupby

def searchForRuns(hand, player):
    runHand = copy.deepcopy(hand)
    #print "in runs"
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
        #TODO: Fix issues with too many runs
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
                            foundRunOf5 = True
                            if checked[i] in dups:
                                multiplier += 1
                            if checked[i+1] in dups:
                                multiplier += 1
                            if checked[i+2] in dups:
                                multiplier += 1
                            if checked[i+3] in dups:
                                multiplier += 1
                            if checked[i+4] in dups:
                                multiplier += 1
                            for i in range(multiplier):
                                print "Run of 5, for 5"
        #TODO: Fix issues with too many runs
        for i in range(0,len(checked)-3):
            if not foundRunOf5:
                if (checked[i]) + 1 == (checked[i+1]):
                    if (checked[i+1]) + 1 == (checked[i+2]):
                        if (checked[i+2]) + 1 == (checked[i+3]):
                            foundRunOf4 = True
                            if checked[i] in dups:
                                multiplier += 1
                            if checked[i+1] in dups:
                                multiplier += 1
                            if checked[i+2] in dups:
                                multiplier += 1
                            if checked[i+3] in dups:
                                multiplier += 1
                            for i in range(multiplier):
                                print "Run of 4, for 4"
        for i in range(0,len(checked)-2):
            if not foundRunOf5:
                if not foundRunOf4:
                    if (checked[i]) + 1 == (checked[i+1]):
                        if (checked[i+1]) + 1 == (checked[i+2]):
                            if checked[i] in dups:
                                multiplier += 1
                            if checked[i+1] in dups:
                                multiplier += 1
                            if checked[i+2] in dups:
                                multiplier += 1
                            for i in range(multiplier):
                                print "Run of 3, for 3"

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

cribHand = ['4 of Hearts', '4 of Spades', '5 of Clubs', '6 of Diamonds', '6 of Clubs']
player = 1

searchForRuns(cribHand, player)
