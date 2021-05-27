import hug

from lib.icos.utils import icos_data


@hug.get('/data')
def get_icos_data(**kwargs):
    icos_data.get_data(**kwargs)
