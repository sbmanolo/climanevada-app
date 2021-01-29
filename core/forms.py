from django import forms
from django.contrib.gis.forms import GeometryCollectionField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Row, Submit, Reset, Button, Column, Fieldset, ButtonHolder, HTML

from leaflet.forms.widgets import LeafletWidget
from bootstrap_daterangepicker import widgets as drwidgets
from bootstrap_daterangepicker import fields as drfields

from datetime import datetime, timedelta, date

from dal import autocomplete, forward

from .models import CnStations, CnVariables

current_date = date.today()
current_date = datetime(current_date.year, current_date.month, current_date.day)

current_year = str(current_date - timedelta(days=365)) + " - " + str(current_date)

LEAFLET_WIDGET_ATTRS = {
    'map_height': '80vh',
    'map_width': '100%',
    'settings_overrides': {
        'DEFAULT_CENTER': (37.05, -3.2),
        'DEFAULT_ZOOM': 10,
    },
    'map_srid': 25830,
    'callback': 'window.map_init_basic',
}

class FormMapWidget(LeafletWidget):
    geometry_field_class = 'LeafletGeometryField'

class VariableTypeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.variable_type

class StationsForm(autocomplete.FutureModelForm):

    variables = forms.CharField()

    class Meta:
        model = CnStations
        fields = ['station_name','variables']
        labels = {'station_name':'Name','date_range':'Date range'}   
    
    def __init__(self, *args, **kwargs):

        super(StationsForm, self).__init__(*args, **kwargs)

        variable_type_choices = list(dict.fromkeys([(item.variable_type, item.variable_type) for item in CnVariables.objects.filter(variable_type__isnull=False).order_by('variable_type')]))
        
        self.fields['variable_type'] = forms.CharField(widget=autocomplete.ListSelect2(choices=variable_type_choices, url='variable-type-autocomplete', forward=['station_name'], attrs={'data-placeholder': (u'Leave blank to show all')}), required=False) 
        self.fields['variable_type'] = forms.CharField(widget=autocomplete.ListSelect2(choices=variable_type_choices, url='variable-type-autocomplete', forward=['station_name'], attrs={'data-placeholder': (u'Leave blank to show all')}), required=False) 
        self.fields['variables'] = forms.ModelMultipleChoiceField(queryset=CnVariables.objects.all(),widget=autocomplete.ModelSelect2Multiple(url='variables-autocomplete',forward=['station_name', 'variable_type','altitude']), required=False)
        self.fields['station_name'] = forms.ModelMultipleChoiceField(queryset=CnStations.objects.all(),widget=autocomplete.ModelSelect2Multiple(url='stations-autocomplete',forward=['variables','altitude', 'sensors-toggle']), required=False)   
        self.fields['altitude'] = forms.CharField(widget=forms.TextInput(attrs={'class':'js-range-slider irs-hidden-input shiny-bound-input', 'id':'selAltitude', 'data-type':'double', 'data-min':'0', 'data-max':'3399', 'data-step':'1', 'data-grid':'true', 'data-grid-num':'9.99705882352941', 'data-grid-snap':'false', 'data-prettify-separator':',', 'data-prettify-enabled':'true', 'data-keyboard':'true', 'data-drag-interval':'true', 'data-data-type':'number' }), required=False) # 'data-from':'1', 'data-to':'3398',
        self.fields['date_range'] = drfields.DateTimeRangeField(input_formats=['%Y-%m-%d %I:%M:%S'],widget=drwidgets.DateTimeRangeWidget(format='%Y-%m-%d %I:%M:%S'), initial=current_year, required=False) #attrs={'data-toggle':'datetimepickerr', 'data-target':'#datetimepicker'}
        self.fields['location'] =  GeometryCollectionField(label='', widget=FormMapWidget(attrs=LEAFLET_WIDGET_ATTRS), required=False)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Fieldset(
                    '',
                    HTML('<div class="col-md-12" style="padding-left:0px;padding-right:0px;" id="toggle-group"><input id="stations-toggle" class="btn-obsnev" type="checkbox" checked data-toggle="toggle" data-onstyle="success" data-on="Stations" data-off="Stations" data-width="49%" data-size="bg"> <input id="sensors-toggle" class="btn-obsnev" type="checkbox" checked data-toggle="toggle" data-onstyle="success" data-on="Sensors" data-off="Sensors" data-width="49%" data-size="bg"></div>'),
                    'variable_type',
                    'variables',
                    'station_name',
                    'altitude',
                    'date_range',
                    ButtonHolder(
                        Div(
                            Button('tutorial', 'Tutorial', css_class='btn btn-outline-secondary',),
                            Button('reset', 'Reset', css_class='btn btn-secondary reset-stations-form', onclick="window.location.href = '/stations';"),
                            Submit('download', 'Download', css_class='btn btn-primary btn-download'),
                            css_class='',
                        ),
                        Div(
                            id='disabled-download-info',
                            css_class='alert alert-warning',
                            role='alert',
                        ),
                    )
                ), css_class='col-lg-3 col-md-4 side-form-scroll', id="map-query"), 
            Div(
                Field('location'), css_class='col-lg-9 col-md-8', id="map-div"),
                css_class='row',
            ),
        )