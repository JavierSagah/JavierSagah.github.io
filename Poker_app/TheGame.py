# this class contains the behavior of the actual poker gaming stage
# Checks for the minimum number of players to be 2
# the button it is given to the last player that joined the table
# the table will accept only up to the max number of players allowed (8)
# player1 starts with the small blind and player2 the big blind
#   - if there is only 2 players, player 2 will be the button holder and player1 the one on the left of the button
#   - if 3 or more players, player1 is on the left of the button holder and player 2 on the left of player1
# blinds and button move clockwise after every round
# cards are dealt clockwise starting by the player on the left of the button
# so that the last card is dealt to the button holder
# flop + turn + river = the board
# each player will have a combination of 7 cards( the board + their 2 cards at hand) to make a game for them
# this includes any combination of 5 cards from the 7 which can include both of the players cards, one, or none
# betting rounds:
#   - 1st round: the round of betting when each player has two cards only.
#   - 2nd round: the round of betting when each player has two hole cards and there are three exposed common cards.
#   - 3rd round: the round of betting when each player has two hole cards and there are four exposed common cards.
#   - 4th round: the final round of betting when each player has two hole cards and there are four exposed common cards.
# there is a special type of bet called all-in
#   - all-in puts every chips of the player into the pot and forces the other players to call or fold ONLY
#   - the players that called will have their cards shown this includes the player who called all-in
#   - all-in can happen in any betting round
# players cards will be shown:
#   - for all players that did not fold when all-in was called
#   - for all players that did not fall at the end of the last round of bets
#
# GAME:
# shuffle cards
# 1st round of bets: clockwise ending on player2 (big blind)
#   - the small and big blinds are set by the table or
#     the small blind is set by the player on the left of the button
#   - the big blind is twice the small blind
#   - 2 cards are dealt first: 1 card each player from player1 to player_n then the second card in the same manner.
#   - Ending at the big blind all players have their turn to bet (clockwise)
#       call: if small blind, matches the big blind or highest bet
#               if big blind, nothing is added. If there is a higher bet, matches that bet. Ends the first betting round
#               button and any other player, matches the big blind or highest bet
#       fold: if small blind or big blind, player is out of this round and loses his blind bet. It goes into the pot
#             if button and any other player, loses nothing and is out of this round
#             the player's cards cannot be seen by others
#       check: available at the end of the round. Only for the big blind player or the player who set the highest bet
#              it adds no more chips to the betting round, just ends the first betting round
#       rise: sets a new highest bet for this round and this player becomes the end of the betting round
#              all players have this option
# the flop: 3 cards are put on the table facing up
# 2nd round of bets: clockwise from player1 to button holder
#    - same as the first round of bets but no small and big blinds exist here
#      everything now is based on the position of the button which marks the end of each round
# the turn: the fourth card is put on the table facing up
# 3rd round of bets
#    - procedure is same as the second round of bets
# the river: the fifth and last card is put on the table facing up
# the final round of bets
#    - procedure is same as 2nd and 3rd round of bets + end of game
#
# End of Game:
# - if all but one player fold or quit at any point in game,
#   game ends and full pot goes to that player and no player cards are shown.
# - whenever all-in is called and there are at least 2 remaining players in the round,
#   only those players' cards will be shown and the board will be completed,
#   the winner will be decided and the game will end.
# - the player with the best hand wins. The best hand is decided based on the "hand value rules"
# - in case of more than one winne (tie occurs among the remaining players) the pot will be evenly split among them
#
# Hand value rules:
# - High card: Simple value of the card. Lowest: 2 - Highest: Ace
# - Pair:	Two cards with the same value
# - Two pairs: Two times two cards with the same value
# - Three of a kind: Three cards with the same value
# - Straight: Sequence of 5 cards of any suit in increasing value (Ace can precede 2 and follow up King)
# - Flush: 5 cards of any value but all the same suit
# - Full house: Combination of three of a kind and a pair
# - Four of a kind: Four cards of the same value
# - Straight flush: Straight of the same suit
# - Royal flush: Straight flush from Ten to Ace. This is the highest hand in the game.
#
# In the case of more than one player with the same hand value:
# - High card: When No Player Has Even A Pair, Then The Highest Card Wins.
#   When Both Players Have Identical High Cards, The Next Highest Card Wins, And So On Until Five Cards Have Been Used.
#   In The Unusual Circumstance That Two Players Hold The Identical Five Cards, The Pot Would Be Split.
# - Pair: If Two Or More Players Hold A Single Pair Then Highest Pair Wins.
#   If The Pairs Are Of The Same Value, The Highest Kicker (any of the 5 cards in a hand that is not in the combo)
#   card determines the winner.
#   A Second And Even Third Kicker Can Be Used If Necessary.
# - Two pairs: The Highest Pair Is Used To Determine The Winner.
#   If Two Or More Players Have The Same Highest Pair, Then The Highest Of The Second Pair Determines The Winner.
#   If Both Players Hold Identical Two Pairs, The Fifth Card Is Used To Break The Tie.
# - Three of a kind: If More Than One Player Holds Three Of A Kind, Then The Higher Value Of The Cards Used To Make
#   The Three Of A Kind Determines The Winner. If Two Or More Players Have The Same Three Of A Kind,
#   Then A Fourth Card (And A Fifth If Necessary) Can Be Used As Kickers To Determine The Winner.
# - Straight: If More Than One Player Has A Straight, The Straight Ending In The highest card Wins.
#   If Both Straights End In A Card Of The Same Strength, The Hand Is Tied.
# - Flush: If Two Or More Players Hold A Flush, The Flush With The Highest Card Wins.
#   If More Than One Player Has The Same Strength High Card, Then The Strength Of The Second Highest Card Held Wins.
#   This Continues Through The Five Highest Cards In The Player's Hands.
# - Full house: When Two Or More Players Have Full Houses, We Look First At The Strength Of The Three Of A Kind
#   To Determine The Winner. For Example, Aces Full Of Deuces (AAA22) Beats Kings Full Of Jacks (KKKJJ).
#   If There Are Three Of A Kind On The Table (Community Cards) that Are Used By Two Or More Players
#   to Make A Full House, Then We Would Look At The Strength Of The Pair To Determine A Winner.
# - Four of a kind: Four Aces Beats Any Other Four Of A Kind, Four Kings Beats Four Queens Or Less And So On.
#   The Only Tricky Part Of A Tie Breaker With Four Of A Kind Is When The Four Falls On The Table In A Game
#   And Is Therefore Shared Between Two (Or More) Players. A Kicker Can Be Used, However,
#   If The Fifth Community Card Is Higher Than Any Card Held By Any Player Still In The Hand,
#   Then The Hand Is Considered A Tie And The Pot Is Split.
# - Straight flush: A King High Straight Flush Loses Only To A Royal. If More Than One Player Has A Straight Flush,
#   The Winner Is The Player With The Highest Card Used In The Straight. The suit has no effect.
# - Royal flush: Between Two Royal Flushes, There Can Be No Tie Breaker. If Two Players Have Royal Flushes,
#   They Split The Pot. This is almost impossible to happen.

