from django.db import models

class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ('Engineering', 'Engineering'),
        ('HR', 'HR'),
        ('Marketing', 'Marketing'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
      return self.first_name + ' ' + self.last_name

class Project(models.Model):
    name = models.CharField(max_length=200)
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
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    hours_per_week = models.PositiveIntegerField()

    def __str__(self):
      return self.first_name + ' ' + self.last_name

