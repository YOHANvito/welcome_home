from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import ChatRoom, Message


@login_required
def chat_inbox(request):
    rooms = ChatRoom.objects.filter(participants=request.user).distinct().order_by('name')
    return render(request, 'chatapp/inbox.html', {'rooms': rooms})


@login_required
def create_demo_room(request):
    room, created = ChatRoom.objects.get_or_create(name="General Chat")
    room.participants.add(request.user)
    return redirect('chat_room', room.id)


@login_required
def create_room(request):
    room, created = ChatRoom.objects.get_or_create(name="General Room")
    room.participants.add(request.user)
    return redirect('chat_room', room.id)


@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)

    if request.user not in room.participants.all():
        room.participants.add(request.user)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                room=room,
                sender=request.user,
                content=content
            )
        return redirect('chat_room', room_id=room.id)

    return render(request, 'chatapp/room.html', {
        'room': room,
        'messages': room.messages.all()
    })