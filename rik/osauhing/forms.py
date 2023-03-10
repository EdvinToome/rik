from django import forms
from .models import Osauhing, PhysicalPartner, LegalPartner
import datetime
from django.forms.models import inlineformset_factory

LegalPartnerFormset = inlineformset_factory(
    Osauhing, LegalPartner, extra = 0, can_delete = False, fields = ['initial_legal_partner', 'ownership', 'isFounder']
)
PhysicalPartnerFormset = inlineformset_factory(
    Osauhing, PhysicalPartner, extra = 0, can_delete = False, fields = ['initial_physical_partner', 'ownership', 'isFounder']
)
class DateInput(forms.DateInput):
    input_type = 'date'

class CreateLegalPartnerForm(forms.ModelForm):
    class Meta:
        model = LegalPartner
        fields = ['initial_legal_partner', 'ownership', 'isFounder']
    name = forms.CharField()
    registry_code = forms.CharField()
    ownership = forms.DecimalField()
    isFounder = forms.BooleanField(required=False)

class CreateOsauhingForm(forms.ModelForm):
    class Meta:
        model = Osauhing
        fields = ['name', 'registry_code', 'foundation_date', 'capital']
    name = forms.CharField()
    registry_code = forms.CharField()
    foundation_date = forms.DateField(widget=DateInput)
    capital = forms.DecimalField()


class CreatePhysicalPartnerForm(forms.ModelForm):
    class Meta:
        model = PhysicalPartner
        fields = ['initial_physical_partner', 'ownership', 'isFounder']
    first_name = forms.CharField()
    last_name = forms.CharField()
    personal_code = forms.CharField()
    ownership = forms.DecimalField()
    isFounder = forms.BooleanField(required=False)


