import hug

from lib.icos.utils import icos_data


@hug.get('/data')
def get_icos_data(**kwargs):
    return icos_data.get_data(**kwargs)


@hug.get('/datacube')
def get_datacube():
    return icos_data.get_datacube()
