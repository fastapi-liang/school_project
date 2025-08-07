from rest_framework import serializers
from .models import Class, Student

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields =  '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class_names = serializers.CharField(source='class_name.name', read_only=True)
    class Meta:
        model = Student
        fields = ['id', 'name', 'gender', 'student_id', 'class_names', 'class_name']


# 第二种方法
# class StudentSerializer(serializers.ModelSerializer):
#     class_name_name = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Student
#         fields = ['id', 'name', 'class_name', 'class_name_name']
#
#     def get_class_name_name(self, obj):
#         return obj.class_name.name if obj.class_name else None