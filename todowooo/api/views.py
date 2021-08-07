from datetime import timezone
from django.contrib.auth.models import Permission
from rest_framework import generics,permissions
from .serializers import TodoSerializer, TodoSerializerCompleted
from todo.models import Todo
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api import serializers
from rest_framework.authtoken.models import Token





@csrf_exempt
def signup(request):

        if request.method == 'POST':
                try:
                    data=JSONParser().parse(request)
                    user = User.objects.create_user(data['username'], password=data['password1'])
                    user.save()
                    token=Token.objects.create(user=user)
                    return JsonResponse({'token':str(token)},status=201)
                     
                except IntegrityError:
                    return JsonResponse({'error':'That username has already been taken. Please choose a new username'},status=400)


@csrf_exempt
def login(request):

        if request.method == 'POST':
                
            data=JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password1'])
            if user is None:
                return JsonResponse({'error':'could not login.please check username and password'})
            else:
                try:
                    token=Token.objects.get(user=user)
                except: 
                     token=Token.objects.create(user=user)   

                return JsonResponse({'token':str(token)},status=200)     
                                    
                                 

class TodoCompletedList(generics.ListAPIView):

    serializer_class=TodoSerializer
    permission_classes=[permissions.IsAuthenticated]


    def get_queryset(self):
        user=self.request.user
        return Todo.objects.filter(user=user,datecompleted__isnull=False).order_by('-datecompleted')




class TodoListCreate(generics.ListCreateAPIView):

    serializer_class=TodoSerializer
    permission_classes=[permissions.IsAuthenticated]


    def get_queryset(self):
        user=self.request.user
        return Todo.objects.filter(user=user,datecompleted__isnull=True)     

    def perform_create(self, serializer):
       serializer.save(user=self.request.user)



class TodoRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):

    serializer_class=TodoSerializer
    permission_classes=[permissions.IsAuthenticated]


    def get_queryset(self):
        user=self.request.user
        return Todo.objects.filter(user=user)



class TodoComplete(generics.UpdateAPIView):

    serializer_class=TodoSerializerCompleted
    permission_classes=[permissions.IsAuthenticated]


    def get_queryset(self):
        user=self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.datecompleted=timezone.now()
        serializer.save()
            



