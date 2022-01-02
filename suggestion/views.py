import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from event.process import EventProcess
from satisfaction.process import SatisfactionProcess
from suggestion.models import SuggestionEvent
from suggestion.process import SuggestionProcess
from suggestion.serializer import SuggsetionSerializer as Serializer

# def index(request):
#     ic(request.session.session_key)
#     try:
#         ic(request.session['user'])
#     except KeyError:
#         print('키 에러1')
#     request.session['user'] = 1
#     ic('-'*100)
#     try:
#         ic(request.session['user'])
#     except KeyError:
#         print('키 에러2')
#     request.session['test'] = "hahaha"
#     ic(request.session['test'])
#     return render(request, 'index.html')



@api_view(['GET', 'POST'])
def suggestion_all(request):
    if request.method == 'GET':
        all_event = SuggestionEvent.objects.all()
        serializer = Serializer(all_event, many=True)
        return Response(data=serializer.data)

    elif request.method == 'POST':
        serializer = Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': f'"{serializer.data.get("title")}" 입력 완료'}, status=201)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def suggestion_by_id(request, id):
    try:
        event = SuggestionEvent.objects.get(pk=id)
    except SuggestionEvent.DoesNotExist:
        return Response({'message': 'Event_DoesNotExis'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Serializer(event)
        return Response({'result': serializer.data}, status=201)

    elif request.method == 'PUT':
        serializer = Serializer(instance=event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': f'<ID_{serializer.data.get("id")}: {serializer.data.get("title")}> 수정완료'}, status=201)

    elif request.method == 'DELETE':
        event.delete()
        return Response({'result': '삭제 성공'}, status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def suggestion_user(request, user_id):
    return Response(data=SuggestionProcess().process(user_id), status=201)


@api_view(['GET'])
def suggestion_user_test(request, user_id):
    return Response(data=SuggestionProcess().process_test(user_id), status=201)


@api_view(['POST'])
def suggestion_accept(request):
    request_data = request.data
    event_process = EventProcess()
    SatisfactionProcess().suggestion(request_data, "Accept")
    if request_data['type'] == "SUGGESTION":
        suggestion = event_process.suggestion_event(request_data)
        suggestion
        return Response(suggestion, status=201)
    if request_data['type'] == "ROUTINE":
        routine = event_process.routine_event(request_data)
        routine
        return Response(routine, status=201)

    return Response({'message': 'Event_DoesNotExis'}, status=status.HTTP_404_NOT_FOUND)
    # return Response({'result':f'{request_data[]}'}, status=201)


@api_view(['POST'])
def suggestion_reject(request):
    SatisfactionProcess().suggestion(request.data, "Reject")
    url = f'http://서버:8000/api/routine/reject/{request.data["suggestion_id"]}'
    requests.get(url)
    return Response({'result':f'<{request.data["contents"]}> 거절'}, status=201)
