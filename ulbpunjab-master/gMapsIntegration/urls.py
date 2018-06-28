from django.conf.urls import url
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name = 'home'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'gMapsIntegration/form.html'}, name='logout'),
    url(r'^login/$', auth_views.login,{'template_name': 'gMapsIntegration/form.html'},name='login'),
    url(r'^populate_states_districts_data', views.populate_states_districts_data, name = 'populate_states_districts_data'),
    url(r'^landfilladd/', views.landfilladd, name = 'landfilladd'),
    url(r'^data/', views.add_data, name = 'add_data'),
    url(r'^details/(?P<ids>[\d]+)/monitoring/', views.monitoring, name = 'monitoring'),
    url(r'^api_sendDistricts/', views.api_sendDistricts, name = 'api_sendDistricts'),
    url(r'^details/(?P<ids>[\d]+)/LandfillSiteConceptualModelSubmit/', views.LandfillsFinalSiteConceptualModelSubmit, name = 'LandfillsFinalSiteConceptualModelSubmit'),
    url(r'^details/(?P<ids>[\d]+)/baselinedata/', views.LandfillsBaselineDataSubmit, name = 'LandfillsBaselineDataSubmit'),
    url(r'^details/(?P<ids>[\d]+)/add_more/', views.add_more, name = 'add_more'),
    url(r'^details/(?P<ids>[\d]+)/edit_add_more/', views.edit_add_more, name = 'edit_add_more'),
    url(r'^details/(?P<ids>[\d]+)/sampling_protocol/surface_water/(?P<sam_num>[\d]+)/', views.surface_water_sample, name = 'surface_water_sample'),
    url(r'^details/(?P<ids>[\d]+)/sampling_protocol/surface_water/', views.surface_water, name = 'surface_water'),
    url(r'^details/(?P<ids>[\d]+)/sampling_protocol/ground_water/(?P<sam_num>[\d]+)/', views.ground_water_sample, name = 'ground_water_sample'),
    url(r'^details/(?P<ids>[\d]+)/sampling_protocol/ground_water/', views.ground_water, name = 'ground_water'),
    url(r'^details/(?P<ids>[\d]+)/sampling_protocol/sediment/(?P<sam_num>[\d]+)/', views.sediment_sample, name = 'sediment_sample'),
    url(r'^details/(?P<ids>[\d]+)/sampling_protocol/sediment/', views.sediment, name = 'sediment'),
    url(r'^details/(?P<ids>[\d]+)/sampling_protocol/soil/(?P<sam_num>[\d]+)/', views.soil_sample, name = 'soil_sample'),
    url(r'^details/(?P<ids>[\d]+)/sampling_protocol/soil/', views.soil, name = 'soil'),
    url(r'^details/(?P<ids>[\d]+)/sampling_protocol/upload_images', views.upload_images, name = 'upload_images'),
    url(r'^details/(?P<ids>[\d]+)/sampling_protocol/', views.sampling_protocol, name = 'sampling_protocol'),
    url(r'^details/(?P<ids>[\d]+)/form1/(?P<langs>[\d]+)/', views.form1, name = 'form1'),
    url(r'^details/(?P<ids>[\d]+)/form4/', views.form4, name = 'form4'),
    url(r'^details/(?P<ids>[\d]+)/', views.details, name = 'details'),
    url(r'^search/', views.search, name = 'search'),
]
