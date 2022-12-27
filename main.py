# blackjack game - original credit/code by Al Sweigart (Inventwithpython.com)

import random
import sys

# set up card constants
HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)
BACKSIDE = 'backside'


def main():
    print('''
    Blackjack game.
    Try to get to 21 without going over. The dealer must stop at 17.
    Press [H] to hit
    Press [S] to stand
    Press [D] to double down
    ''')

    money = 5000
    while True:
        # check for balance
        if money <= 0:
            print("You're out of money. Play again.")
            sys.exit()

        # enter the bet
        print('Money: ', money)
        bet = getBet(money)

        # give dealer and player two cards
        deck = getDeck()
        # pull 2 cards from the deck
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        # player's turn
        print('Bet: '), bet
        while True:
            displayHands(playerHand, dealerHand, False)
            print()

            # check if player busts
            if getHandValue(playerHand) > 21:
                break
            # get player's move
            move = getMove(playerHand, money - bet)

            if move == "D":
                # double down
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print('Bet increased to {}'.format(bet))
                print('Bet: ', bet)

            # if move is a hit or double, add a card
            if move in ('H', 'D'):
                newCard = deck.pop()
                rank, suit = newCard
                print('You drew a {} of {}.'.format(rank, suit))
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    # bust
                    continue

            if move in ('S', 'D'):
                # stand or double down = no more cards
                break

        # handle dealer moves
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                print('Dealer hits...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    # dealer busts
                    break
                input('Press Enter to continue...')
                print('\n\n')

        # show final hands
        displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)

        # handle win/loss/tie
        if dealerValue > 21:
            print('Dealer busts! You win ${}!'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('You lost!')
            money -= bet
        elif playerValue > dealerValue:
            print('You won ${}!'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print('Push, bet is returned.')

        input('Press Enter to continue...')
        print('\n\n')


# define function for player bet
def getBet(maxBet):
    while True:
        print('How much do you want to bet? (1-{}, or QUIT)'.format(maxBet))
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if not bet.isdecimal():
            print('Enter a valid bet amount.')
            continue

        bet = int(bet)
        # ensure bet can be pulled from balance
        if 1 <= bet <= maxBet:
            return bet


# generate the deck
def getDeck():
    # return a list of tuples for all 52 cards
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            # add numbered cards
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            # add face cards
            deck.append((rank, suit))
        # shuffle deck
    random.shuffle(deck)
    return deck


def displayHands(playerHand, dealerHand, showDealerHand):
    # show player's hand, hide dealer's first card if showDealerHand = false
    print()
    if showDealerHand:
        print('DEALER: ', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        # hide the first dealer card
        displayCards([BACKSIDE] + dealerHand[1:])

    # show player's cards
    print('PLAYER: ', getHandValue(playerHand))
    displayCards(playerHand)


# returns the value of the cards
# face cards are worth 10, aces are worth 1 or 11 (automatically picked)
def getHandValue(cards):
    value = 0
    numberOfAces = 0

    # add the value for the non-ace cards:
    for card in cards:
        rank = card[0]
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)

    # add value for aces, starting with 1 for each ace
    value += numberOfAces
    for i in range(numberOfAces):
        # if another 10 can be added without busting, do it
        if value + 10 <= 21:
            value += 10

    return value


# display all the cards
def displayCards(cards):
    rows = ['', '', '', '', '']

    for i, card in enumerate(cards):
        # print top line of card
        rows[0] += ' ___  '
        if card == BACKSIDE:
            # print the card's back
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            # print card front
            rank, suit = card
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

        # print each row on screen
        for row in rows:

        print(row)


def getMove(playerHand, money):
    # asks player for move, returns H for Hit, S for Stand, and D for Double Down
    while True:
        # determine what moves player can make
        moves = ['(H)it', '(S)tand']

        # player can double down on first move (2 cards)
        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')

        # get player's move
        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            return move  # player has entered a valid move
        if move == 'D' and '(D)ouble down' in moves:
            return move  # player has enter a valid move


# if program is run (instead of imported) run the game
if __name__ == "__main__":
    main()






