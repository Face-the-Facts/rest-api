from django.shortcuts import render
from django.core.exceptions import *
from .models import Politician, Vote, Poll, PollResult
from .serializers import PoliticianSerializer, VoteSerializer, PollSerializer, ResultSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import requests
from django.conf import settings

class PoliticianViewSet(viewsets.ModelViewSet):
    queryset = Politician.objects.all()
    serializer_class = PoliticianSerializer

    @action(methods=['get'], detail=True, url_path='votes', url_name='votes')
    def votes(self, request, pk):
        votes = Vote.objects.filter(politician=pk)
        vote_list = [vote for vote in votes.values()]
        print(vote_list)
        serializer = VoteSerializer(data=vote_list, many=True, context={'politician': pk})
        print(votes.values_list())
        print(serializer.is_valid())
        if serializer.is_valid():
            return Response(vote_list, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        print(request.data)
        pass

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    """ def get_queryset(self):
        return Vote.objects.filter(politician=self.request.politician) """


class ResultDoesNotExist(Exception):
    pass

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get_result(self, abgeordnetenwatch_id):
        r = requests.get(f'https://www.abgeordnetenwatch.de/api/v2/votes?poll={abgeordnetenwatch_id}&range_end=999')
        votes = r.json()['data']

        result = {
            'yes': 0,
            'no': 0,
            'abstain': 0,
            'no_show': 0
        }

        for vote in votes:
            result[vote['vote']] += 1
        
        return result

    def list(self, request):

        # Page number and size for forwarding pagination to Abgeordnetenwatch API
        page_num = request.query_params.get('page')
        if page_num == None:
            page_num = 1
        page_size = request.query_params.get('page_size')
        if page_size == None:
            page_size = settings.REST_FRAMEWORK['PAGE_SIZE']

        r = requests.get(f'https://www.abgeordnetenwatch.de/api/v2/polls?page={page_num}&pager_limit={page_size}')
        response = r.json()['data']
        poll_ids = []
        for poll in response:
            poll_ids.append(poll['id'])
            try:

                saved_poll = Poll.objects.get(abgeordnetenwatch_id=poll['id'])

                if saved_poll.result == None:
                    raise ResultDoesNotExist
                
                print(f"Poll {saved_poll} found")
                serializer = PollSerializer(saved_poll, context={'request': request})


            except ObjectDoesNotExist:
                print("Poll not found, creating...")
                
                result = self.get_result(poll['id'])

                new_poll = {
                'title': poll['label'],
                'abstract': poll['field_intro'],
                'topics': poll['field_topics'],
                'yes': result['yes'],
                'no': result['no'],
                'abstain': result['abstain'],
                'no_show': result['no_show'],
                'result': max(result, key=result.get),
                'abgeordnetenwatch_id': poll['id'],
                'abgeordnetenwatch_url': poll['api_url'],                    
                }

                serializer = PollSerializer(data=new_poll, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    print('\nSerialized data single poll:')
                    print(serializer.data)
                else:
                    print('\nSerializer errors:')
                    print(serializer.errors)
                
            except ResultDoesNotExist:
                print('Result does not exist')
                pass
            

        queryset = Poll.objects.filter(abgeordnetenwatch_id__in=poll_ids)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PollSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
            

        