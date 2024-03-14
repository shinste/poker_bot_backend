from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
from openai import OpenAI
import os

class Feedback(CreateAPIView): 
    def create(self, request, *args, **kwargs):
        try:
            if request.method == 'POST':
                entire_data = request.data
                cards = entire_data.get('cards')
                history = entire_data.get('history')
                client = OpenAI(
                    api_key=os.environ.get("OPENAI_API_KEY"),
                )
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "system", "content": "I am playing poker and you are analyzing how my last round went, and what I get better at"},
                            {"role": "user", "content": f'This is my game history: {history}. These are the cards that were used: {cards}. Im player 1 \
                            and the playing cards are in the key "playing". In a maximum of 3 sentences, rate how well I played, a couple of blunders I \
                            had if I had any, and what I should improve on.'}
                        ]
                    )
                ai_feedback = response.choices[0].message.content.strip()
                return JsonResponse({'feedback': ai_feedback})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500) 