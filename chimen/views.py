from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from guidelines.models import Guideline


def home(request):
    context = {}
    return render(request, 'home.html', context)

def search(request):
    keywords = request.GET.get('keyword', '').strip()
    
    condition = None
    for keyword in keywords.split(' '):
        if condition is None:
            condition = Q(additional_information__contains=keyword)
        else:
            condition = condition | Q(additional_information__contains=keyword)
    
    result = []
    if condition is not None:
        result = Guideline.objects.filter(condition)
    
    paginator = Paginator(result, 20)
    target_page_num = request.GET.get('page', 1)
    current_page = paginator.get_page(target_page_num)
    
    context = {}
    context['keywords'] = keywords
    context['result'] = result
    context['result_count'] = result.count()
    context['current_page'] = current_page

    return render(request, 'search.html', context)