from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse

from .models import Comment
from .forms import CommentForm


def comment_update(request):
    #referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}

    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            if not parent.root is None:
                comment.root = parent.root
            else:
                comment.root = parent
            comment.parent = parent
            comment.recipient = parent.user
        comment.save()
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_displayname()
        data['time'] = comment.time.timestamp()
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        data['pk'] = comment.pk
        if not comment.root is None:
            data['root_pk'] = comment.root.pk
        else:
            data['root_pk'] =  ''
        if not parent is None:
            data['recipient'] = comment.recipient.get_displayname()
        else:
            data['recipient'] = ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)