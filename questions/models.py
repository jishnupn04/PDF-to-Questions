from django.db import models

class UploadedPDF(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class GeneratedQuestion(models.Model):
    pdf = models.ForeignKey(UploadedPDF, on_delete=models.CASCADE)
    question_text = models.TextField()
    marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
