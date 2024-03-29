from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
import openai
from openai import OpenAI
import random
import os
# from dotenv import load_dotenv
# load_dotenv()

# openai.api_key = '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'

class AIMove(CreateAPIView):
    def create(self, request, *args, **kwargs):
        try:
            if request.method == 'POST':
                entire_data = request.data
                turn = entire_data.get('turn')
                player = entire_data.get('player')
                current_bet = entire_data.get('current_bet')
                budget = entire_data.get('budget')
                cards = entire_data.get('cards')
                commit = entire_data.get('committed')
                commit_round = entire_data.get('commitRound')
                difficulty = entire_data.get('difficulty')
                best = entire_data.get('best')
                if not player or not budget or not cards or not difficulty or not best:
                    return JsonResponse({'errir': 'Required Field Missing'}, status=400)
                shown = 'none'
                if turn == 0:
                    turn = 'preflop'
                elif turn == 1:
                    turn = 'flop'
                    shown = str(cards['playing'][0:4])
                elif turn == 2:
                    turn = 'turn'
                    shown = str(cards['playing'][0:5])
                elif turn == 3:
                    turn = 'river'
                    shown = str(cards['playing'][0:6])
                client = OpenAI(
                    # defaults to os.environ.get("OPENAI_API_KEY")
                    api_key=os.environ.get("OPENAI_API_KEY"),
                )
                prompt = f'Your cards are {cards[str(player)]}. The turn is {turn} so the cards shown are {shown}. You have a {best}'
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "system", "content": f"You are a poker player with {difficulty} skill level. You will receive some game information and you will make a simple move based on it"},
                            {"role": "user", "content": f"f{prompt}, you have already committed {commit} chips in this round, and you've already committed {commit_round} this turn, and what the current bet is = {current_bet}, and your budget for this move = {budget}, \
                            DO NOT RAISE PAST THIS PLEASE. Also do not call if calling will put your budget into negative. I need you to give me the move/action of player {player} ONLY and no explanation. Here are possible move breakdowns: IF current bet is 0, these are \
                            your move options: 'check', 'raise [amount you'd like to raise]' or fold. IF current bet is 0, do not fold. IF current bet is higher than 0, here are your output options: call, fold, raise [amount you'd like to raise, must be twice the current bet]. \
                            If other player seem to be very passive in this round, please lean towards raising. please dont add anything else such as punctuation, context, just the move and if its a raise, then the number too. If you have a good hand, consider raising. \
                            if you have a bad hand, consider folding. DO NOT FOLD if the current bet is 0 or the current bet is the same as what you've bet this turn"}
                        ]
                    )
                ai_move = response.choices[0].message.content.strip()
                new_bet = 0
                if 'raise' in ai_move.lower():
                    new_bet = float(ai_move.split(' ')[1])
                
                # round_history.conversation = round_history.conversation + move
                # round_history.save()
                return JsonResponse({'move': ai_move, 'bet_increase': new_bet})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # 2grb84sjt0mdpwvzxne9piu4lyey6h1f