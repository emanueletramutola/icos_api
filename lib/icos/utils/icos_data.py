#!/usr/bin/python
import io
import os
import uuid
import zipfile
from contextlib import closing
from pathlib import Path

import pandas as pd
import requests
from icoscp.sparql.runsparql import RunSparql

import icos_query
import lib.icos.config as conf


def get_data(params):
    config = conf.get_config()

    check_datacube_exists()

    bb = pd.read_csv(config.path_datacube, dtype=str)

    cc = bb.query(get_filter(params))

    path_file = config.path_output / (str(uuid.uuid4()) + '.zip')

    with zipfile.ZipFile(path_file, 'w') as zf:
        for url in cc.Url.unique():
            r = requests.get(url)
            with closing(r), zipfile.ZipFile(io.BytesIO(r.content)) as archive:
                file = archive.infolist()[0]
                with archive.open(file, "r") as fo:
                    zf.writestr(file, fo.read())

    zf.close()

    return path_file


def get_filter(params):
    filter_year = ''
    filter_month = ''
    filter_day = ''
    filter_variable = ''
    filter_station_name = ''

    if 'year' in params.keys():
        filter_year = get_filter_by_field('Year', params['year'])

    if 'month' in params.keys():
        filter_month = get_filter_by_field('Month', params['month'])

    if 'day' in params.keys():
        filter_day = get_filter_by_field('Day', params['day'])

    if 'variable' in params.keys():
        filter_variable = get_filter_by_field('Data_type', params['variable'])

    if 'station_name' in params.keys():
        filter_station_name = get_filter_by_field('Station_name', params['station_name'])

    return '{0} & {1} & {2} & {3} & {4}'.format(filter_year,
                                                filter_month,
                                                filter_day,
                                                filter_variable,
                                                filter_station_name)


def get_filter_by_field(field, filter_list):
    filter_field = field + " in ("

    is_first_element = True
    for x in filter_list:
        if not is_first_element:
            filter_field += ","

        filter_field += "'" + x + "'"
        if is_first_element:
            is_first_element = False

    filter_field += ")"

    return filter_field


def build_datacube():
    config = conf.get_config()

    result = RunSparql(icos_query.get_query_dataset_full(), 'pandas').run()

    list_dobj = result.get('dobj').to_list()

    columns_to_export = ['Year', 'Month', 'Day', 'Site', 'Station_name', 'Latitude', 'Longitude', 'Data_type', 'Url']

    f = open(config.filename_datacube, "w")
    f.write(",".join(columns_to_export) + os.linesep)
    f.close()

    if len(list_dobj) > 0:
        for i in range(len(list_dobj)):
            list_latitude = []
            list_longitude = []
            list_station_name = []
            list_data_type = []
            list_url = []

            id_dobj_full = list_dobj[i]

            id_dobj = id_dobj_full[id_dobj_full.rindex("/") + 1:]

            url = icos_query.get_url_download_dobj(id_dobj)
            r = requests.get(url)

            with closing(r), zipfile.ZipFile(io.BytesIO(r.content)) as archive:
                file = archive.infolist()[0]
                with archive.open(file, "r") as fo:
                    csv = fo.read()
                    rows = csv.decode('UTF-8').split('\n')

                    latitude = [i for i in rows if i.startswith('# LATITUDE')][0].split(' ')[2].strip()
                    longitude = [i for i in rows if i.startswith('# LONGITUDE')][0].split(' ')[2].strip()
                    station_name = [i for i in rows if i.startswith('# STATION NAME')][0].split(':')[1].strip()
                    data_type = [i for i in rows if i.startswith('# FILE NAME')][0].split('.')[3].strip()

                    columns = rows[len(rows) - rows[::-1].index('#')].replace('#', '').split(';')
                    fo.seek(0)
                    data = pd.read_csv(fo, sep=';', comment='#', names=columns)

                    for j in range(len(data)):
                        list_latitude.append(latitude)
                        list_longitude.append(longitude)
                        list_station_name.append(station_name)
                        list_data_type.append(config.data_type_dictionary[data_type])
                        list_url.append(url)

                    data.insert(len(data.columns), "Latitude", list_latitude, True)
                    data.insert(len(data.columns), "Longitude", list_longitude, True)
                    data.insert(len(data.columns), "Station_name", list_station_name, True)
                    data.insert(len(data.columns), "Data_type", list_data_type, True)
                    data.insert(len(data.columns), "Url", list_url, True)

                    data.insert(len(data.columns), "Month_new", data['Month'].astype(str).str.zfill(2), True)
                    data.insert(len(data.columns), "Day_new", data['Day'].astype(str).str.zfill(2), True)

                    data.rename(columns={'Month': 'Month_old', 'Day': 'Day_old'}, inplace=True)
                    data.rename(columns={'Month_new': 'Month', 'Day_new': 'Day'}, inplace=True)

                    data[columns_to_export] \
                        .drop_duplicates() \
                        .to_csv('icos_datacube.csv', columns=columns_to_export, index=False, header=False, mode='a')


def check_datacube_exists():
    config = conf.get_config()

    if not Path(config.path_datacube).is_file():
        # the file does not exist. Proceed to create the datacube
        build_datacube()


def get_datacube():
    check_datacube_exists()

    return config.path_datacube
