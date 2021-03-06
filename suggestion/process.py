import datetime
import random
import requests
from django.db.models import Max
from suggestion.models import SuggestionEvent


class SuggestionProcess:
    def get_random_event(self):
        max_id = SuggestionEvent.objects.all().aggregate(max_id=Max("id"))['max_id']
        while True:
            pk = random.randint(1, max_id)
            event = SuggestionEvent.objects.filter(pk=pk)
            if event:
                return event

    def get_random_event2(self):
        max_id = SuggestionEvent.objects.all().count()
        rand_id = []
        [rand_id.append(random.randint(0, max_id)) for i in range(2)]
        event = []
        for i in rand_id:
            event.append(SuggestionEvent.objects.all()[i])
        return event

    def get_week_event(self):
        pass

    def get_top3_routine(self, user_id):
        url = f'http://127.0.0.3:8003/api/routine/today_top10/{user_id}'
        response = requests.get(url)
        data = response.json()
        top3 = data[:3]
        return top3

    def process(self, user_id):
        rand_many = self.get_random_event2()
        top3 = self.get_top3_routine(user_id)
        suggestions = []
        for event in rand_many:
            start_day = event.start
            end_day = event.end
            if str(type(event.start)) != "<class 'NoneType'>":
                start_day = event.start.strftime('%Y-%m-%d')
            if str(type(event.end)) != "<class 'NoneType'>":
                end_day = event.end.strftime('%Y-%m-%d')
            else:
                start_day = datetime.date.today()
            suggestions.append({
                "suggestion_id": event.id,
                "user_id": user_id,
                "contents": event.title,
                "location": event.location,
                "routine": None,
                "start": start_day,
                "end": end_day,
                "classification": event.classification,
                "type": "SUGGESTION"
            })
        for routine in top3:
            cron = routine['cron']
            routine_days_char = cron[5].split('.')
            days_to_ko = {'mon': '???', 'tue': '???', 'wed': '???', 'thu': '???', 'fri': '???', 'sat': '???', 'sun': '???'}
            ko_days = [days_to_ko.get(day) for day in routine_days_char]
            days = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}
            routine_days_int = [days.get(day) for day in routine_days_char]
            date = []
            for day in routine_days_int:
                period = 7 - datetime.date.today().weekday() + day
                if period < 7:
                    period = period
                else:
                    period -= 7
                date.append(datetime.date.today() + datetime.timedelta(days=period))
            suggestions.append({
                "suggestion_id": routine['id'],
                "user_id": user_id,
                "contents": routine['contents'],
                "location": routine['location'],
                "routine":ko_days,
                "start": date,
                "end": None,
                "classification": None,
                "type": "ROUTINE",
            })
        return suggestions