from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from notifications.models import Notification


def chimen_notifications(request):
    context = {}
    return render(request, 'chimen_notifications/chimen_notifications.html', context)

def chimen_notification(request, chimen_notification_pk):
    chimen_notification = get_object_or_404(Notification, pk=chimen_notification_pk)
    chimen_notification.unread = False
    chimen_notification.save()
    return redirect(chimen_notification.data['url'])

def delete_notifications_read(request):
    notifications = request.user.notifications.read()
    notifications.delete()
    return redirect(reverse('chimen_notifications:chimen_notifications'))