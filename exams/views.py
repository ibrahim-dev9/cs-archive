from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Exam, Subject

def exam_list(request):
    # Get filter parameters from URL
    subject_id = request.GET.get('subject')
    grade = request.GET.get('grade')
    study_type = request.GET.get('study_type')
    exam_type = request.GET.get('type')  # Added type retrieval
    
    # Start with the base queryset
    queryset = Exam.objects.all().order_by('-created_at')
    
    # Filter by Subject
    if subject_id:
        queryset = queryset.filter(subject_id=subject_id)
    
    # Filter by Grade
    if grade:
        queryset = queryset.filter(grade=grade)

    # Filter by Study Type (Normal/Evening)
    if study_type:
        queryset = queryset.filter(study_type=study_type)

    # Filter by Exam Type (Monthly/Final)
    if exam_type:
        queryset = queryset.filter(type=exam_type)
        
    # Pagination: 20 items per page
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    exams = paginator.get_page(page_number)

    subjects = Subject.objects.all()
    
    context = {
        'exams': exams,
        'subjects': subjects,
        'selected_subject': int(subject_id) if subject_id else None,
        'selected_grade': int(grade) if grade else None,
        'selected_study_type': int(study_type) if study_type else None,
        'selected_type': int(exam_type) if exam_type else None, # Pass back to template
        'grade_choices': Exam.GRADE_CHOICES,
        'study_type_choices': Exam.STUDY_TYPE_CHOICES,
        'type_choices': Exam.TYPE_CHOICES, # Pass type choices
    }
    return render(request, 'exams/exams_list.html', context)