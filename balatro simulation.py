import numpy as np
import pandas as pd
import itertools as it

def createDeck(uniqueReturn = None):
    if (uniqueReturn != None): assert len(uniqueReturn) == 8
    """
    Create a new deck
    Output: 52 card pandas dataframe
    """
    suits = ['H', 'D', 'C', 'S']
    rank = [str(i) for i in range(2, 11)]  # Starts from 2 to 10
    face = ['J', 'Q', 'K', 'A']
    
    deck = []
    for suit in suits:
        for r in rank:
            deck.append(r + suit)
        for f in face:
            deck.append(f + suit)

    ranks = [card[:-1] for card in deck]
    suits_ = [card[-1:] for card in deck]

    df = pd.DataFrame({'Card': deck, 'Rank': ranks, 'Suit': suits_})

    # Assigning score for cards
    scores = []
    for r in ranks:
        if r in face:
            scores.append(10 if r != 'A' else 11)
        else:
            scores.append(int(r))

    rank_id = []
    for r in ranks:
        if r in face:
            if r == 'J':
                rank_id.append(11)
            elif r == 'Q':
                rank_id.append(12)
            elif r == 'K':
                rank_id.append(13)
            elif r == 'A':
                rank_id.append(14)
        else:
            rank_id.append(int(r))

    df['Scores'] = scores
    df['RankID'] = rank_id
    if (uniqueReturn == None):
        return df
    else:
        return df.iloc[uniqueReturn]

def findHands(deck, hand):
    """
    Return a list of tuples of what cards are played and what the name of the hand is
    """
    assert len(hand) == 8
    hands = []

    for h in list(it.combinations(hand.index, 5)):
        handDF = deck.iloc[np.array(h)]
        handDF = handDF.sort_values(by='RankID')
        isFlush = len(handDF['Suit'].value_counts()) == 1
        isStraight = (handDF['RankID'].diff().dropna() == 1).all()

        if isFlush:
            if isStraight:
                if handDF['RankID'].min() == 10:
                    hands.append(("Royal Flush", handDF.index))
                else:
                    hands.append(("Straight Flush", handDF.index))
            else:
                hands.append(("Flush", handDF.index))
        if handDF['RankID'].value_counts().max() == 4:
            hands.append(("4 of a kind", handDF[handDF['RankID'] == handDF['RankID'].value_counts().idxmax()].index))
            hands.append(("3 of a kind", handDF[handDF['RankID'] == handDF['RankID'].value_counts().idxmax()].index[:3]))
            hands.append(("Pair", handDF[handDF['RankID'] == handDF['RankID'].value_counts().idxmax()].index[:2]))
        if handDF['RankID'].value_counts().max() == 3:
            if handDF['RankID'].value_counts().min() == 2:
                hands.append(("Full House", handDF.index))
                hands.append(("3 of a kind", handDF[handDF['RankID'] == handDF['RankID'].value_counts().idxmax()].index))
                hands.append(("pair", handDF[handDF['RankID'] == handDF['RankID'].value_counts().idxmin()].index))
            else:
                hands.append(("3 of a kind", handDF[handDF['RankID'] == handDF['RankID'].value_counts().idxmax()].index))
                hands.append(("pair", handDF[handDF['RankID'] == handDF['RankID'].value_counts().idxmax()].index[:2]))
                hands.append(("pair", handDF[handDF['RankID'] == handDF['RankID'].value_counts().idxmax()].index[2:]))
                hands.append(("pair", handDF[handDF['RankID'] == handDF['RankID'].value_counts().idxmax()].index[1:-1]))
        if isStraight and not isFlush:
            hands.append(("Straight", handDF.index))
        if handDF['RankID'].value_counts().max() == 2:
            if handDF['RankID'].value_counts().tolist().count(2) == 2:
                counts = handDF['RankID'].value_counts()
                twos = counts[counts == 2].index
                hands.append(("Two Pair", handDF[handDF['RankID'].isin(twos)].index))
            else:
                hands.append(("Pair", handDF[handDF['RankID'] == handDF['RankID'].value_counts().idxmax()].index))
        for x in handDF.index:
            hands.append(("High Card",[x]))
        

    return hands

def getBaseScore(hand_name):
    """
    Calculate the base score before modifiers and cards played
    """
    hand_scores = {
        'High Card': (5, 1),
        'Pair': (10, 2),
        'Two Pair': (20, 2),
        '3 of a kind': (30, 3),
        'Straight': (30, 4),
        'Flush': (35, 4),
        'Full House': (40, 4),
        '4 of a kind': (60, 7),
        'Straight Flush': (100, 8),
        'Royal Flush': (100, 8),
    }
    return hand_scores.get(hand_name, (0, 0))

def convertHandsToDF(possibleHands):
    """
    Processes tuples of possible hands
    Input: [("string"),HandDF]
    """

    handNames = []
    handIndicies = []

    for name,id in possibleHands:
        handNames.append(name)
        handIndicies.append(list(id))

    card1 = []
    card2 = []
    card3 = []
    card4 = []
    card5 = []

    for x in handIndicies:
        numplayed = len(x)
        card1.append(x[0])
        if (numplayed >= 2): card2.append(x[1])
        else: card2.append(-1)
        if (numplayed >= 3): card3.append(x[2])
        else: card3.append(-1)
        if (numplayed >= 4): card4.append(x[3])
        else: card4.append(-1)
        if (numplayed >= 5): card5.append(x[4])
        else: card5.append(-1)


    scoringDF = pd.DataFrame({
        'Name': handNames,
        'Card1':card1,
        'Card2':card2,
        'Card3':card3,
        'Card4':card4,
        'Card5':card5
        })

    return scoringDF.drop_duplicates()

def printHandByGroup (hand):
    print("High Card")
    print(hand[hand['Name'] == 'High Card'])
    print("")
    print("Pair")
    print(hand[hand['Name'] == 'Pair'])
    print("")
    print("Two Pair")
    print(hand[hand['Name'] == 'Two Pair'])
    print("")
    print("3 of a kind")
    print(hand[hand['Name'] == '3 of a kind'])
    print("")
    print("Straight")
    print(hand[hand['Name'] == 'Straight'])
    print("")
    print("Flush")
    print(hand[hand['Name'] == 'Flush'])
    print("")
    print("Full House")
    print(hand[hand['Name'] == 'Full House'])
    print("")
    print("4 of a kind")
    print(hand[hand['Name'] == '4 of a kind'])
    print("")
    print("Straight Flush")
    print(hand[hand['Name'] == 'Straight Flush'])
    print("")
    print("Royal Flush")
    print(hand[hand['Name'] == 'Royal Flush'])

def getOneScoringDF(deck):
    hand = deck.sample(8, replace=False)
    possibleHands = findHands(deck,hand)
    scoringDF = convertHandsToDF(possibleHands)
    scoringDF['BaseScore'] = [getBaseScore(x) for x in scoringDF['Name']]
    card1Score = np.array(scoringDF['Card1'])
    card2Score = np.array(scoringDF['Card2'])
    card3Score = np.array(scoringDF['Card3'])
    card4Score = np.array(scoringDF['Card4'])
    card5Score = np.array(scoringDF['Card5'])
    for i in range(len(card1Score)):
        if card1Score[i] == -1: card1Score[i] = 0
        else: card1Score[i] = deckDF.iloc[card1Score[i]]['Scores']
    for i in range(len(card2Score)):
        if card2Score[i] == -1: card2Score[i] = 0
        else: card2Score[i] = deckDF.iloc[card2Score[i]]['Scores']
    for i in range(len(card3Score)):
        if card3Score[i] == -1: card3Score[i] = 0
        else: card3Score[i] = deckDF.iloc[card3Score[i]]['Scores']
    for i in range(len(card4Score)):
        if card4Score[i] == -1: card4Score[i] = 0
        else: card4Score[i] = deckDF.iloc[card4Score[i]]['Scores']
    for i in range(len(card5Score)):
        if card5Score[i] == -1: card5Score[i] = 0
        else: card5Score[i] = deckDF.iloc[card5Score[i]]['Scores']
    cardScores = card1Score + card2Score + card3Score + card4Score + card5Score
    baseScore = np.array([x[0] for x in scoringDF['BaseScore']])
    baseMult = np.array([x[1] for x in scoringDF['BaseScore']])
    scoringDF['Score'] = (cardScores + baseScore) * baseMult
    return scoringDF


deckDF = createDeck()
print(deckDF)
once = getOneScoringDF(deckDF)
print(once)
