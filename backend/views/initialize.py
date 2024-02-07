from django.http import JsonResponse
from rest_framework.generics import ListAPIView
import openai
import random

openai.api_key = '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'

class Initialize(ListAPIView):
    def list(self, request, *args, **kwargs):
        players = int(request.GET.get('players'))
        button = request.GET.get('button')
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['heart', 'diamond', 'club', 'spade']
        
        deck = [(value, suit) for suit in suits for value in values]
        
        random.shuffle(deck)

        cards = {}
        for i in range(players):
            cards[i] = [deck.pop(0), deck.pop(0)]
            
        cards['playing'] = deck[players * 2:players * 2 + 5]
        return JsonResponse(cards)
        
        
            
        
    
    
    # def list(self, request, *args, **kwargs):
    #     players = request.GET.get('players')
    #     buy_in = request.GET.get('buy_in')
    #     ante = request.GET.get('ante')
    #     difficulty = request.GET.get('difficulty')
        
    #     completion = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": "You are a dealer at a poker table, the game has started with 3 people and the user. The order of the players is User, then player 1, then player 2, then player 3, then back to the user. player 2 is under the gun"},
    #             {"role": "user", "content": "please play the roles of the other players while giving them actual cards from a deck before the flop and say what the players would optimally do with their cards and provide the user with cards, say what the other players play until its the user's turn, just simple actions that have happened, don't reveal the other players' cards, ONLY the user's cards or say any unnecessary roleplay"}
    #         ]
    #     )
    #     return JsonResponse({'message': completion.choices[0].message})
