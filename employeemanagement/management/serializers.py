from rest_framework import serializers
from .models import Employee, Project, Assignment

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

class AssignmentSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Assignment
        fields = "__all__"

class EmployeeSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = "__all__"
