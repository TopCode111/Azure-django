from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import viewsets, views
from rest_framework import permissions
from sentry_sdk import capture_exception
import json
from api_backend.apps.dbs import graph
from api_backend.apps.apis.logic import parse_tasks

from .models import KqJsons, KqClone, SessionDetails, GDTemplateTracker
from ..account.serializers import CurrentUserSerializer
from . import serializers as s
from django.conf import settings


class NotebooksViewSet(viewsets.ViewSet):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer

    def create(self, request):
        """
        Put code for "POST: /notebooks" endpoint here.
        """
        path = "static/notebooks/template.ipynb"
        parse_tasks.generate_tasks(path, "00000")

        '''
        path = "static/misc_files/scaffold_extract.json"
        data = None
        excluded_keys = ["relations"]
        try:
            with open(path, "r") as read_file:
                data = json.load(read_file)
        except Exception as e:
            capture_exception(e)
        g = graph.GremlinData()
        #g.attach_content_to_graph(data, excluded_keys)
        '''
        #return_value = g.attach_scaffold_to_graph(data, excluded_keys)
        return_value = ''
        response = {'msg': return_value}
        return Response(response, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        """
        Put code for "GET: /notebooks/<gid>" endpoint here. Note: { id } is { gid }.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """
        Put code for "POST: /notebooks/<nid>" endpoint here. Note: { id } is { nid }
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)


class UserAllNotebooksView(views.APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def get(self, request, sid, format=None):
        """
        Put code for "GET: /notebooks/user/<sid>" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)


class UserNotebookView(views.APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def get(self, request, nid, sid, format=None):
        """
        Put code for "GET: /notebooks/<nid>/users/<sid>" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)


class TasksViewSet(viewsets.ViewSet):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer

    def create(self, request):
        """
        Put code for "POST: /tasks" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        Put code for "GET: /tasks/<nid>" endpoint here. Note: { id } is { nid }
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Put code for "POST: /tasks/<gid>" endpoint here. Note: { id } is { gid }
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        """
        Put code for "PATCH: /tasks/<cid>" endpoint here. Note: { id } is { cid }
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """
        Put code for "DELETE: /tasks/<cid>" endpoint here. Note: { id } is { cid }
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)


class SubmitCheckoutView(views.APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def put(self, request, cid, format=None):
        """
        Put code for "POST: /tasks/rating/<cid>" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)


class UserSignalsView(views.APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        """
        Put code for "POST: /signals" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)


class UserKQAggregatesViewSet(views.APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def get(self, request, type, cid, sid, format=None):
        """
        Put code for "GET: /aggregations/<type>/<cid>/users/<sid>" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)
    
    def post(self, request, type, cid, sid, format=None):
        """
        Put code for "POST: /aggregations/<type>/<cid>/users/<sid>" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)


class UserSubjectDetailViewSet(views.APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request, type, cid, format=None):
        """
        Put code for "GET: /aggregations/<type>/<kid>/users/<sid>" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)
    
    def post(self, request, type, cid, format=None):
        """
        Put code for "POST: /aggregations/<type>/<kid>/users/<sid>" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)


class AllUserKQAggregateViewSet(views.APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    
    def get(self, request, type, cid, format=None):
        """
        Put code for "GET: /aggregations/<type>/<cid>" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)
    
    def post(self, request, type, cid, format=None):
        """
        Put code for "POST: /aggregations/<type>/<cid>" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)    


class PathfindersViewSet(viewsets.ViewSet):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer

    def list(self, request):
        """
        Put code for "GET: /pathfinders" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED) 

    @action(methods=['POST'], detail=False, url_path='relations')
    def relation_check(self, request, *args, **kwargs):
        """
        Put code for "POST: /pathfinders/relations" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED) 

    @action(methods=['POST'], detail=False, url_path='relations/multirelation')
    def create_multi_relation(self, request, *args, **kwargs):
        """
        Put code for "POST: /pathfinders/relations/multirelation" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)


class DownNavigationView(views.APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def get(self, request, kid):
        """
        Put code for "GET: /pathfinders/down/<kid>" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)


class UpNavigationView(views.APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def get(self, request, kid):
        """
        Put code for "GET: /pathfinders/up/<kid>" endpoint here.
        """
        response = {'msg': "Please return your response for this endpoint."}
        return Response(response, status=status.HTTP_201_CREATED)
