from django.db import models


class Class(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    student_id = models.CharField(max_length=20, unique=True)
    class_name = models.ForeignKey(Class, related_name='students', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
