from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Color(models.Model):
    color_name = models.CharField(max_length=100)

    def __str__(self):
        return self.color_name
    
class Person(models.Model):
    color = models.ForeignKey(Color ,null=True , blank=True, on_delete=models.CASCADE , related_query_name="color")
    name = models.CharField(max_length=100)
    age = models.IntegerField()

class Company(models.Model):
    name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    about = models.TextField()
    type = models.CharField(max_length=100,choices=
                            (("IT","IT"),
                             ("Non IT","Non IT"),
                             ("Moblies Phones","Moblie Phones")
                            ))
    added_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class employee(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    phone = models.IntegerField(validators=[MinValueValidator(6200000000),MaxValueValidator(9999999999)])
    position = models.CharField(max_length=100,choices=(
                                ("Manager","manger"),
                                ("Software Developer","sd"),
                                ("Project Leader","Pl")
                                ))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_query_name="company" )

