from django.http import JsonResponse
from rest_framework.generics import ListAPIView
import random
# import os
# from langchain.chains import LLMChain
# from langchain.memory import ConversationBufferMemory
# from langchain.prompts import PromptTemplate
# from langchain_openai import OpenAI
# from dotenv import load_dotenv
# load_dotenv()
class Initialize(ListAPIView):
    def list(self, request, *args, **kwargs):
        # load_dotenv()
        if request.method == 'GET':
            players = request.GET.get('players')
            players = int(players)
            session_id = request.GET.get('session_id')
            values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
            suits = ['heart', 'diamond', 'club', 'spade']
            
            deck = [(value, suit) for suit in suits for value in values]
            
            random.shuffle(deck)

            cards = {}
            for i in range(1, players + 1):
                cards[i] = [deck.pop(0), deck.pop(0)]
            cards['playing'] = deck[players * 2:players * 2 + 5]
            return JsonResponse(cards)
