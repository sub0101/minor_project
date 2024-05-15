
from django.shortcuts import redirect, render, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.utils.timezone import activate
from .models import User, Message
from django.db.models import Q
import json
from vkeel.profile import *
from vkeel.models import ActiveChat


@login_required(login_url="/login")
def chatroom(request, pk:int):
    count =  len(ActiveChat.objects.filter( Q(chat_user = User.objects.get(id = pk)) & Q(chat_user2  = request.user)))
    if request.user.is_advocate:
            count =  len(ActiveChat.objects.filter( Q(chat_user2 = User.objects.get(id = pk)) & Q(chat_user  = request.user)))

    if count !=0:
        active_chat = ActiveChat.objects.filter(chat_user2 = request.user)
        if request.user.is_advocate:
            active_chat = ActiveChat.objects.filter(chat_user = request.user)
            print(active_chat ,"s")
            

        other_user = get_object_or_404(User, pk=pk)
        messages = Message.objects.filter(
            Q(receiver=request.user, sender=other_user)
        )
        messages.update(seen=True)
        messages = messages | Message.objects.filter(Q(receiver=other_user, sender=request.user) )
        if request.user.is_advocate:
            profile = AdvocateProfile.objects.get(user = request.user)
        else:
            profile = UserProfile.objects.get(user = request.user)

        return render(request, "chatroom.html", {"other_user": other_user, "messages": messages , "use":profile , 'active_chat':active_chat })
    return redirect('/')


@login_required
def ajax_load_messages(request, pk):

    other_user = get_object_or_404(User, pk=pk)
    messages = Message.objects.filter(seen=False).filter(
        Q(receiver=request.user, sender=other_user)
    )
    message_list = [{
        "sender": message.sender.name,
        "message": message.message,
        "sent": message.sender == request.user,
        "date_created":message.date_created
    } for message in messages]
    messages.update(seen=True)
    
    if request.method == "POST":
        
        message = json.loads(request.body)
        m = Message.objects.create(receiver=other_user, sender=request.user, message=message )
        message_list.append({
            "sender": request.user.name,
            "message": m.message,
            "sent": True,
            "date_created": m.date_created
        })
    print(message_list)
    return JsonResponse(message_list, safe=False)




def m(request):
    return render(request , "my.html") 