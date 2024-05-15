from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [

    path( '' , index , name = 'index' ),
    path('advocate/advocate_profile/<int:id>/' , advoprofile , name = 'advoprofile'),
    path('index' , index , name = 'index' ),
    path('contact' , contact , name = 'contact'),
    
    path('about' , about , name = 'about'),
    path('ask_quetion' , quetion_view , name = 'quetions'),
    path('questions' , quetion_view , name = 'quetions' ),
    path('main_signup' , main_signupview , name = "mainsignup"),
    path('main_signup/user_signup' , user_signupview , name = "usersignup"),
    path('main_signup/advocate_signup' , advocate_signupview , name = "advocatesignup"),
    path('login' , login_view , name = "login"),
    path('logout' , logout , name = "logout"),
    path('edit_profile/<int:id>/' , edit_profile , name = "profile"),
    path('delete_education/<int:id>' , delete_education , name = 'delete_education'),
    path('delete_case/<int:id>' , delete_case , name = 'delete_case'),
    path( 'advo_search' , advo_search  , name = 'advo_search'),
    path('personal/<int:id>' , edit_personal_profile_view , name  ="personal"),
    path('questions/answer/<int:id>/' , answer , name = 'answer'),
    path('edit_userprofile/<int:id>/' , edit_userprofile , name = 'userprofile'),
    path('reply/<int:id>' , reply , name ='reply' ),
    # path('simple-checkout/' ,simplecheckout , name = 'simplecheckout' )
    path('handlerequest/' , handlerequest , name = "handlerequest"),
    path('advice/<int:id>/',instantadvice, name='instantadvice'),
    path('follow/<int:id>' , follow_view , name = 'follow'),
    path('unfollow/<int:id>' , unfollow_view , name = 'unfollow'),
    path('chat_users/' , chatview ,name = 'chat' ),
    path('activate-chat/<int:id>' , activate_chat , name= 'activate_chat'),
    path('deactivate-chat/<int:id>' , deactivate_chat , name= 'deactivate_chat'),
    path('search_advo/' , search_advo , name = 'search_advo'),
    path('accounts/', include('allauth.urls')),
  
    
]
