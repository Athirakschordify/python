from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, ProjectViewSet, AssignmentViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'assignments', AssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
