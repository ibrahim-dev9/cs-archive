from django.contrib import admin
from .models import Subject, Exam, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    # Added study_type to list_display and list_filter
    list_display = ('subject', 'grade', 'type', 'study_type', 'created_at', 'has_pdf')
    list_filter = ('grade', 'subject', 'type', 'study_type')
    search_fields = ('subject__name', 'description')
    inlines = [PhotoInline]
    
    actions = ['generate_pdf_action']

    def generate_pdf_action(self, request, queryset):
        count = 0
        for exam in queryset:
            exam.generate_pdf_from_photos()
            count += 1
        self.message_user(request, f"Generated PDFs for {count} exams.")
    generate_pdf_action.short_description = "Generate PDF from attached photos"

    def has_pdf(self, obj):
        return bool(obj.pdf)
    has_pdf.boolean = True

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.generate_pdf_from_photos()

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher_name')

admin.site.register(Photo)