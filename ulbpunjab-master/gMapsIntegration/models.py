from django.db import models

# Create your models here.
class Airports(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=25, decimal_places=20)
    longitude = models.DecimalField(max_digits=25, decimal_places=20)
    area = models.DecimalField(max_digits=35, decimal_places=20)
    class Meta:
        ordering = ('latitude', 'longitude')
    def __str__(self):
        return self.name

class Highway(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=25, decimal_places=20)
    longitude = models.DecimalField(max_digits=25, decimal_places=20)
    area = models.DecimalField(max_digits=35, decimal_places=20)
    class Meta:
        ordering = ('latitude', 'longitude')
    def __str__(self):
        return self.name

class Rivers(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=25, decimal_places=20)
    longitude = models.DecimalField(max_digits=25, decimal_places=20)
    area = models.DecimalField(max_digits=35, decimal_places=20)
    class Meta:
        ordering = ('latitude', 'longitude')
    def __str__(self):
        return self.name

class Water(models.Model):
    latitude = models.DecimalField(max_digits=25, decimal_places=20)
    longitude = models.DecimalField(max_digits=25, decimal_places=20)
    area = models.DecimalField(max_digits=35, decimal_places=20)
    # latitude_top = models.DecimalField(max_digits=25, decimal_places=20)
    # latitude_bottom = models.DecimalField(max_digits=25, decimal_places=20)
    # longitude_left = models.DecimalField(max_digits=25, decimal_places=20)
    # longitude_right = models.DecimalField(max_digits=25, decimal_places=20)

    class Meta:
        ordering = ('latitude', 'longitude')
    def __str__(self):
        location = str(self.latitude) + ',' + str(self.longitude)
        return location

class Wells(models.Model):
    latitude = models.DecimalField(max_digits=25, decimal_places=20)
    longitude = models.DecimalField(max_digits=25, decimal_places=20)
    area = models.DecimalField(max_digits=35, decimal_places=20)
    # latitude_top = models.DecimalField(max_digits=25, decimal_places=20)
    # latitude_bottom = models.DecimalField(max_digits=25, decimal_places=20)
    # longitude_left = models.DecimalField(max_digits=25, decimal_places=20)
    # longitude_right = models.DecimalField(max_digits=25, decimal_places=20)

    class Meta:
        ordering = ('latitude', 'longitude')
    def __str__(self):
        location = str(self.latitude) + ',' + str(self.longitude)
        return location

class States(models.Model):
    state = models.CharField(max_length=100)
    class Meta:
        ordering = ["state"]
    def __str__(self):
        return self.state

class Districts(models.Model):
    state = models.ForeignKey(States, related_name='districts', on_delete=models.CASCADE)
    district = models.CharField(max_length=100)
    class Meta:
        ordering = ["state", "district"]
    def __str__(self):
        return (str(self.district) + ', ' + str(self.state))

class Landfills(models.Model):
    district = models.ForeignKey(Districts, related_name='landfills', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=25, decimal_places=20)
    longitude = models.DecimalField(max_digits=25, decimal_places=20)
    area = models.DecimalField(max_digits=35, decimal_places=20)
    distance_airport = models.DecimalField(max_digits=35, decimal_places=20)
    distance_water = models.DecimalField(max_digits=35, decimal_places=20)
    distance_well = models.DecimalField(max_digits=35, decimal_places=20)
    distance_road = models.DecimalField(max_digits=35, decimal_places=20)
    distance_river = models.DecimalField(max_digits=35, decimal_places=20)
    road_name = models.CharField(max_length=1000)
    airport_name = models.CharField(max_length=1000)
    river_name = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('latitude', 'longitude')
    def __str__(self):
        return self.name

class LandfillsFinalSiteConceptualModel(models.Model):
    landfill = models.ForeignKey(Landfills, related_name='landfill_final_site_conceptual_model', on_delete=models.CASCADE)
    s0 = models.TextField(default="")
    s1 = models.TextField(default="")
    s2 = models.TextField(default="")
    s3 = models.TextField(default="")
    s4 = models.TextField(default="")
    s5 = models.TextField(default="")
    s6 = models.TextField(default="")
    s7 = models.TextField(default="")
    s8 = models.TextField(default="")
    s9 = models.TextField(default="")
    s10 = models.TextField(default="")
    s11 = models.TextField(default="")
    class Meta:
        ordering = ["landfill"]
    def __str__(self):
        return self.landfill.name

class LandfillsBaselineDataModel(models.Model):
    landfill = models.ForeignKey(Landfills, related_name='landfill_baseline_data', on_delete=models.CASCADE)
    x0 = models.TextField(default="")
    x1 = models.TextField(default="")
    x2 = models.TextField(default="")
    x3 = models.TextField(default="")
    x4 = models.TextField(default="")
    x5 = models.TextField(default="")
    x6 = models.TextField(default="")
    x7 = models.TextField(default="")
    x8 = models.TextField(default="")
    class Meta:
        ordering = ["landfill"]
    def __str__(self):
        return self.landfill.name

class LandfillsImages(models.Model):
    landfill = models.ForeignKey(Landfills, related_name='images', on_delete=models.CASCADE)
    image = models.FileField(upload_to='landfills/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["landfill"]
    def __str__(self):
        return self.landfill.name

class LandfillsExtra(models.Model):
    landfill = models.ForeignKey(Landfills, related_name='landfill_extra', on_delete=models.CASCADE)
    distance_water = models.DecimalField(max_digits=35, decimal_places=20, default=10000)
    depth_waste = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    area = models.DecimalField(max_digits=35, decimal_places=20, default=0)
    groundwater_depth = models.DecimalField(max_digits=14, decimal_places=4, default=100)
    soil_perm = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    groundwater_quality = models.IntegerField(default=0)
    distance_habitat = models.DecimalField(max_digits=35, decimal_places=20, default=100)
    distance_airport = models.DecimalField(max_digits=35, decimal_places=20, default=100)
    distance_water_body = models.DecimalField(max_digits=35, decimal_places=20, default=10000)
    type_soil = models.DecimalField(max_digits=14, decimal_places=4, default=100)
    life_future = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    waste_type = models.IntegerField(default=0)
    waste_quantity_site = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    waste_quantity_disposed = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    distance_village = models.DecimalField(max_digits=35, decimal_places=20, default=10000)
    flood = models.DecimalField(max_digits=14, decimal_places=4, default=1000)
    rainfall_annual = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    distance_city = models.DecimalField(max_digits=35, decimal_places=20, default=100)
    public_acceptance = models.IntegerField(default=0)
    ambient_air = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    waste_hazard = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    biodegradable_waste = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    age_filing = models.DecimalField(max_digits=14, decimal_places=4, default=100)
    waste_moisture = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    bod = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    cod = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    tds = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    class Meta:
        ordering = ["landfill"]
    def __str__(self):
        return self.landfill.name

class LandfillConceptualModel(models.Model):
    landfill = models.ForeignKey(Landfills, related_name='landfill_conceptual_model', on_delete=models.CASCADE)
    index = models.IntegerField()
    data = models.TextField()
    class Meta:
        ordering = ["landfill"]
    def __str__(self):
        return (str(self.index) + " - " + self.landfill.name)

class LandfillSample(models.Model):
    landfill = models.ForeignKey(Landfills, related_name='landfill_sample', on_delete=models.CASCADE)
    sample_type = models.IntegerField()
    index = models.IntegerField()
    completed = models.IntegerField(default=0)
    class Meta:
        ordering = ["sample_type" ,"index", "landfill"]
    def __str__(self):
        return (str(self.sample_type) + " " + str(self.index) + " - " + self.landfill.name)

class LandfillSampleData(models.Model):
    landfill_sample = models.ForeignKey(LandfillSample, related_name='landfill_sample_data', on_delete=models.CASCADE)
    index = models.IntegerField()
    data = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    class Meta:
        ordering = ["index"]
    def __str__(self):
        return (str(self.landfill_sample.sample_type) + " " + str(self.landfill_sample.index) + " " + str(self.index) + " - " + self.landfill_sample.landfill.name)

class LandfillSampleComments(models.Model):
    landfill = models.ForeignKey(Landfills, related_name='landfill_sample_comments', on_delete=models.CASCADE)
    sample_type = models.IntegerField()
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["landfill"]
    def __str__(self):
        return self.landfill.name

class LandfillProtocolComments(models.Model):
    landfill = models.ForeignKey(Landfills, related_name='landfill_protocol_comments', on_delete=models.CASCADE)
    index = models.IntegerField()
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["landfill"]
    def __str__(self):
        return self.landfill.name

class LandfillForm1(models.Model):
    landfill = models.ForeignKey(Landfills, related_name='landfill_form1', on_delete=models.CASCADE)
    s0 = models.TextField(default="")
    s1 = models.TextField(default="")
    s2 = models.TextField(default="")
    s3 = models.TextField(default="")
    s4 = models.TextField(default="")
    s5 = models.TextField(default="")
    s6 = models.TextField(default="")
    s7 = models.TextField(default="")
    s8 = models.TextField(default="")
    s9 = models.TextField(default="")
    s10 = models.TextField(default="")
    s11 = models.TextField(default="")
    class Meta:
        ordering = ["landfill"]
    def __str__(self):
        return self.landfill.name

class LandfillForm4(models.Model):
    landfill = models.ForeignKey(Landfills, related_name='landfill_form4', on_delete=models.CASCADE)
    s0 = models.TextField(default="")
    s1 = models.TextField(default="")
    s2 = models.TextField(default="")
    s3 = models.TextField(default="")
    s4 = models.TextField(default="")
    s5 = models.TextField(default="")
    s6 = models.TextField(default="")
    s7 = models.TextField(default="")
    s8 = models.TextField(default="")
    s9 = models.TextField(default="")
    s10 = models.TextField(default="")
    s11 = models.TextField(default="")
    class Meta:
        ordering = ["landfill"]
    def __str__(self):
        return self.landfill.name
