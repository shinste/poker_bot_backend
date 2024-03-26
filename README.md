# Poker AI Assistant Project (Poker Bot Backend Documentation)

## Introduction
Hello, welcome to my poker AI assistant platform, where players can elevate their poker skills with real-time AI analysis and recommendations. Whether you're a seasoned pro or a newcomer to the poker scene, this project provides personalized assistance, strategic insights, and smooth gameplay that will sharpen your skills.

I chose to develop this project with the goal of deepning my understanding of web development and enhancing user experience. Choosing React as my frontend framework, and implementing OpenAI into a Django backend, I saw an opportunity to create a practical and entertaining way to utilize AI for learning. 

I was driven to develope a single-page application in order to focus directly on functionality and usability for the user. I've also decided to minimize the use of API calls and abstaining from using a database. This approach not only refined my TypeScript proficiency but also improve my problem-solving and debugging skills in ReactJS. Because this is a backend documentation repository, it only has 5 different API calls I will elaborate on. By centralizing the application's logic in the frontend, I aim to craft a simple yet effective learning tool for people to enhance their poker strategy through experience.

## Hosted Project
#### Note:
For cost purposes, the EC2 instance that hosts this app will be scheduled to run between 9AM - 5PM (Pacific), Mon - Fri.

* [PokerBot](https://main--pokerbot.netlify.app/)
  - Hosted Through Netlify
### 
* [Frontend Documentation](https://github.com/shinste/poker_bot_frontend)

#### Looking for my Portfolio?
* [Portfolio](https://master--stephenshinportfolio.netlify.app/)

## Scope
Poker Bot allows you to play unlimited games of poker with computer AI opponents. It provides adjustable settings for different levels of play and specific betting amounts. Instead of dollars, the currency used to gamble in this program are simply "Chips". Before you play, you will first be prompted to adjust the number of opponents to play, buy in ammount, big bet amount, and difficulty.
* Gameplay
  - Gameplay-wise, the program will operate under the rules of Texas Hold 'Em. It will implement small blinds, big blinds, minimum reraises, and many more. There will be a couple of caveats to the rules that will be mentioned below
  - There will be variability with pots, players and antes that the user can edit in order to fit their desired game settings
  - Opponent cards will be shown at the end of the game, or if you have folded. 
* Move Recommendation
  - Not sure what to do? Opt for the "Give me a suggestion" button that will prompt an AI to generate advice based on your hand, community cards, and opponent moves. AI isn't perfect, so it isn't impossible for the advice or given information to be exactly correct!
* Feed Back
  - There will be a end-of-game summary button that prompts AI to give an explanation of how the current game went, what you've played well, and how you could improve in the future.
* Exceptions to the rules
  - All In Winnings: Under normal rules, what happens when you win a round after going all in, but other players had bet more money than the amount that you pushed? That winner gains ONLY that amount from each player, but the rest of the money is then seen as a sidepot, and it will go to the player with the second best hand. In this program, only the former part of this rule applies. The winner receives their rightful share of money, but the rest of the money is sent back to their rightful owners.

## Endpoint Documentation

### Initialize
* Endpoint name: Initialize Game
* Description: This endpoint handles the randomizing of cards/suites to all of the players and community cards. It will be returned as a JSON with numbers as keys, which refer to each player, and the cards value and suite type as each value for those keys. The "playing" key will be 5 randomized cards that will be for the flop, turn, and river.
* Endpoint Type: GET
* Endpoint: \initiate\  
* Parameters: Integer
* Return Type: JSON

Example Request:
  https://pokerbotbackend.applikuapp.com/initiate/?players=3
  
Example Response:
```
  {
    "0": [["A", "spade"], [7, 'spade]],
    "1": [[10, "diamond"], ['J', 'heart]],
    "2": [[4, "club"], [5, 'club]],
    "playing": [["K", "heart], [3, "spade], [Q, "club], [2, "heart],[8, "diamond]]
  }
```
Error Handling: 400 (Required field missing)

### AI Move
* Endpoint name: Move
* Description: This will prompt the AI to make a legal poker move for a player based on information such as what turn it is, current bet, budget, cards, etc.
* Endpoint Type: POST
* Endpoint: \ai_move\
* Parameters: Integers, Strings, Dictionary
* Return Type: JSON

Example Request:
  https://pokerbotbackend.applikuapp.com/ai_move/
  Body: 
  ```
  {
    player: 1,
    turn: 2,
    current_bet: 50,
    budget: 300,
    cards: {
              "0": [["A", "spade"], [7, 'spade]],
              "1": [[10, "diamond"], ['J', 'heart]],
              "2": [[4, "club"], [5, 'club]],
              "playing": [["K", "heart], [3, "spade], ["Q", "club], [2, "heart],[8, "diamond]]
            },
    committed: 100,
    commitRound: 20,
    difficulty: 'Professional',
    best: 'J High'
  }
```

Example Response:
```
{
  'move': raise,
  'bet_increase': 10
}
```

Error Handling: 400 (Required field missing), 500 (Issues with OpenAI)
  
### AI Suggestion
* Endpoint name: Suggestion
* Description: This will prompt the AI to make an analytical suggestion or recommendation on what the user should do in the current spot he/she is in based on information such as turn, hand, budget, etc.
* Endpoint Type: POST
* Endpoint: \ai_feedback\
* Parameters: Strings, Ints, Lists
* Return Type: JSON

Example Request:
  https://pokerbotbackend.applikuapp.com\ai_feedback\
  Body:
  ```
  {
    turn: 'Flop',
    current_bet: 0,
    budget: 300,
    hand: [[10, 'heart'], [2, 'spade']],
    community: [['J', 'heart'], ['A', 'spade'], [9, 'diamond']],
    committedRound: 20,
    committedTurn: 0,
    conversationContext: ["Player 2 has bought back in!", "Player 2's Move: call", "Player 3's Move: call",…],
    players: 4,
    best: '10 High'
  }
  ```
  
Example Response:
```
  {
    "suggest": "Based on your current hand (10 High) and the community cards on the table (9, A, J), you have a weak hand. Stronger hands that could beat you include a pair of Aces, a pair of Jacks, and potentially a straight or flush draw. Based on the betting history, since all players have just called the previous round, it is likely that a few of them are on drawing hands or have marginal holdings. Given that the pot odds are good and you are yet to invest anything in this turn, it might be worth seeing the next card. SUGGESTED MOVE: CHECK"
  } 
```
Error Handling: 400 (Required field missing), 500 (Issues with OpenAI)

### AI Feedback
* Endpoint name: Feedback
* Description: Provides post game feedback about how the game was played by the user, issues that they could've made, and how to improve.
* Endpoint Type: POST
* Endpoint: \ai_feedback\
* Parameters: Lists
* Return Type: JSON 
Example Request:
  https://pokerbotbackend.applikuapp.com/recommend/
  Body:
  ```
  {
    cards: {
              "0": [["A", "spade"], [7, 'spade]],
              "1": [[10, "diamond"], ['J', 'heart]],
              "2": [[4, "club"], [5, 'club]],
              "playing": [["K", "heart], [3, "spade], ["Q", "club], [2, "heart],[8, "diamond]]
            },
    history: ["Player 2 has bought back in!", "Player 2's Move: call", "Player 3's Move: call",…]
  }
  ```
Example Response:
```
  {
    "feedback" : "Based on the game history provided, you played passively by consistently checking rather than betting or raising, which likely resulted in losing the hand despite having the opportunity to potentially bluff or bet stronger hands. One blunder was not taking more control of the betting rounds, allowing your opponents to easily stay in the game and ultimately leading to a loss with a weaker hand. To improve, consider being more aggressive with your betting strategy, especially when the community cards offer potential strong hands, and avoid being too passive throughout the game."
  }
```
Error Handling: 400 (Required field missing), 500 (Issues with OpenAI)

### Tie Breaker
* Endpoint name: Tie Breaker
* Description: Calculates which player's hand would win the round in a tie. I've decided to implement this logic in Django because ties in Poker aren't very common.
* Endpoint Type: POST
* Endpoint: \tiebreaker\
* Parameters: Strings, Integers
* Return Type: JSON

Example Request:
  https://pokerbotbackend.applikuapp.com/tiebreaker/
  Body:
  ```
  {
    cards: {
              "0": [["A", "spade"], [7, 'spade]],
              "1": [[7, "diamond"], ['J', 'heart]],
              "2": [[4, "club"], [5, 'club]],
              "playing": [["K", "heart], [7, "spade], ["Q", "club], [2, "heart],[8, "diamond]]
            },
    hand: '7 High Pair',
    ties: ['0', '1']
  }
  ```
  
Example Response:
```
  {
    "winner": "0"
  }
```

Error Handling: 400 (Required field missing)



