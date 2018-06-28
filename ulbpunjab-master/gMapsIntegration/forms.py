from django import forms
from .models import Water, Landfills, Wells, Highway, Rivers, Airports, LandfillsExtra, LandfillsImages, LandfillConceptualModel, LandfillSample, LandfillSampleComments, LandfillProtocolComments, LandfillSampleData, LandfillForm1, LandfillForm4, States, Districts, LandfillsFinalSiteConceptualModel, LandfillsBaselineDataModel


class WaterForm(forms.ModelForm):
    class Meta:
        model = Water
        fields = {'latitude', 'longitude', 'area'}

class WellsForm(forms.ModelForm):
    class Meta:
        model = Wells
        fields = {'latitude', 'longitude', 'area'}

class HighwayForm(forms.ModelForm):
    class Meta:
        model = Highway
        fields = {'latitude', 'longitude', 'area', 'name'}

class AirportsForm(forms.ModelForm):
    class Meta:
        model = Airports
        fields = {'latitude', 'longitude', 'area', 'name'}

class RiversForm(forms.ModelForm):
    class Meta:
        model = Rivers
        fields = {'latitude', 'longitude', 'area', 'name'}

class LandfillsForm(forms.ModelForm):
    class Meta:
        model = Landfills
        fields = {'latitude', 'longitude', 'area', 'name', 'distance_airport', 'distance_water', 'distance_well', 'distance_road', 'distance_river', 'road_name', 'airport_name', 'river_name'}

class LandfillsExtraForm(forms.ModelForm):
    class Meta:
        model = LandfillsExtra
        fields = {'distance_water', 'area', 'distance_airport', 'distance_water_body'}

class LandfillsImagesForm(forms.ModelForm):
    class Meta:
        model = LandfillsImages
        fields = {'image'}

class LandfillConceptualModelForm(forms.ModelForm):
    class Meta:
        model = LandfillConceptualModel
        fields = {'index', 'data'}

class LandfillSampleForm(forms.ModelForm):
    class Meta:
        model = LandfillSample
        fields = {'sample_type', 'index'}

class LandfillSampleDataForm(forms.ModelForm):
    class Meta:
        model = LandfillSampleData
        fields = {'data', 'index'}

class LandfillSampleCommentsForm(forms.ModelForm):
    class Meta:
        model = LandfillSampleComments
        fields = {'sample_type', 'comment'}

class LandfillProtocolCommentsForm(forms.ModelForm):
    class Meta:
        model = LandfillProtocolComments
        fields = {'index', 'comment'}

class LandfillForm1Form(forms.ModelForm):
    class Meta:
        model = LandfillForm1
        fields = {'s0'}

class LandfillForm4Form(forms.ModelForm):
    class Meta:
        model = LandfillForm4
        fields = {'s0'}

class LandfillsFinalSiteConceptualModelForm(forms.ModelForm):
    class Meta:
        model = LandfillsFinalSiteConceptualModel
        fields = {'s0'}

class LandfillsBaselineDataModelForm(forms.ModelForm):
    class Meta:
        model = LandfillsBaselineDataModel
        fields = {'x0'}
