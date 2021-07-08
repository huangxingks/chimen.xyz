from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.core.paginator import Paginator

from .models import Subject, Guideline
from visits.utils import visit_once


def get_guideline_context(request, guidelines):
    paginator = Paginator(guidelines, settings.GUIDELINE_NUM_PER_PAGE)
    target_page_num = request.GET.get('page', 1)
    current_page = paginator.get_page(target_page_num)
    current_page_num = current_page.number

    page_range = list(range(max(current_page_num-2, 1), min(current_page_num+2, paginator.num_pages)+1))
    if page_range[0]-1>=2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1]>=2:
        page_range.append('...')
    if page_range[0] != 1:    
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    #context['MEDIA_URL'] = settings.MEDIA_URL
    context['subjects'] = Subject.objects.all()
    #context['guideline_num_of_subjects'] = Subject.objects.annotate(applicationguideline_count=Count('applicationguideline'))
    context['guidelines'] = current_page.object_list
    context['current_page'] = current_page
    context['page_range'] = page_range
    return context

def guideline_list(request):
    guidelines = Guideline.objects.all()
    context = get_guideline_context(request, guidelines)
    return render(request, 'guidelines/guideline_list.html', context)

def guideline_by_subject(request, subject_pk):
    subject = get_object_or_404(Subject, pk=subject_pk)
    guidelines = Guideline.objects.filter(subject=subject)
    context = get_guideline_context(request, guidelines)
    context['subject'] = subject    
    return render(request, 'guidelines/guideline_by_subject.html', context)

def guideline_detail(request, guideline_pk):
    guideline = get_object_or_404(Guideline, pk=guideline_pk)
    context = {}
    context['guideline'] = guideline
    response = render(request, 'guidelines/guideline_detail.html', context)
    key = visit_once(request, guideline)
    response.set_cookie(key,'true')
    return response

def guideline_ongoing(request):
    return

def guideline_coming(request):
    return