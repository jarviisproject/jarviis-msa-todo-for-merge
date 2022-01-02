from event.serializer import EventSerializer


class EventProcess(object):
    def routine_event(self, request_data):
        events = []
        routine_date = []
        [routine_date.append(f'{date} 00:00') for date in request_data['start']]
        for date in routine_date:
            event_data = {}
            event_data['user_id'] = request_data['user_id']
            event_data['title'] = request_data['contents']
            event_data['classification'] = request_data['classification']
            event_data['type'] = request_data['type']
            event_data['location'] = request_data['location']
            event_data['start'] = date
            event_data['end'] = date
            events.append(event_data)
        serializer = EventSerializer(data=events, many=True)
        if serializer.is_valid():
            serializer.save()
        return serializer.data

    def suggestion_event(self, request_data):
        event_data = {}
        event_data['user_id'] = request_data['user_id']
        event_data['title'] = request_data['contents']
        event_data['classification'] = request_data['classification']
        event_data['type'] = request_data['type']
        event_data['location'] = request_data['location']
        event_data['start'] = f'{request_data["start"]} 00:00'
        event_data['end'] = request_data['end']
        serializer = EventSerializer(data=event_data)
        if serializer.is_valid():
            serializer.save()
        return serializer.data


