# Poker AI Assistant Project (Poker Bot)

## Introduction
This is a project I started in order to further familiarize myself with Python and web development. Since this is a smaller project, I've decided to use Flask as my framework and make use of an AI API. I thought that this project could be very interesting and useful to someone who enjoys poker, but wants to improve their statistical and strategical moves in the game. I also intend to use this program in order to improve my own playing, so I would like to make this application as practical as I can.

## Scope
Features that will be implemented into this program will be as follows:
* Game Play
  - Being able to play the game while acquiring useful advice can help you get experience that will improve your real-time strategies and decisions
  - There will be variability with pots, players and antes that the user can edit in order to fit their desired game settings
* Move Recommendation
  - There will be a specialized recommendation that takes into account statistics, play style, and the amount of money
* Summary
  - There will be a end-of-game summary giving an explanation of how the game went, how much you've deviated away from your playstyle, and how you could improve in the future.

## Endpoint Documentation
### Game Information
* Endpoint name: Game Info
* Description: Give our AI some initial game information 
* Endpoint Type: GET (post?)
* Endpoint: \game_info\
* Parameters: Strings, Ints
* Return Type: JSON

Example Request:
  http://127.0.0.1:8000/game_info/?players=3&buy_in=200&ante=5&difficulty=easy
  
Example Response:
```
  {
    "status": "success"
  }
```
Error Handling: 400 (Required field missing, Ante higher than buy in)

### Initialize Cards
* Endpoint name: Initialize
* Description: Retrieve Cards for players and the playing turns (flop, river, turn)
* Endpoint Type: GET
* Endpoint: \initiate\
* Parameters: Strings, Ints
* Return Type: JSON

Example Request:
  http://127.0.0.1:8000/initiate/?players=3
  
Example Response:
```
  {
    "0": [["A", "spade"], ['7', 'spade]],
    "1": [["10", "diamond"], ['J', 'heart]],
    "2": [["4", "club"], ['5', 'club]],
    "playing": [["K", "heart], ["3", "spade], ["Q", "club], ["2", "heart],["8", "diamond]]
  }
```
Error Handling: 400 (Required field missing, Ante higher than buy in)

### Turn
* Endpoint name: Progression of the game depending on user's last move
* Description: Based on the last action by the user, AI will analyze your move and play the game from all the other players' POV.
* Endpoint Type: GET
* Endpoint: \turn\
* Parameters: Strings, Ints
* Return Type: JSON

Example Request:
  http://127.0.0.1:8000/turn/?move=raise&amount=100&turn=preflop
  http://127.0.0.1:8000/turn/?move=fold&turn=river
  http://127.0.0.1:8000/turn/?move=start&button=2
  
Example Response:
```
  {
    "player1": "fold",
    "player2": "call",
    "player3": "raise 200",
    "turn": "preflop"
  } 
``` 

Example Request:
  http://127.0.0.1:8000/turn/?move=fold&turn=preflop
  
Example Response:
Raise:
```
  {
    result: "player 2 calls player 3's raise. The river is turned and there is a two of hearts, 
10 of spades, J of hearts. Player 2 checks, but player 3 raises 100. Player 2 folds and player 3
wins $500. Player 3 had 10 of hearts and 10 of diamonds, while player 2 had 4 of hearts and 5 of hearts. 
  }
```

### Recommendation
* Endpoint name: Recommendation
* Description: Provide a couple recommendations based on statistics, play style, and budget
* Endpoint Type: GET
* Endpoint: \recommend\
* Parameters: Strings
* Return Type: JSON 
Example Request:
  http://127.0.0.1:8000/recommend/
Example Response:
```
  {
    "recommendation" : "With a hand of Ace-King of spades and a flop of Queen, Ten, Jack of spades,
you have flopped the nut straight flush, which is an incredibly strong hand. Given that the player
before you raised to 100 in an $800 pot, you want to maximize your potential winnings.

  You should consider raising in this situation to build the pot further. Since you have such a
strong hand, you want to extract as much value as possible from your opponents, especially since
there's a high likelihood that someone else might have a strong hand with a spade flush or possibly
even a full house. Consider raising to at least 300-400 to put pressure on your opponents and increase
the size of the pot. "
  }
```



