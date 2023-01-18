from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.admin.widgets import AdminDateWidget
from django.urls import reverse_lazy
from .forms import CreateOsauhingForm, CreatePhysicalPartnerForm, CreateLegalPartnerForm, LegalPartnerFormset, PhysicalPartnerFormset
from .models import Osauhing, PhysicalPartner, LegalPartner
import inspect

class OsauhingList(ListView):
    model = Osauhing
    legalpartners = LegalPartner.objects.all()
    physicalpartners = PhysicalPartner.objects.all()

    def get_queryset(self):
        name = self.request.GET.get('search')
        object_list = self.model.objects.all()
        final_object_list = self.model.objects.all()

        if name:
            # Make filter multiple parameters with OR
            final_object_list = object_list.filter(name__icontains=name)
            final_object_list = final_object_list | object_list.filter(registry_code__icontains=name)
            for legalpartner in self.legalpartners:
                if legalpartner.name.lower().__contains__(name.lower()):
                    final_object_list = final_object_list | object_list.filter(id=legalpartner.parent_osauhing_id)
                if legalpartner.registry_code.lower().__contains__(name.lower()):
                    final_object_list = final_object_list | object_list.filter(id=legalpartner.parent_osauhing_id)
            for physicalpartner in self.physicalpartners:
                full_name = physicalpartner.first_name + " " + physicalpartner.last_name
                if physicalpartner.first_name.lower().__contains__(name.lower()):
                    final_object_list = final_object_list | object_list.filter(id=physicalpartner.parent_osauhing_id)
                if physicalpartner.last_name.lower().__contains__(name.lower()):
                    final_object_list = final_object_list | object_list.filter(id=physicalpartner.parent_osauhing_id)
                if physicalpartner.personal_code.lower().__contains__(name.lower()):
                    final_object_list = final_object_list | object_list.filter(id=physicalpartner.parent_osauhing_id)
                if full_name.lower().__contains__(name.lower()):
                    final_object_list = final_object_list | object_list.filter(id=physicalpartner.parent_osauhing_id)
                    
        return final_object_list


class OsauhingView(DetailView):
    model = Osauhing

    # Add legal partners where parent is osauhing
    def get_context_data(self, **kwargs):
        context = super(OsauhingView, self).get_context_data(**kwargs)
        context['legalpartners'] = LegalPartner.objects.filter(parent_osauhing_id=self.object.id)
        context['physicalpartners'] = PhysicalPartner.objects.filter(parent_osauhing_id=self.object.id)
        return context
def unique(list1):

# initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        match = False
        # check if exists in unique_list or not
        xname = str(x.name)
        for y in unique_list:
            yname = str(y.name)
            if xname == yname:
                match = True
                break
        if match == False:
            unique_list.append(x)
            match == False
    return unique_list

class OsauhingCreate(CreateView):
    model = Osauhing

    def form_valid(self, form):
        result = super(OsauhingCreate, self).form_valid(form)
        legalparnters_formset = LegalPartnerFormset(form.data, instance=self.object, prefix='legalpartners_formset')
        physicalpartners_formset = PhysicalPartnerFormset(form.data, instance=self.object,
                                                          prefix='physicalpartners_formset')
        partner_exist = False
        total_ownership = 0
        for legal_partner in legalparnters_formset.cleaned_data:
            total_ownership += legal_partner['ownership']
            for existing_legal_partner in LegalPartner.objects.all():
                if legal_partner['name'] == existing_legal_partner.name and legal_partner['registry_code'] == existing_legal_partner.registry_code:
                    partner_exist = True
                    break
            if partner_exist == False:
                form.add_error(None, 'Legal partner with name ' + legal_partner['name'] + ' and registry code ' + legal_partner['registry_code'] + ' does not exist')
                return super().form_invalid(form)
            partner_exist = False
        if total_ownership != form.cleaned_data['capital']:
            form.add_error(None, 'Total ownership of legal partners is not equal to osauhing capital')
            return super().form_invalid(form)

        if legalparnters_formset.is_valid():    
            legalpartners = legalparnters_formset.save()
        if physicalpartners_formset.is_valid():
            physicalpartners = physicalpartners_formset.save()
        return result

    def get_context_data(self, **kwargs):
        context = super(OsauhingCreate, self).get_context_data(**kwargs)
        context['legalpartners_formset'] = LegalPartnerFormset(prefix='legalpartners_formset')
        context['physicalpartners_formset'] = PhysicalPartnerFormset(prefix='physicalpartners_formset')
        context['all_legal_partners'] = unique(LegalPartner.objects.all())
        context['all_physical_partners'] = PhysicalPartner.objects.all()
        context['temp_legal_partners'] = ['']
        return context
    #Add validation for formsets
    def save(self, commit=True):
       self.object = super(OsauhingCreate, self).save(commit=False)
#
    form_class = CreateOsauhingForm
    template = 'osauhing/osauhing_form.html'
    # , 'physical_partners', 'legal_partners'

    success_url = reverse_lazy('osauhing_list')


class OsauhingUpdate(UpdateView):
    model = Osauhing
    form_class = CreateOsauhingForm
    # , 'physical_partners', 'legal_partners'
    template = 'osauhing/osauhing_form.html'
    success_url = reverse_lazy('osauhing_list')


class OsauhingDelete(DeleteView):
    model = Osauhing
    success_url = reverse_lazy('osauhing_list')


class PhysicalPartnerList(ListView):
    model = PhysicalPartner


class PhysicalPartnerView(DetailView):
    model = PhysicalPartner


class PhysicalPartnerCreate(CreateView):
    model = PhysicalPartner
    form_class = CreatePhysicalPartnerForm
    template = 'osauhing/osauhing_form.html'
    success_url = reverse_lazy('physicalpartner_list')


# Create your views here.

class PhysicalPartnerUpdate(UpdateView):
    model = PhysicalPartner
    form_class = CreatePhysicalPartnerForm
    template = 'osauhing/osauhing_form.html'
    success_url = reverse_lazy('physicalpartner_list')


class PhysicalPartnerDelete(DeleteView):
    model = PhysicalPartner
    success_url = reverse_lazy('physicalpartner_list')


class LegalPartnerList(ListView):
    model = LegalPartner


class LegalPartnerView(DetailView):
    model = LegalPartner


class LegalPartnerCreate(CreateView):
    model = LegalPartner
    form_class = CreateLegalPartnerForm
    template = 'osauhing/osauhing_form.html'
    success_url = reverse_lazy('legalpartner_list')


class LegalPartnerUpdate(UpdateView):
    model = LegalPartner
    form_class = CreateLegalPartnerForm
    template = 'osauhing/osauhing_form.html'
    success_url = reverse_lazy('legalpartner_list')


class LegalPartnerDelete(DeleteView):
    model = LegalPartner
    success_url = reverse_lazy('legalpartner_list')
