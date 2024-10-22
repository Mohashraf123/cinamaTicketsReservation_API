from django.db import models

#guset--Movie-reservation
class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=10)
    #date = models.DateField()
    
class Guest(models.Model):
    name=models.CharField(max_length=30)
    mobile=models.CharField(max_length=11)
    

class Reserevation(models.Model):
    guest=models.ForeignKey(Guest,related_name='reservation',on_delete=models.CASCADE) 
    movie=models.ForeignKey(Movie,related_name='reservation',on_delete=models.CASCADE)   
     

