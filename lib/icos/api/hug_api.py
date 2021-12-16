import hug

from icos.utils import icos_data


@hug.get('/api/data')
def get_icos_data(**kwargs):
    return icos_data.get_data(**kwargs)


@hug.get('/api/datacube')
def get_datacube():
    return icos_data.get_datacube()
