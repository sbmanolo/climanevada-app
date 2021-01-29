from django.db import models

from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.db.models import PointField

import psycopg2

from string import capwords

class CnNetwork(models.Model):
    network_id = models.IntegerField(primary_key=True, blank=True)
    network_code = models.CharField(max_length=255, blank=True, null=True)
    network_name = models.CharField(max_length=255, blank=True, null=True)
    network_manager = models.CharField(max_length=255, blank=True, null=True)
    network_status = models.CharField(max_length=255, blank=True, null=True)
    data_policy = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cn_network'

    def __str__(self):
        return self.network_name

class CnStations(models.Model):
    station_id = models.IntegerField(primary_key=True, blank=True)
    station_name = models.CharField(max_length=255, blank=True, null=True)
    station_code = models.CharField(max_length=255, blank=True, null=True)
    coord_x = models.FloatField(blank=True, null=True)
    coord_y = models.FloatField(blank=True, null=True)
    epsg = models.IntegerField(blank=True, null=True)
    munic_code = models.IntegerField(blank=True, null=True)
    munic_name = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    cn_network_id = models.ForeignKey(CnNetwork, on_delete=models.DO_NOTHING, db_column="cn_network_id", blank=True, null=True)
    tipo = models.CharField(max_length=255, blank=True, null=True, db_column='type')
    category = models.CharField(max_length=255, blank=True, null=True)
    elev = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    record_start = models.DateTimeField(blank=True, null=True)
    record_end = models.TimeField(blank=True, null=True)
    station_variables_id = models.CharField(max_length=255, blank=True, null=True)
    geom_4326 = gis_models.PointField(srid=4326, blank=True, null=True)
    geom_25830 = gis_models.GeometryField(srid=25830, blank=True, null=True)
    #geom_4326 = models.GeometryField(srid=25830, blank=True, null=True)
    station_type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cn_stations'

    def __str__(self):
        return capwords(self.munic_name) + " (" + self.station_code + ")"

class CnVariables(models.Model):
    variable_code = models.CharField(primary_key=True, max_length=255, blank=True)
    variable_id = models.IntegerField(blank=True, null=True)
    variable_name = models.CharField(max_length=512, blank=True, null=True)
    variable_units = models.CharField(max_length=255, blank=True, null=True)
    variable_type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cn_variables'

    def __str__(self):
        if self.variable_name:
            if self.variable_name[0] == "(":
                return self.variable_code
            else:
                return self.variable_name
        else:
            return self.variable_code

class CnDatos(models.Model):
    time = models.DateTimeField(primary_key=True)
    variable_id = models.IntegerField()
    value = models.FloatField(blank=True, null=True)
    validation_id = models.IntegerField()
    station_id = models.IntegerField()
    #ref = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'cn_datos'
