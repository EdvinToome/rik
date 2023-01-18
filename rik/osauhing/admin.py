from django.contrib import admin
from osauhing.models import Osauhing, PhysicalPartner, LegalPartner, InitialLegalPartner, InitialPhysicalPartner


# Register your models here.
admin.site.register(Osauhing)
admin.site.register(PhysicalPartner)
admin.site.register(LegalPartner)
admin.site.register(InitialLegalPartner)
admin.site.register(InitialPhysicalPartner)