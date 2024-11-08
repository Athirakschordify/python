from rest_framework import viewsets
from .models import Employee, Project, Assignment
from .serializers import EmployeeSerializer, ProjectSerializer, AssignmentSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def perform_update(self, serializer):
        employee = serializer.save()
        if not employee.is_active:
            Assignment.objects.filter(employee=employee).delete()

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
