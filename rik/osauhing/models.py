from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
import datetime
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters are allowed.')
numeric = RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')
def validate_date(date):
    if date > datetime.date.today():
        raise ValidationError("The date cannot be in the future!")
# Create your models here.

class Osauhing(models.Model):
    name = models.CharField( max_length=100, validators=[MinLengthValidator(7), alphanumeric])
    registry_code = models.CharField(max_length=7, validators=[MinLengthValidator(7), numeric])
    foundation_date = models.DateField(validators=[validate_date])
    capital = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(2500)])
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('osauhing-detail', kwargs={'pk': self.pk})



class PhysicalPartner(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    personal_code = models.CharField(max_length=100)
    ownership = models.DecimalField(max_digits=10, decimal_places=0)
    isFounder = models.BooleanField(default=False)
    parent_osauhing = models.ForeignKey(Osauhing, on_delete=models.CASCADE)
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def get_absolute_url(self):
        return reverse('physicalpartner-detail', kwargs={'pk': self.pk})


class LegalPartner(models.Model):
    name = models.CharField(max_length=100)
    registry_code = models.CharField(max_length=100)
    initial_legal_partner = models.ForeignKey('InitialLegalPartner', on_delete=models.CASCADE)
    ownership = models.DecimalField(max_digits=10, decimal_places=0)
    isFounder = models.BooleanField(default=False)
    parent_osauhing = models.ForeignKey(Osauhing, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('legalpartner-detail', kwargs={'pk': self.pk})

class InitialLegalPartner(models.Model):
    name = models.CharField(max_length=100)
    registry_code = models.CharField(max_length=7, validators=[MinLengthValidator(7), numeric])




