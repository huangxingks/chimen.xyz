from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist

from .models import LikeNum, LikeRecord


def SuccessResponse(like_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['like_num'] = like_num
    return JsonResponse(data)

def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def like_update(request):
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, "Not log in")

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, "Object not exist")

    if request.GET.get('is_liked') != 'true':
        # like
        like_record, is_created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if is_created:
            # not liked， like it
            like_num, is_created = LikeNum.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_num.number += 1
            like_num.save()
            return SuccessResponse(like_num.number)
        else:
            # already liked， cannot like
            return ErrorResponse(402, "Already liked this content")
    else:
        # unlike
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # already liked, unlike it
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            like_num, is_created = LikeNum.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not is_created:
                like_num.number -= 1
                like_num.save()
                return SuccessResponse(like_num.number)
            else:
                return ErrorResponse(404, 'Error')
        else:
            # not liked, cannot unlike
            return ErrorResponse(403, "Haven't liked this content")