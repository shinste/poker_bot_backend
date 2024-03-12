from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
from openai import OpenAI
import os


class Suggestion(CreateAPIView): 
    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            entire_data = request.data
            turn = entire_data.get('turn')
            hand = entire_data.get('hand')
            community = entire_data.get('community')
            budget = entire_data.get('budget')
            players = entire_data.get('players')
            current_bet = entire_data.get('current_bet')
            committed_turn = entire_data.get('committedTurn')
            committed_round = entire_data.get('committedRound')
            history = entire_data.get('conversationContext')
            best = entire_data.get('best')
            client = OpenAI(
                # defaults to os.environ.get("OPENAI_API_KEY")
                api_key=os.environ.get("OPENAI_API_KEY"),
            )
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": "You are giving me a breakdown on what my next move should be in this poker game, you will receive context."},
                        {"role": "user", "content": f'The turn is {turn}, and my cards are {hand}, while the playing cards are {community}. This means I have a {best}. There are {players} players, and I am player 1. \
                          The current bet is {current_bet}, and I have committed {committed_turn} in this turn alone, I have committed {committed_round} in the entire round. My remaining chips are {budget}. The player betting history \
                          is shown here: {history}, the player numbers that arent 1 are the opponents. Please give me a CONCISE breakdown of what I should do. Briefly mention a couple stronger hands that could beat you and the probabilities of my opponents having them based on their previous actions. provide the conclusive suggested move in capitalized letters please.'}
                    ]
                )
            ai_suggest = response.choices[0].message.content.strip()
            return JsonResponse({'suggest': ai_suggest})