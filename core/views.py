import os, csv, zipfile

from datetime import datetime
from string import capwords

from django.http import HttpResponse, FileResponse

from django.db.models import Q

from django.shortcuts import render, redirect

from django.core import serializers
from django.core.files.temp import NamedTemporaryFile

from django.utils.safestring import SafeString

from .models import CnStations, CnVariables, CnNetwork, CnDatos
from .forms import StationsForm

from dal import autocomplete

def is_valid_queryparam(param):
    return param != '' and param is not None

def get_common_variables(stations, exclude):

    stations_qs = CnStations.objects.filter(station_id__in=stations)
    variables_choices_list = []

    if len(stations_qs) > 0:
        for i in range(len(stations_qs)):
            if stations_qs[i].station_variables_id:
                station_variables = stations_qs[i].station_variables_id.split("/")
                station_variables = filter(None, station_variables)
                variables_choices_list.append(station_variables)
    
    if variables_choices_list:
        common_variables = set(variables_choices_list[0])
        if exclude == True:
            for s in variables_choices_list[1:]:
                common_variables.intersection_update(s)
            common_variables = sorted(list(common_variables))
            return common_variables
        else:
            return list(dict.fromkeys(common_variables))
    else:
        return CnVariables.objects.none()

def get_common_stations(variables, variable_type, exclude):

    variables_qs = CnVariables.objects.filter(variable_code__in=variables)
    stations_qs = CnStations.objects.all()
    variables_choices_list = []

    variables_ids = list(dict.fromkeys([(item.variable_id) for item in CnVariables.objects.filter(variable_code__in=variables).order_by('variable_code')]))

    common_stations = []
    if exclude == True:
        for station in stations_qs:
            if station.station_variables_id:
                station_variables = station.station_variables_id.split("/")
                station_variables = list(filter(None, station_variables))
                
                flag = False
                for variable in variables_ids:
                    if str(variable) not in station_variables:
                        flag = True
                if flag == False:
                    common_stations.append(station.station_id)

        return common_stations

    if exclude == False:
        for station in stations_qs:
            if station.station_variables_id:
                station_variables = station.station_variables_id.split("/")
                station_variables = list(filter(None, station_variables))

                for variable in variables_ids:
                    if str(variable) in station_variables:
                        common_stations.append(station.station_id)

        common_stations = list(dict.fromkeys(common_stations))       
        return common_stations



def metadata(request):
    if request.path_info == "/variables-metadata/":
        json_data = serializers.serialize('json', CnVariables.objects.all())
        context = {
            'variables_list':SafeString(json_data),
        }
        return render(request, 'variables-metadata.html', context)
    elif request.path_info == "/stations-metadata/":
        json_data = serializers.serialize('json', CnStations.objects.all())
        context = {
            'stations_list':SafeString(json_data),
        }
        return render(request, 'stations-metadata.html', context)
    elif request.path_info == "/networks-metadata/":
        json_data = serializers.serialize('json', CnNetwork.objects.all())
        context = {
            'networks_list':SafeString(json_data),
        }
        return render(request, 'networks-metadata.html', context)

def About(request):
    return render(request, 'about.html',)

def ClimateDataApp(request):
    if request.method == 'GET':
        if is_valid_queryparam(request.GET.get('csrfmiddlewaretoken')):
            if is_valid_queryparam(request.GET.get('station_name')) and is_valid_queryparam(request.GET.get('date_range')) and is_valid_queryparam(request.GET.get('variables')):
                parameter = request.GET.getlist('variables')
                if parameter is not None:
                    cn_variables = CnVariables.objects.filter(variable_code__in=parameter)
                    cn_variables_ids = []
                    for item in cn_variables:
                        cn_variables_ids.append(int(item.variable_id))

                parameter = request.GET.getlist('station_name')
                if parameter is not None:
                    stations = [int(station_name) for station_name in parameter]
                    items = CnStations.objects.filter(station_id__in=stations)
                    station_ids = items.values_list('station_id', flat = True)
                    station_ids = [int(station_id) for station_id in station_ids]

                parameter = request.GET.get('date_range')
                if parameter is not None:
                    parameter = parameter.split(" - ")
                    time_range = parameter

            form = StationsForm(request.GET)

            #Procesamos la descarga si existe una petición de la misma
            if "download" in request.GET:
                #Creamos el CSV con la leyenda relativa a los parametros de descarga seleccionados.
                #Los archivos CSV se borran al finalizar el proceso, su nombre contiene la fecha y hora actuales con una precision de microsegundos para evitar un hipotetico duplicado
                with open('/tmp/Stations_info_' + str(datetime.now())[:-2] + '.csv', encoding='utf-8', mode='w',) as csv_file_legend:
                    writer = csv.writer(csv_file_legend, dialect=csv.excel, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                    #Stations Info
                    queryset = items
                    writer.writerow(['STATIONS INFORMATION'])
                    writer.writerow(['Station ID', 'Station name', 'Station Code', 'Municipality', 'Province', 'Elevation'])
                    for item in queryset:
                        writer.writerow([item.station_id, item.station_name, item.station_code, capwords(item.munic_name), item.province, item.elev])

                    #Variables Info
                    queryset = CnVariables.objects.filter(variable_id__in=cn_variables_ids)
                    writer.writerow([''])
                    writer.writerow(['VARIABLES INFORMATION'])
                    writer.writerow(['Variable ID', 'Variable name', 'Variable Code', 'Variable units', 'Variable Type',])
                    for item in queryset:
                        writer.writerow([item.variable_id, item.variable_name, item.variable_code, item.variable_units, item.variable_type])

                #Repetimos la operacion anterior escribiendo esta vez los datos solicitados.
                with open('/tmp/Stations_data' + str(datetime.now())[:-2] + '.csv', 'w', encoding='utf-8') as csv_file_data:
                    writer = csv.writer(csv_file_data, dialect=csv.excel, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(['Station ID', 'Variable', 'Time', 'Value'])
                    queryset = CnDatos.objects.filter(station_id__in=station_ids).filter(time__range=[time_range[0], time_range[1]]).filter(variable_id__in=cn_variables_ids)
                    for item in queryset:
                        if item.value != None:
                            writer.writerow([item.station_id, item.variable_id, item.time, round(item.value, 2)])
                        else:
                            writer.writerow([item.station_id, item.variable_id, item.time, item.value])

                buff = NamedTemporaryFile(suffix='.zip')
                with zipfile.ZipFile(buff, "w") as zip_file:
                    zip_file.write(csv_file_legend.name, 'Legend.csv')
                    zip_file.write(csv_file_data.name, 'Stations_data.csv')
                    zip_file.write('static/files/readme.txt', 'readme.txt')
                    zip_file.close()
                    response = HttpResponse(open(buff.name, 'rb'), content_type='application/zip')
                    response['Content-Disposition'] = 'attachment; filename=cli_data_sierranevada.zip'
                    os.remove(csv_file_legend.name)
                    os.remove(csv_file_data.name)
                    return response
            else:
                items = CnStations.objects.all()
                form = StationsForm()
        else:
            items = CnStations.objects.all()
            form = StationsForm()

        json_networks = serializers.serialize('geojson', CnNetwork.objects.all(), fields=('pk', 'network_name'))
        stations = CnStations.objects.filter(station_variables_id__isnull=False)
        json_stations = serializers.serialize('geojson', stations, geometry_field='geom_4326', fields=('geom_4326','station_id','station_code','station_name','station_type','station_variables_id','cn_network_id','munic_name','elev','pk'))
        
        return render(request, 'stations.html', {'form': form, 'stations': json_stations, 'networks': json_networks,},)

class StationsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        variable_type = self.forwarded.get('variable_type', None)
        variables = self.forwarded.get('variables', None)
        altitudes = self.forwarded.get('altitude', None)
        
        if altitudes:
            altitudes = altitudes.split(';')
            min_altitude, max_altitude = altitudes[0], altitudes[1]
        else:
            min_altitude, max_altitude = '0', '3999'

        if variables:
            common_stations = get_common_stations(variables, variable_type, False)
            qs = CnStations.objects.filter(station_id__in=common_stations).filter(elev__range=(min_altitude, max_altitude)).filter(station_variables_id__isnull=False).order_by('munic_name')
        else:
            qs = CnStations.objects.all().filter(elev__range=(min_altitude, max_altitude)).filter(station_variables_id__isnull=False).order_by('munic_name')

        if self.q:
            words = self.q.split(' ')
            for word in words:
                qs = qs.filter(munic_name__istartswith=word).order_by('munic_name') | qs.filter(station_code__istartswith=word)
        return qs

class VariablesAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        stations = self.forwarded.get('station_name', None)
        variable_type = self.forwarded.get('variable_type', None)
        altitude = self.forwarded.get('altitude', None)

        if altitude:
            altitude = altitude.split(';')
        else:
            altitude = ['0', '3399']

        if variable_type and not stations :
            qs = CnVariables.objects.filter(variable_type=variable_type).order_by('variable_name')
        elif stations and not variable_type:
            common_variables = get_common_variables(stations, False)
            qs = CnVariables.objects.filter(variable_id__in=common_variables).order_by('variable_name')
        elif variable_type and stations:
            common_variables = get_common_variables(stations, False)
            qs = CnVariables.objects.filter(variable_type=variable_type).filter(variable_id__in=common_variables).order_by('variable_name')
        else:
            qs = CnVariables.objects.all().order_by('variable_name')
        if self.q:
            qs = qs.filter(variable_name__istartswith=self.q).order_by('variable_name')
        return qs

class VariableTypeAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        variables = self.forwarded.get('variables', None)
        variable_type_choices = list(dict.fromkeys([(item.variable_type) for item in CnVariables.objects.filter(variable_type__isnull=False).order_by('variable_type')]))
        return variable_type_choices

class StationsLeafletAutocomplete(autocomplete.Select2ListView):
    def get_list(self):

        getall = self.forwarded.get('getall', None)

        if getall: 
            stations_list = list(dict.fromkeys([(str(item.station_id)) for item in CnStations.objects.filter(station_variables_id__isnull=False)]))
            return stations_list
        else:

            variable_type = self.forwarded.get('variable_type', None)
            variables = self.forwarded.get('variables', None)
            min_altitude = self.forwarded.get('min_altitude', None)
            max_altitude = self.forwarded.get('max_altitude', None)
            station_type = self.forwarded.get('station_type', None)

            station_types = []
            if station_type[0] == True:
                station_types.append('Station')
            if station_type[1] == True:
                station_types.append('Sensor')  

            if not variables:
                qs = CnStations.objects.filter(station_type__in=station_types).filter(elev__range=(min_altitude, max_altitude)).filter(station_variables_id__isnull=False).order_by('munic_name')
            else:
                common_stations = get_common_stations(variables, variable_type, False)
                qs = CnStations.objects.filter(station_type__in=station_types).filter(station_id__in=common_stations).filter(elev__range=(min_altitude, max_altitude)).filter(station_variables_id__isnull=False).order_by('munic_name')

            if qs.exists():
                stations_list = list(dict.fromkeys([(str(item.station_id)) for item in qs.order_by('munic_name')]))
                return stations_list
            else:
                return CnStations.objects.none()