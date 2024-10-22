from django.contrib import admin
from django.urls import path,include
from tickets import views
from rest_framework.routers import DefaultRouter

#viewsets router
router=DefaultRouter()
router.register('guests',views.viewsets_guest)
router.register('movies',views.viewsets_movie)
router.register('reservations',views.viewsets_reservation)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    #1
    # path('django/jsonresponsenomodel/',views.no_rest_no_model),
    #2
    path('django/jsonresponsefrommodel/',views.no_rest_from_model),
    
    #3
    path('rest/fbvlist/',views.FBV_List),
    
    path('rest/fbvpk/<int:pk>',views.FBV_pk),
    #4
    path('rest/cbv/',views.CBV_LIST.as_view()),
    
    path('rest/cbvpk/<int:pk>',views.CBV_pk.as_view()),
    
    #5
    path('rest/mixinslist/',views.mixins_list.as_view()),
    
    path('rest/mixinspk/<int:pk>',views.mixins_pk.as_view()),
    
    #6
    path('rest/genericslist/',views.generics_list.as_view()),
    
    path('rest/genericspk/<int:pk>',views.generics_pk.as_view()),
    
    #7
    path('rest/viewsets/',include(router.urls)),
        
    #8
    path('fbv/findmovie',views.find_movie),
    
    #9
    path('fbv/newreserv',views.new_reservation)
    
]

