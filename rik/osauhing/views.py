from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.admin.widgets import AdminDateWidget
from django.urls import reverse_lazy
from .forms import CreateOsauhingForm, CreatePhysicalPartnerForm, CreateLegalPartnerForm, LegalPartnerFormset, PhysicalPartnerFormset
from .models import Osauhing, PhysicalPartner, LegalPartner, InitialLegalPartner, InitialPhysicalPartner
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
                if legalpartner.initial_legal_partner.name.lower().__contains__(name.lower()):
                    final_object_list = final_object_list | object_list.filter(id=legalpartner.parent_osauhing_id)
                if legalpartner.initial_legal_partner.registry_code.lower().__contains__(name.lower()):
                    final_object_list = final_object_list | object_list.filter(id=legalpartner.parent_osauhing_id)
            for physicalpartner in self.physicalpartners:
                full_name = physicalpartner.initial_physical_partner.first_name + " " + physicalpartner.initial_physical_partner.last_name
                if physicalpartner.initial_physical_partner.first_name.lower().__contains__(name.lower()):
                    final_object_list = final_object_list | object_list.filter(id=physicalpartner.parent_osauhing_id)
                if physicalpartner.initial_physical_partner.last_name.lower().__contains__(name.lower()):
                    final_object_list = final_object_list | object_list.filter(id=physicalpartner.parent_osauhing_id)
                if physicalpartner.initial_physical_partner.personal_code.lower().__contains__(name.lower()):
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

class OsauhingCreate(CreateView):
    model = Osauhing

    def form_valid(self, form): 

        partner_exist = False
        total_ownership = 0
        temp_legal_partners = list()
        temp_physical_partners = list()
        for x in range(0, int(form.data['legalpartners_formset-TOTAL_FORMS'])):
            total_ownership += int(form.data['legalpartners_formset-' + str(x) + '-ownership'])
            if form.data['legalpartners_formset-' + str(x) + '-initial_legal_partner'] in temp_legal_partners:
                form.add_error(None, 'Osanikud ei tohi korduda.')
                return super(OsauhingCreate, self).form_invalid(form)
            temp_legal_partners.append(form.data['legalpartners_formset-' + str(x) + '-initial_legal_partner'])
        for x in range(0, int(form.data['physicalpartners_formset-TOTAL_FORMS'])):
            total_ownership += int(form.data['physicalpartners_formset-' + str(x) + '-ownership'])
            if form.data['physicalpartners_formset-' + str(x) + '-initial_physical_partner'] in temp_physical_partners:
                form.add_error(None, 'Osanikud ei tohi korduda.')
                return super().form_invalid(form)
            temp_physical_partners.append(form.data['physicalpartners_formset-' + str(x) + '-initial_physical_partner'])
        if total_ownership != int(form.data['capital']):
            form.add_error(None, 'Osanike osade suuruste summa peab olema võrdne osaühingu kogukapitali suurusega.')
            return super().form_invalid(form) 
        result = super(OsauhingCreate, self).form_valid(form)
        legalpartners_formset = LegalPartnerFormset(form.data, instance=self.object, prefix='legalpartners_formset')
        physicalpartners_formset = PhysicalPartnerFormset(form.data, instance=self.object, prefix='physicalpartners_formset')
                
        
        if legalpartners_formset.is_valid():          
            legalpartners = legalpartners_formset.save()
        if physicalpartners_formset.is_valid():
            physicalpartners = physicalpartners_formset.save()

        return result

    def get_context_data(self, **kwargs):
        context = super(OsauhingCreate, self).get_context_data(**kwargs)
        context['legalpartners_formset'] = LegalPartnerFormset(prefix='legalpartners_formset')
        context['physicalpartners_formset'] = PhysicalPartnerFormset(prefix='physicalpartners_formset')
        context['all_legal_partners'] = InitialLegalPartner.objects.all()
        context['all_physical_partners'] = InitialPhysicalPartner.objects.all()

        return context
    #Add validation for formsets
    def save(self, commit=True):
       self.object = super(OsauhingCreate, self).save(commit=False)
#
    form_class = CreateOsauhingForm
    template = 'osauhing/osauhing_form.html'
    # , 'physical_partners', 'legal_partners'

    def get_success_url(self):
        return reverse_lazy('osauhing_view', kwargs={'pk': self.object.pk})


class OsauhingUpdate(UpdateView):
    model = Osauhing

#
    form_class = CreateOsauhingForm
    template = 'osauhing/osauhing_form.html'

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
