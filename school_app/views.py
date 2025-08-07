from django.http import HttpResponse
import json
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .constant import CACHE_TIMEOUT
from .models import Class, Student
from .serializers import StudentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404


def fake_data(request):
    c2 = Class.objects.create(name="清华班")
    c3 = Class.objects.create(name="北大班")
    c1 = Class.objects.create(name="少年班")

    Student.objects.create(name='刘德华', gender='M',student_id='111',class_name=c1)
    Student.objects.create(name='郭德纲', gender='M',student_id='122',class_name=c1)
    Student.objects.create(name='孙悟空', gender='M', student_id='133', class_name=c1)

    Student.objects.create(name='张大大', gender='M', student_id='144', class_name=c2)
    Student.objects.create(name='李小龙', gender='M', student_id='155', class_name=c2)
    Student.objects.create(name='孙博世', gender='M', student_id='166', class_name=c3)

    return HttpResponse("Hello, world. You're at the")



class StudentsByClassView(APIView):
    """
    根据班级获取学生信息
    """
    @swagger_auto_schema(
        operation_description="根据班级获取学生信息",
        operation_summary="根据班级获取学生信息",
        manual_parameters=[
            openapi.Parameter(
                'name', openapi.IN_QUERY, description="班级名称", type=openapi.TYPE_STRING, required=True
            )
        ]
    )
    def get(self, request):
        class_name = request.query_params.get('name')
        if not class_name:
            return Response({'error': 'class_name is required'}, status=status.HTTP_400_BAD_REQUEST)
        cache_key = f'class_students:{class_name}'
        cached_data = cache.get(cache_key)
        if cached_data:
            students = json.loads(cached_data)
            return Response(students)

        try:
            class_obj = Class.objects.get(name=class_name)
        except Class.DoesNotExist:
            return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)
        students_qs = class_obj.students.all()
        serializer = StudentSerializer(students_qs, many=True)
        data = serializer.data

        cache.set(cache_key, json.dumps(data), )
        return Response(data)

class StudentByNameView(APIView):
    """
    View to get student information by name
    """

    @swagger_auto_schema(

        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description="学生姓名",
                type=openapi.TYPE_STRING,
                required=True,

            )
        ],
        responses={
            200: openapi.Response('成功返回学生信息', StudentSerializer),
            400: '缺少参数或参数错误',
            404: '学生不存在'
        },
    operation_description= "根据学生姓名获取学生信息",
    operation_summary= "根据学生姓名获取学生信息"

    )

    def get(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response({'error': 'name is required'}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f'student_info:{name}'
        cached_data = cache.get(cache_key)
        if cached_data:
            student = json.loads(cached_data)
            return Response(student)

        try:
            student = Student.objects.select_related('class_name').get(name=name)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student)
        data = serializer.data

        cache.set(cache_key, json.dumps(data), )
        return Response(data)
class StudentCreateView(APIView):
    serializer_class = StudentSerializer

    @swagger_auto_schema(
        request_body=StudentSerializer,
        operation_summary="创建学生",
        operation_description="根据请求体创建一个学生，并更新缓存"

    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            self.update_cache(student)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_cache(self, student):
        class_name = student.class_name.name
        cache_key_class = f'class_students:{class_name}'
        cached_students = cache.get(cache_key_class)
        if cached_students:
            students = json.loads(cached_students)
            students.append(StudentSerializer(student).data)
            cache.set(cache_key_class, json.dumps(students), )

        # 更新学生信息缓存
        cache_key_student = f'student_info:{student.name}'
        cache.set(cache_key_student, json.dumps(StudentSerializer(student).data), )

class StudentUpdateView(APIView):
    serializer_class = StudentSerializer

    @swagger_auto_schema(
        request_body=StudentSerializer,
        responses={200: StudentSerializer},
        operation_description="更新学生信息",
        operation_summary="更新学生信息"
    )
    def put(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = self.serializer_class(student, data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            self.update_cache(student)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=StudentSerializer,
        responses={200: StudentSerializer}
    )
    def patch(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = self.serializer_class(student, data=request.data, partial=True)
        if serializer.is_valid():
            student = serializer.save()
            self.update_cache(student)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_cache(self, student):
        # 先清理所有班级缓存，简单起见
        for class_obj in Class.objects.all():
            cache_key_class = f'class_students:{class_obj.name}'
            cache.delete(cache_key_class)

        # 更新学生信息缓存
        cache_key_student = f'student_info:{student.name}'
        cache.set(cache_key_student, json.dumps(StudentSerializer(student).data), CACHE_TIMEOUT)