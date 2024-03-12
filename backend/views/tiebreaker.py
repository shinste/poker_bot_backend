from django.http import JsonResponse
from rest_framework.generics import CreateAPIView

class TieBreaker(CreateAPIView):
    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            entire_data = request.data
            cards = entire_data.get('cards')
            hand = entire_data.get('hand')
            ties = entire_data.get('ties')


            converting = {'J': 11,
                          'Q': 12,
                          'K': 13,
                          'A': 14}
            def convert(value):
                if value in converting.keys():
                    return converting[value]    
                else: 
                    return int(value)
            high_value = convert(hand.split(' ')[0])
                    
            for key in cards.keys():
                if key != 'playing':
                    cards[key] = [convert(value[0]) for value in cards[key]]
                else:
                    cards['playing'] = [convert(value[0]) for value in cards['playing']]
                    
            
            # Iterating through cards to determine best hand
            if 'Four of a Kind' in hand:
                output = []
                four_value_tracker = {}
                max_kicker = 0
                for tie in ties:
                    values = cards['playing'] + cards[tie]
                    values = set(values)
                    values.remove(high_value)
                    kicker = max(values)
                    max_kicker = max(max_kicker, kicker)
                    four_value_tracker[tie] = kicker
                for tie in ties:
                    if max_kicker == four_value_tracker[tie]:
                        output.append(tie)
                return JsonResponse({'winner': output})
            elif 'Full House' in hand:
                output = []
                four_kicker_tracker = {}
                for tie in ties:
                    values = cards['playing'] + cards[tie]
                    values.remove(high_value)
                    values.remove(high_value)
                    values.remove(high_value)
                    max_kicker_pair = 0
                    for value in values:
                        if values.count(value) > 1:
                            max_kicker_pair = max(max_kicker_pair, value)
                    four_kicker_tracker[tie] = max_kicker_pair
                max_kicker_value = max(four_kicker_tracker.values())
                for tie in ties:
                    if four_kicker_tracker[tie] == max_kicker_value:
                        output.append(tie)
                return JsonResponse({'winner': output})
            elif 'Three of a Kind' in hand:
                output = []
                three_kicker_tracker = {}
                max_kicker_one = 0
                max_kicker_two = 0
                for tie in ties:
                    values = cards['playing'] + cards[tie]
                    values.remove(high_value)
                    values.remove(high_value)
                    values.remove(high_value)
                    kicker = max(values)
                    max_kicker_one = max(max_kicker_one, kicker)
                    values.remove(kicker)
                    max_kicker_two = max(max_kicker_two, max(values))
                    three_kicker_tracker[tie] = [kicker, max(values)]
                for tie in ties:
                    if three_kicker_tracker[tie][0] == max_kicker_one:
                        output.append(tie)
                if len(output) > 1:
                    for player in output:
                        if three_kicker_tracker[player][1] != max_kicker_two:
                            output.remove(player)
                return JsonResponse({'winner': output})
                            
            # Two Pair
            elif 'Two Pair' in hand:
                two_pair_checker = {}
                highest_sum = 0
                best = ''
                same_two_pair_highest = 0
                best_kicker = 0
                for tie in ties:
                    values = cards['playing'] + cards[tie]
                    kicker = 0
                    last = 0
                    tracker = []
                    for value in sorted(values, reverse = True):
                        if value == last:
                            tracker.append(value)
                            if value == kicker:
                                kicker = 0
                        elif value > kicker: 
                            kicker = value
                        last = value
                    indicator = sum(tracker)
                    if indicator > highest_sum:
                        best = tie
                        highest_sum = indicator
                        best_kicker = kicker
                    elif indicator == highest_sum:
                        two_pair_checker[tie] = [indicator, kicker]
                        same_two_pair_highest = max(indicator, same_two_pair_highest)
                        
                # now if i have duplicate two pairs its in my dictionary
                # and to check if the duplicates two pair is the highest value two pair, i check the highest_sum variable
                if highest_sum == same_two_pair_highest:
                    winners = []
                    kickers = {key: two_pair_checker[key][1] for key in two_pair_checker.keys()}
                    kickers[best] = best_kicker
                    highest_kicker = max(kickers.values())
                    for key in kickers.keys():
                        if kickers[key] == highest_kicker:
                            winners.append(key)
                    return JsonResponse({'winner': winners})
                        
                else:
                    return JsonResponse({'winner': [best]})
            # Pair of High Card
            else:
                output = []
                value_tracker = {}
                max_value = 0
                for tie in ties:
                    values = cards['playing'] + cards[tie]
                    values = sorted(values, reverse = True)
                    pair_slice = 5
                    if 'Pair' in hand:
                        values.remove(high_value)
                        values.remove(high_value)
                        pair_slice = 3
                    
                    value_tracker[tie] = sum(values[0:pair_slice])
                    max_value = max(max_value, sum(values[0:pair_slice]))
                
                for key in value_tracker.keys():
                    if value_tracker[key] == max_value:
                        output.append(key)
                return JsonResponse({'winner': output})
                

                    
                