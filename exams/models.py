from django.db import models
from django.core.files.base import ContentFile
from PIL import Image as PilImage
import io
import os

class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.teacher_name}"

class Exam(models.Model):
    # Dropdown choices
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

    # New Field Choices: Normal vs Not Normal
    STUDY_TYPE_CHOICES = [
        (1, 'صباحي'),   # Normal
        (2, 'مسائي'),   # Not Normal/Evening
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    grade = models.IntegerField(choices=GRADE_CHOICES)
    type = models.IntegerField(choices=TYPE_CHOICES)
    
    # Added the new field here with a default value of 1 (Sabahi)
    study_type = models.IntegerField(choices=STUDY_TYPE_CHOICES, default=1)
    
    description = models.TextField(null=True, blank=True)
    
    # The generated PDF will be stored here
    pdf = models.FileField(upload_to='exam_pdfs/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_pdf_from_photos(self):
        """
        Compiles all associated photos into a single PDF and saves it to the pdf field.
        """
        photos = self.photos.all().order_by('id') # Ensure order
        if not photos.exists():
            return

        pil_images = []
        for photo in photos:
            try:
                # Open image and convert to RGB (necessary for PDF)
                img = PilImage.open(photo.image)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                pil_images.append(img)
            except Exception as e:
                print(f"Error processing image {photo.id}: {e}")
                continue

        if pil_images:
            # Create an in-memory byte buffer
            pdf_buffer = io.BytesIO()
            
            # Save images as PDF to the buffer
            pil_images[0].save(
                pdf_buffer, 
                format='PDF', 
                save_all=True, 
                append_images=pil_images[1:]
            )
            
            # Save the buffer content to the Django FileField
            filename = f'exam_{self.id}_{self.subject.name}_grade{self.grade}.pdf'
            self.pdf.save(filename, ContentFile(pdf_buffer.getvalue()), save=False)
            self.save()

    def __str__(self):
        return f"{self.subject.name} - {self.get_grade_display()}"

class Photo(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='exam_photos/')
    
    def __str__(self):
        return f"Photo for {self.exam}"