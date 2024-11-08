from django.db import models

class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ('Engineering', 'Engineering'),
        ('HR', 'HR'),
        ('Marketing', 'Marketing'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Assignment(models.Model):
    ROLE_CHOICES = [
        ('Developer', 'Developer'),
        ('Manager', 'Manager'),
        ('QA', 'QA'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="assignments")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="assignments")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    hours_per_week = models.IntegerField()

    def __str__(self):
        return f"{self.employee} - {self.project} ({self.role})"
