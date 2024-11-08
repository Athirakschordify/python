from django.urls import path
from .views import EmployeeListView

urlpatterns = [
    path('employee/<int:pk>', EmployeeListView.as_view()),
        path('employee/', EmployeeListView.as_view()),

]
