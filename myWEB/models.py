from django.db import models

# Create your models here.


class CalculatorTable(models.Model):
    value_A = models.CharField(max_length=10)
    value_B = models.CharField(max_length=10)
    value_C = models.CharField(max_length=10)
