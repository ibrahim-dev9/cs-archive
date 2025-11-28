from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Schedule
from exams.models import Subject # Reusing the Subject model
from django.utils import timezone


def schedule_list(request):
    # Get filter parameters
    subject_id = request.GET.get('subject')
    grade = request.GET.get('grade')
    study_type = request.GET.get('study_type')
    exam_type = request.GET.get('type')
    
    # Base queryset - Order by date (upcoming first)
    now = timezone.now()
    queryset = Schedule.objects.filter(date__gte=now).order_by('date')
    
    # Filters
    if subject_id:
        queryset = queryset.filter(subject_id=subject_id)
    if grade:
        queryset = queryset.filter(grade=grade)
    if study_type:
        queryset = queryset.filter(study_type=study_type)
    if exam_type:
        queryset = queryset.filter(type=exam_type)
        
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    schedules = paginator.get_page(page_number)

    subjects = Subject.objects.all()
    
    context = {
        'schedules': schedules,
        'subjects': subjects,
        
        # Preserve filter state
        'selected_subject': int(subject_id) if subject_id else None,
        'selected_grade': int(grade) if grade else None,
        'selected_study_type': int(study_type) if study_type else None,
        'selected_type': int(exam_type) if exam_type else None,
        
        # Choices for dropdowns
        'grade_choices': Schedule.GRADE_CHOICES,
        'study_type_choices': Schedule.STUDY_TYPE_CHOICES,
        'type_choices': Schedule.TYPE_CHOICES,
    }
    return render(request, 'exam_schedule/schedule_list.html', context)