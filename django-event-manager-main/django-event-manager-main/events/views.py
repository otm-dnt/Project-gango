from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .models import Event, Participation

def home(request):
    # Rediriger vers la liste des événements
    return redirect('event_list')

def event_list(request):
    events = Event.objects.all()
    context = {
        'events': events,
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user_participation = None
    
    if request.user.is_authenticated:
        user_participation, created = Participation.objects.get_or_create(
            user=request.user,
            event=event
        )
        
        if request.method == 'POST':
            attendance = request.POST.get('attendance')
            if attendance == 'yes':
                user_participation.is_attending = True
            elif attendance == 'no':
                user_participation.is_attending = False
            user_participation.save()
            messages.success(request, "Votre participation a été mise à jour.")
            return HttpResponseRedirect(reverse('event_detail', args=[event_id]))
    
    participants_count = event.participant_count()
    
    context = {
        'event': event,
        'user_participation': user_participation,
        'participants_count': participants_count,
    }
    return render(request, 'events/event_detail.html', context)