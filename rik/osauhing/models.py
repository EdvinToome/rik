from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator, ValidationError
import datetime
alphanumeric = RegexValidator(r'^[0-9a-zA-Z\s]*$', 'Only alphanumeric characters are allowed.')
alpha = RegexValidator(r'^[a-zA-Z\s]*$', 'Only alphabetic characters are allowed.')
numeric = RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')
def validate_date(date):
    if date > datetime.date.today():
        raise ValidationError("The date cannot be in the future!")
# Create your models here.

class Osauhing(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3), alphanumeric], verbose_name='Nimi')
    registry_code = models.CharField(max_length=7, validators=[MinLengthValidator(7), numeric], verbose_name='Registrikood')
    foundation_date = models.DateField(validators=[validate_date], verbose_name='Asutamiskuupäev')
    capital = models.DecimalField(max_digits=15, decimal_places=0, validators=[MinValueValidator(2500)], verbose_name='Kapitaal')
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('osauhing-detail', kwargs={'pk': self.pk})



class PhysicalPartner(models.Model):
    initial_physical_partner = models.ForeignKey('InitialPhysicalPartner', on_delete=models.CASCADE)
    ownership = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(1), numeric])
    isFounder = models.BooleanField(default=True)
    parent_osauhing = models.ForeignKey(Osauhing, on_delete=models.CASCADE)
    def __str__(self):
        return self.initial_physical_partner.first_name+' '+self.initial_physical_partner.last_name+' '+self.parent_osauhing.name
    def get_absolute_url(self):
        return reverse('physicalpartner-detail', kwargs={'pk': self.pk})


class LegalPartner(models.Model):
#    name = models.CharField(max_length=100)
#    registry_code = models.CharField(max_length=100)
    initial_legal_partner = models.ForeignKey('InitialLegalPartner', on_delete=models.CASCADE)
    ownership = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(1), numeric])
    isFounder = models.BooleanField(default=True)
    parent_osauhing = models.ForeignKey(Osauhing, on_delete=models.CASCADE)
    def __str__(self):
        return self.initial_legal_partner.name+' '+self.parent_osauhing.name
    
    def get_absolute_url(self):
        return reverse('legalpartner-detail', kwargs={'pk': self.pk})

class InitialLegalPartner(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3), alphanumeric])
    registry_code = models.CharField(max_length=7, validators=[MinLengthValidator(7), numeric])
    def __str__(self):
        return self.name

class InitialPhysicalPartner(models.Model):
    first_name = models.CharField(max_length=100, validators=[MinLengthValidator(2), alphanumeric])
    last_name = models.CharField(max_length=100, validators=[MinLengthValidator(2), alphanumeric])
    personal_code = models.CharField(max_length=12,validators=[MinLengthValidator(11), numeric])
    def __str__(self):
        return self.first_name + ' ' + self.last_name

