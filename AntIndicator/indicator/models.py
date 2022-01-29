from django.db import models

class Count(models.Model):
    corpor_count = models.CharField(max_length=200)
    count = models.CharField(max_length=200)
    foreign_count = models.CharField(max_length=200)
    pbr = models.CharField(max_length=200)
    per = models.CharField(max_length=200)
    personal_count = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    
    def __str__(self):
        return self.question_text