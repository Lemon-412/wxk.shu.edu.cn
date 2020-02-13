from django.contrib import admin
from .models import ClassTable, CollegeTable, CalculatorTable, StudentTable, ScoreTable, TeacherTable

# Register your models here.

admin.site.register(ClassTable)
admin.site.register(CollegeTable)
admin.site.register(CalculatorTable)
admin.site.register(StudentTable)
admin.site.register(ScoreTable)
admin.site.register(TeacherTable)
