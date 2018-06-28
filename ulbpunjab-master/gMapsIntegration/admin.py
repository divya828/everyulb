from django.contrib import admin
from .models import Water, Landfills, Wells, Highway, Rivers, Airports, LandfillsExtra, LandfillsImages, LandfillConceptualModel, LandfillSample, LandfillSampleComments, LandfillProtocolComments, LandfillSampleData, LandfillForm1, LandfillForm4, States, Districts, LandfillsFinalSiteConceptualModel, LandfillsBaselineDataModel
# Register your models here.

admin.site.register(Water)
admin.site.register(Landfills)
admin.site.register(Highway)
admin.site.register(Wells)
admin.site.register(Rivers)
admin.site.register(Airports)
admin.site.register(LandfillsExtra)
admin.site.register(LandfillsImages)
admin.site.register(LandfillConceptualModel)
admin.site.register(LandfillSample)
admin.site.register(LandfillSampleComments)
admin.site.register(LandfillProtocolComments)
admin.site.register(LandfillSampleData)
admin.site.register(LandfillForm1)
admin.site.register(LandfillForm4)
admin.site.register(States)
admin.site.register(Districts)
admin.site.register(LandfillsFinalSiteConceptualModel)
admin.site.register(LandfillsBaselineDataModel)
