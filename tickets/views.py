from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest,Movie,Reserevation
from rest_framework.decorators import api_view
from .serializers import GuestSerializer,MovieSerializer,ReservationSerializer
from rest_framework import status,filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins,viewsets


# Create your views here.
#1
# def no_rest_no_model(request):
    
#2  no_rest-from-model
def no_rest_from_model(request):
    data=Guest.objects.all()
    response={
        'guests':list(data.values('name','mobile'))
    }
    return JsonResponse(response)
    

# list==Get
# Create ==POST
# ph query ==GET
#update =PUT
#Delete ==DELETE

#3 Function based views
#3.1 Get post
@api_view(['GET','POST'])
def FBV_List(requset):
    #Get
    if requset.method=='GET':
        guests=Guest.objects.all()
        serializer=GuestSerializer(guests,many=True)
        return Response(serializer.data)
    #Post
    elif requset.method=='POST':
        serializer=GuestSerializer(data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

#3.2 Get Put Delete
@api_view(['GET','PUT','DELETE'])
def FBV_pk(requset,pk):
    try:
        guest=Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #Get
    if requset.method=='GET':
        serializer=GuestSerializer(guest)
        return Response(serializer.data)
    #Put
    elif requset.method=='PUT':
        serializer=GuestSerializer(guest, data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
    #DELETE
    if requset.method=='DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#CBV Class based views
#4.1 List and Create ==GET and PUT
class CBV_LIST(APIView):
    def get(self,request):
        guests=Guest.objects.all()
        serializer=GuestSerializer(guests,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.data,
            status=status.HTTP_400_BAD_REQUEST
            )    

#4.2 Get Put Delete
class CBV_pk(APIView):
    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist: 
            raise Http404
    def get(self,request,pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest)
        return Response(serializer.data)
    def put(self,request,pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        guest=self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
            
            
#5 Mixins
#5.1 Mixins list
class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)

#5.2 get put delete
class mixins_pk(mixins.DestroyModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    def get(self,request,pk):
        return self.retrieve(request)
    def put(self,request,pk):
        return self.update(request)
    def delete(self,request,pk):
        return self.destroy(request)
    
#6
#6.1 get and post
class generics_list(generics.ListCreateAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer

#6.2 get put delete
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    
#7 viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer

class viewsets_movie(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer
    filter_backends=[filters.SearchFilter]
    search_fields = ['movie']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset=Reserevation.objects.all()
    serializer_class=ReservationSerializer


#8 find movie
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    serializer = MovieSerializer(movies, many= True)
    return Response(serializer.data)
# 9 create new reservation   
@api_view(['POST'])
def new_reservation(request):
    
    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    #add new guest
    guest=Guest()
    guest.name=request.data['name']
    guest.mobile=request.data['mobile']
    guest.save()
    
    reserevation=Reserevation() # take instance from modal
    reserevation.guest= guest
    reserevation.movie= movie
    reserevation.save()
    
    return Response(status=status.HTTP_201_CREATED)
    