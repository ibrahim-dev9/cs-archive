from django.db import models
from exams.models import Subject  # Importing Subject from the existing exams app

class Schedule(models.Model):
    # Choices (Consistent with Exams app)
    GRADE_CHOICES = [
        (1, 'الصف الأول'),
        (2, 'الصف الثاني'),
        (3, 'الصف الثالث'),
        (4, 'الصف الرابع'),
    ]
    
    TYPE_CHOICES = [
        (1, 'شهري'),
        (2, 'فاينل'),
        (3, 'يومي'),
    ]

    STUDY_TYPE_CHOICES = [
        (1, 'صباحي'),   # Normal
        (2, 'مسائي'),   # Not Normal/Evening
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField(help_text="Date of the exam")
    description = models.TextField(blank=True, null=True)
    
    grade = models.IntegerField(choices=GRADE_CHOICES)
    type = models.IntegerField(choices=TYPE_CHOICES)
    study_type = models.IntegerField(choices=STUDY_TYPE_CHOICES, default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject.name} - {self.date}"
    
    class Meta:
        ordering = ['date'] # Orders by nearest date first