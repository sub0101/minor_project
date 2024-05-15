
from datetime import datetime
import json
from os import error
from django.db.models import Q
from django.contrib import messages
from django.core.checks.messages import Error
from django.db.models import query
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse, HttpResponseRedirect , JsonResponse
from .forms import *
from django.utils.timezone import now
from django.core import serializers
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .PayTm import Checksum
import random
from django.core.mail import send_mail
from .pythonData import cities , laws
from collections import OrderedDict
from operator import getitem 
orderid   = 2701
sender = None
reciever = None

obj= None
courts = ['Madras High Court' ,'High Court of Delhi' , 'HIGH COURT OF BOMBAY']
sorted_advocates = []


# def send_email(subject , message , email):
#     send_mail(subject,message , 'AdvoLegal',[str(email)])
    
def index(request):
    
    advocate = User.objects.filter(is_advocate = True)
    return_value = sort_advocate(advocate , request.user)
    detail = return_value[0]
    advocate = return_value[1]
    advo  = list()
    
    for i  in range(0,4):
        if len(advocate)>i:

            advo.append( advocate[i])
    


    return render(request, 'index.html' , {'advocate':advocate , 'detail':detail})



def login_view(request):

    if request.method == 'POST':

        email = request.POST.get('email')

        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            if user.is_active:
                django_login(request, user)
                messages.success(request, 'you have successfully Login')
                return HttpResponseRedirect('/index')
            else:
                print('failed login')
        else:
            messages.warning(request, 'Wrong Email and Password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def edit_profile_removeCopy(user , value , type):
    bool = True
    if type == 'law':

        for i in user.profile.area_of_law:
   
            if i == value  :
                bool = False


    if type == 'courts':

        for i in user.profile.visiting_courts:
   
            if i == value and value!='all' :
                bool = False
   

    if type == 'city':

        for i in user.profile.service_cities:
   
       
            if i == value and value!='all' :
                bool = False


    return bool

def delete_advo_data( user , data , type):
  
    if type == 'area_of_law':
        user.area_of_law.remove(data)
    if type == 'visiting_courts':
        user.visiting_courts.remove(data)
    if type == 'service_cities':
        user.service_cities.remove(data)
    pass
        

def edit_profile(request, id):


    context = {}

    user = User.objects.get(id = request.user.id)
    profile_model = AdvocateProfile.objects.get(user = user)
    case_model = CaseProfile.objects.filter(user = user)
    education_detail = EducationModel.objects.filter(user=user)
    form2 = ProfileForm(request.POST or None,  instance=profile_model)
    form3 = CaseForm()
    form4 = EducationForm()
   
    
    if request.method == 'POST' :
      
        form2 = ProfileForm(request.POST or None,  instance=profile_model)

        print(form2.is_valid())
        # print(form2.errors)
        print(request.POST.get('value'))
        if request.POST.get('delete')!=None:
            print('aaa')
            value = request.POST.get('delete').split(',')
            delete_advo_data( profile_model , value[0] ,value[1])
        form3 = CaseForm(request.POST)
        form4 = EducationForm(request.POST)
        
        if form3.is_valid():
            print('sd')
            form3.save(commit=False).user = request.user
            form3.save()

        if form4.is_valid():
            print('s')
            form4.save(commit=False).user = request.user
            form4.save()

        if form2.is_valid() :  
            ajax_value = ""
            
            if request.POST.get('check') == None:

                form2.save()
            elif request.POST.get('check') !=None:

                if request.POST.get('check') =='add_courts':
                    print('court')

                    ajax_value =  request.POST.get('value')
                   
                    value = edit_profile_removeCopy(request.user , ajax_value , 'courts')
                    if value:
                        profile_model.visiting_courts.append(ajax_value)
                    form2.save(commit=False).user = request.user
                    form2.save()
                    response={'msg':ajax_value}
      
                    return JsonResponse(response)

                if request.POST.get('check')  == 'add_law':
                    print('law')

                    ajax_value =  request.POST.get('value')

                 
                    value = edit_profile_removeCopy(request.user , ajax_value , 'law')
                    
                    if value:
                        profile_model.area_of_law.append(ajax_value)

                    # form2.save(commit=False).user = request.user
                    form2.save()
                    response={'msg':ajax_value}
      
                    return JsonResponse(response)
               
                if request.POST.get('check')  == 'add_cities':
                    print('cities')
                    ajax_value =  request.POST.get('value')
                    value = edit_profile_removeCopy(request.user , ajax_value , 'city')
                    if value:
                        profile_model.service_cities.append(ajax_value)
                    
                    # form2.save(commit=False).user = request.user
                    form2.save()
                    
                    response={'msg':ajax_value}
      
                    return JsonResponse(response)
           
               
        return redirect('/edit_profile/{}'.format(request.user.id))
   
    context = { 'form2': form2, 'form3': form3,
               'form4': form4, 'education_detail': education_detail  , 'case':case_model , 'laws':laws , 'courts':courts , 'city':cities}

    return render(request, "profiles/professional.html", context)


def delete_education(request , id):
    
    instance = EducationModel.objects.get(id = id)
    temp = instance.user.id
    instance.delete()
    return redirect('/edit_profile/{}'.format(temp))
    return render(request, "profiles/professional.html",)

def delete_case(request , id):
    
    instance = CaseProfile.objects.get(id = id)
    temp = instance.user.id
    instance.delete()
    return redirect('/edit_profile/{}'.format(temp))
 

@login_required
def edit_personal_profile_view(request, id):

    context = {}

    profile_model = get_object_or_404(AdvocateProfile, user = request.user)
   
    user_model = User.objects.get(email = request.user)
    
    form1 = edit_user_form(data = request.POST  or None, instance=user_model)
    form2 = ProfileForm(request.POST or  None, instance=profile_model)
    if request.method == 'POST':
        form1 = edit_user_form(data = request.POST, files = request.FILES  or None, instance=user_model)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('/personal/{}'.format(request.user.id))

    context = {'form1': form1, 'form2': form2}
               
    return render(request, "profiles/personal.html", context)


def advocate_signupview(request):

    form = AdvocateSignupForm(request.POST)
  
    subject = 'Welcome To Advolegal'
    user = None
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)

            user.is_advocate = True
            user.save()
            message = 'Hii {}.!  Welcome TO Advolegal  , Your Account Successfully Created. For Any Query Contact Us'.format(user.name)
          

            # send_mail(subject,message , 'jick2701@gmail.com',[user.email])
            # send_email(subject , message ,user.email)
            return HttpResponseRedirect('/index')
        else:
            return render(request, 'advocate_signup.html', {'form': form, 'user': user})
    else:
        form = AdvocateSignupForm()
    return render(request, 'advocate_signup.html', {'form': form, 'user': user})

def user_signupview(request):
    return render(request , 'user_signup.html')

def main_signupview(request):
    return render(request , 'main_signup.html')

@login_required
def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/index')




def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        query = request.POST.get('query')
        user = ContactUs(name = name , email  = email , mobile = mobile , query = query , date = datetime.now())
        user.save()
        messages.success(request, 'Your Query succesfully Submitted. Thanks for your Query')
        subject = 'We HAve Recieved Your message'
        # message = 'ddddd'
        message = 'We Have Recieved Your message and would like thank you for writing to us if your query is urgent please use telephone number listed below to talk to one of our staff member , other wise we will reply by email as soon as possible\n Contact Number: 8448862887 \n Email:advolegal0@gmail.com' 
      
        # send_email(subject ,message , email )
        return redirect('/contact')
    return render(request, 'contact2.html')



def user_signupview(request):

    form = UserSignupForm(request.POST)
    subject = 'Welcome To Advolegal'

    user = None
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.is_user = True
            user.save()
            message = 'Hii {}.!  Welcome TO Advolegal  , Your Account Successfully Created. For Any Query Contact Us'.format(user.name)
          

            # send_email(subject,message ,user.email)
            return HttpResponseRedirect('/index')
        else:
            return render(request, 'user_signup.html', {'form': form, 'user': user})
    else:
        form = UserSignupForm()
    return render(request, 'user_signup.html', {'form': form, 'user': user})

@login_required
def edit_userprofile(request , id):

    user = get_object_or_404(User , id =request.user.id)

    profile = get_object_or_404(UserProfile, user = user)
  
    userform = edit_user_form(data=request.POST , files=request.FILES or None, instance = user)
    profile_form = UserProfileform(data=request.POST , files=request.FILES , instance = profile)
    if request.method == 'POST':
        if profile_form.is_valid() and userform.is_valid():
            
            profile_form.save()         
        
            userform.save()
            return redirect('/edit_userprofile/{}'.format(profile.id))
    else:    
        userform = edit_user_form(request.POST   or  None, instance = user)
        profile_form = UserProfileform(request.POST or None , instance = profile)
    return render(request , 'profiles/user_profile.html' , {'form2':profile_form , 'form1':userform})



def quetion_view(request):

    questions = Question.objects.all()
    questions = reversed(questions)
   
    if request.method == 'POST':

       
        if request.POST.get('filter') is not None:
        
            questions = Question.objects.filter(area_of_law = request.POST.get('filter'))
            questions = reversed(questions)
         
            if request.POST.get('filter') == "all":
                questions = Question.objects.all()
                questions = reversed(questions)
        
         
            return render(request , 'quetions.html' ,{'questions':questions , 'filter_law':laws })

        else:    
       
            title = request.POST.get('title')
            description = request.POST.get('description')
            area_of_law = request.POST.get('area_of_law')
            question = Question(user =  request.user, title = title, question_description  =description , area_of_law = area_of_law ,  date_posted = datetime.now())
            question.save()
            questions = Question.objects.all()
            questions = reversed(questions)

            return redirect('/questions' , {'questions':questions , 'filter_law':laws})
   
   

      
    return render(request , 'quetions.html' ,{'questions':questions,'filter_law':laws })


def answer(request , id):
  
    question = Question.objects.get(id=id)
    answer = Answer.objects.filter(question = question) 
    answer  = reversed(answer)

    return render(request , 'answer.html' ,{'question':question , 'answer':answer})


def reply(request , id):

    if request.method == 'POST':

        question = Question.objects.get(id = id)    
        ask_quetion_user  = question.user
        rep = request.POST.get('reply')
       
        answer = Answer(user = request.user , question = question , reply = rep )
        answer.save()
        subject = 'Reply On Your Quetion'
        message = 'Hii , {name} , {user} Reply On your Quetions \n CHeck The reply \n http://127.0.0.1:8000/answer/{id}'.format( user =request.user.name ,   name = ask_quetion_user.name , id = id)
        # send_email(subject , message  ,ask_quetion_user.email)
        return redirect('/questions/answer/{}'.format(id))
    return render(request , 'quetions.html')


# advocate profile and search
def check(experience , rate , answer , following , user):

    rating_user =""
    ans = 0
    follower = 0
    bool=True
    # rate = Rating.objects.filter(user = user)
    average_rate = 0
    # experience = ""
    follower = Follower.objects.filter(following  = following).count
    # print(follower)
    is_follow = 0
    try:
        if user is not None:
      
            is_follow = Follower.objects.filter(following = following , follower = user).count
    except:
        is_follow=0
    finally:
        for i in rate:
 
            average_rate = average_rate + i.rate

        x = datetime.now()
    
        if experience !="":
            date_time_str = str(experience + ' 08:15:27.243860')
            practicing_since = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
            practicing_since=  str(practicing_since.year)
            x= str(x.year)
            x =int(x)
            practicing_since = int(practicing_since)
            experience = x-practicing_since
        else:
            experience=0
        if len(rate)!=0:
            average_rate = average_rate/ len(rate)
        else:
            average_rate = 0
    

        value = {'experience':experience , 'rate':average_rate , 'answer': len(answer) , 'follower':follower , 'is_follow':is_follow }

        return value

def advoprofile(request , id):
    

    if request.method == 'POST':
        rating_user =""
        obj=None
        bool=True
        print('ighhfhfhgft5')
        try:
            user = User.objects.get(id = id)
            print(user.name)
            rating_user = Rating.objects.get(reviewer = request.user.email , user = user)
            bool = True
    
        except:
            
            bool= False
   
        if bool:
            print('ia')
            print(rating_user)
            print(int(request.POST.get('temp')))
            print( request.POST.get('post_review'))
            rating_user.post = request.POST.get('post_review')
            rating_user.rate = int(request.POST.get('temp'))
            rating_user.save()
        else:
            print('i')
            user = User.objects.get(id = id)
            val = request.POST.get('temp')

            obj = Rating(user =  user , reviewer = request.user.email, post = 'sdfsdfsdfsd' , rate = val)
           
            obj = obj.save()
        

    
    print('hh')
    is_active = ""
    user = User.objects.get(id = id)
    profile= AdvocateProfile.objects.get(user = user)
    education_profile = EducationModel.objects.filter(user = user)
  
    service_cities = profile.service_cities
    area_of_law = profile.area_of_law
    visiting_courts = profile.visiting_courts
   
  
    
    value = check(profile.practicing_since,  Rating.objects.filter(user = user) , Answer.objects.filter(user  = user) , get_object_or_404(User,email = user.email) , request.user)
    try:
        if request.user.is_user:
            is_active =  len(ActiveChat.objects.filter( Q(chat_user2 = request.user) & Q(chat_user  = user)))
        else:
            is_active =  len(ActiveChat.objects.filter( Q(chat_user2 = user) & Q(chat_user  = request.user)))
    except :
        return redirect('index')


    return render(request , 'advocateprofile.html' ,{'rate':value['rate'] ,'experience':value['experience'], 'advocate':user , 'answer':value['answer'],
              'city' :service_cities , 'law':area_of_law , 'courts':visiting_courts ,'education':education_profile , 'followers':value['follower'] , 'is_follow':value['is_follow'] , 'is_active':is_active})

def search_city(users , city):
    users = AdvocateProfile.objects.all()
    city_list = []
    for i in users:
       for j in i.service_cities:

           if j == city:
               city_list.append(i.user)

    return city_list

def sortLaw(users , law):
    users = AdvocateProfile.objects.all()
    
    law_list = []
    for i in users:
       
        for j in i.area_of_law:
            
            if j == law:
                law_list.append(i.user)
    
    return law_list
def search_advo( request ):
    if request.method == 'POST':
        print('inside')
        name_list  = list(User.objects.filter(is_advocate = True).values('name'))
        return  JsonResponse(name_list , safe= False)

            
def search_name(user,name):

    name_list = []
    for i in user:
        if i.name == name:
            name_list.append(i)
    return  name_list

            
        
def sortGender(users , gender):
    
    gender_list = []
    users = AdvocateProfile.objects.all()
    
    for i in range(0,len(users)):
      if users[i].gender == gender:
        
          gender_list.append(users[i].user)

    return gender_list

    
def sort_advocate(advocate , user):
    rate ={}
    
    for i in range(0 , len(advocate)):
        view = check(advocate[i].profile.practicing_since , Rating.objects.filter(user =advocate[i]) , Answer.objects.filter(user = advocate[i]) , get_object_or_404(User , email = advocate[i]) , user)
       
        rate[advocate[i].email] = view 
       

    rate = OrderedDict(sorted(rate.items(), 
       key = lambda x: getitem(x[1], 'experience'))) 
  
    rate = OrderedDict(reversed(list(rate.items()))) 
    new_list = []
 
    for i in rate:
        new_list.append(User.objects.get(email = i))
 
    advocate = new_list
    
    
    return [rate , advocate]

def advo_search(request):
    print('a')
    advice = AdviceForm()
    advocate = User.objects.filter(is_advocate = True)
    user = User.objects.filter(is_advocate = True )
    rate={}
    # profile  = AdvocateProfile.objects.get(user  = advocate[0])
   
    if request.method == 'POST':
        gender = request.POST.get('gender')
        city = request.POST.get('city')
     
        law = request.POST.get('filter_law')
        name = request.POST.get('myCountry')
       
        if gender !=None:
           print('gender')
           gender_list =  sortGender(User.objects.all() , gender )
           advocate = gender_list
    
        elif city != None and law =='all' :
            print('city')
            print(request.POST.get('city')
)
            city_list = search_city(User.objects.all() , city)
            advocate = city_list
       
        elif law != 'all' and name == None : 
            print('law')
            law_list = sortLaw(User.objects.all() , law)
            advocate = law_list
            
        elif name != 'None' or law == 'all':
            print('search')
            name_list = search_name(User.objects.filter(is_advocate = True) , name)
            advocate = name_list
        
    
   
    return_value =  sort_advocate(advocate , request.user)
    advocate = return_value[1]
    rate = return_value[0]
    
   
    return render(request , 'advo_search.html' , {'advocate':advocate ,'advice_form':advice ,'detail':rate , 'filter_law':laws,'cities':cities })
   
# -----------------------------------
@login_required

def instantadvice(request , id):
    advice = AdviceForm()
    user = User.objects.get(id = id )
    global orderid
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        global obj
        obj = InstantAdvice(user = User.objects.get(email = email) , name= name, advocate = user.email , created = datetime.now() , mobile = mobile , ammount=399)
      

        param_dict = { 'MID':'HCmKti75698412597568',
            'ORDER_ID': str(obj.transaction_id),
            
            'TXN_AMOUNT':'399',
            'CUST_ID':str(request.user.id),
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/', }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict ,'V38%h#PI3JNLXKGR')
        global sender
        sender = obj
        global reciever
        reciever = user
        return render(request , 'payment.html', {'param_dict':param_dict})
    return render(request, 'advice.html' , {'advice':advice})
    
@csrf_exempt

def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i== 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict ,'V38%h#PI3JNLXKGR' , checksum)

    if verify:
        if response_dict['RESPCODE'] == '01':
            print('transaction successfully')
            global sender
            global reciever
            global obj
            obj.save()
            subject = 'Your Transaction Has been done '
            message= 'Hello {name} your query has been successfully submited . Advocate contact you as soon as possible if there is no call from advocate And if You feel any Wrong then please Contact Us We Will Do Our Best. Thank You \n Your Transaction Id: {transaction}'.format(name = sender.name , transaction = obj.transaction_id)
            # send_mail(subject,message ,'advolegal0@gmail.com', [sender.user.email])
            message = 'Hello Mr./Ms . {name} New User Want to  Contact You Please Call him as soon as possible user is waiting for you. We will send money to your account shortly. Thank You'.format(name = reciever.email  )
            detail = '\n Name: {name} ,\n  email: {email} ,\n  contact : {contact}'.format(name = sender.name , email = sender.advocate , contact = sender.mobile)
            message = message + " "+ detail
            subject='ADvolegal New User Connection'
            
            # send_mail( subject, message ,'advolegal0@gmail.com', [sender.advocate])
            verify = 'false'
        else:
            print('failed')
        return render(request , 'paymentstatus.html' , {'response':response_dict})
    

    return HttpResponse("done")



def follow_view(request , id):
    follower = get_object_or_404(User ,id = request.user.id)
    following  = get_object_or_404(User , id = id)
    print(str(follower)+ str(following))
    obj= {}
    try:
     obj =   Follower.objects.get( follower = follower , following = following) 
    except :
         
        Follower.objects.create(follower  = follower , following = following)
       
        return redirect('/advo_search')
    
    return redirect('/advo_search')


def unfollow_view(request , id):
    Follower.objects.filter(following = get_object_or_404(User , id = id ), follower = request.user).delete()
    return redirect('/advo_search')

    

def chatview(request):
    if request.user.is_user:
        users = ActiveChat.objects.filter(chat_user2 = request.user)
    else:
        users = ActiveChat.objects.filter(chat_user = request.user)

   
    return render(request , 'chat.html' , {'users':users})

def activate_chat(request , id):
    if request.method == 'POST':
        if request.user.is_advocate:
            count =  len(ActiveChat.objects.filter( Q(chat_user2 = User.objects.get(id = id)) & Q(chat_user  = request.user)))
        else:
            count =  len(ActiveChat.objects.filter( Q(chat_user = User.objects.get(id = id)) & Q(chat_user2  = request.user)))
        if count==0:
            ActiveChat.objects.create(chat_user = User.objects.get(id = id) , chat_user2 = request.user)
    return redirect('/chat_users')



def deactivate_chat(request , id):
    if request.method == "POST":
        if request.user.is_advocate:
            count =  len(ActiveChat.objects.filter( Q(chat_user2 = User.objects.get(id = id)) & Q(chat_user  = request.user)))
        else:
            count =  len(ActiveChat.objects.filter( Q(chat_user = User.objects.get(id = id)) & Q(chat_user2  = request.user)))
        if count!=0:
            ActiveChat.objects.filter(Q(chat_user = User.objects.get(id = id)) & Q(chat_user2  = request.user)).delete()
            ActiveChat.objects.filter(Q(chat_user2 = User.objects.get(id = id)) & Q(chat_user  = request.user)).delete()

    return redirect('/advocate/advocate_profile/{}'.format(User.objects.get(id = id).id))



def getadvodata(request , id):
    
    advocates = User.objects.filter(advocate = True)
    return render(request , 'advo_search.html' , {'advocates':advocates})