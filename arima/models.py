from django.db import models


# Create your models here.
class Arima(models.Model):
    input = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    output = models.CharField(max_length=2000)
    total_time = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=200,null=True)
    log_file = models.CharField(max_length=200,null=True)
    created_time = models.DateTimeField(auto_now=True)
    resolved_time = models.DateTimeField(auto_now=True)