#!/usr/bin/python

filter_station_chars_to_replace = "$$_id_station_$$"
filter_sampling_chars_to_replace = "$$_sampling_$$"
filter_data_type_chars_to_replace = "$$_data_type_$$"

filter_station = "VALUES ?station {<http://meta.icos-cp.eu/resources/stations/AS_" \
                 + filter_station_chars_to_replace \
                 + ">}?dobj cpmeta:wasAcquiredBy/prov:wasAssociatedWith ?station ."

filter_sampling = "?dobj cpmeta:wasAcquiredBy / cpmeta:hasSamplingHeight ?samplingHeight " \
                  ".FILTER( ?samplingHeight = '" + filter_sampling_chars_to_replace + "'^^xsd:float )"

filter_data_type_ch4 = "<http://meta.icos-cp.eu/resources/cpmeta/atcCh4L2DataObject>"
filter_data_type_co = "<http://meta.icos-cp.eu/resources/cpmeta/atcCoL2DataObject>"
filter_data_type_co2 = "<http://meta.icos-cp.eu/resources/cpmeta/atcCo2L2DataObject>"
filter_data_type_mto = "<http://meta.icos-cp.eu/resources/cpmeta/atcMtoL2DataObject>"
filter_data_type_c14 = "<http://meta.icos-cp.eu/resources/cpmeta/atcC14L2DataObject>"

filter_data_type_all = "{0}{1}{2}{3}{4}".format(filter_data_type_ch4, filter_data_type_co, filter_data_type_co2,
                                                filter_data_type_mto, filter_data_type_c14)

query_sparql = """
        prefix cpmeta: <http://meta.icos-cp.eu/ontologies/cpmeta/>
        prefix prov: <http://www.w3.org/ns/prov#>
        select ?dobj ?spec ?fileName ?size ?submTime ?timeStart ?timeEnd
        where {
            VALUES ?spec {
    """ + filter_data_type_chars_to_replace + """
            }?dobj cpmeta:hasObjectSpec ?spec .
    """ + filter_station_chars_to_replace + """
            ?dobj cpmeta:hasSizeInBytes ?size .
            ?dobj cpmeta:hasName ?fileName .
            ?dobj cpmeta:wasSubmittedBy/prov:endedAtTime ?submTime .
            ?dobj cpmeta:hasStartTime | (cpmeta:wasAcquiredBy / prov:startedAtTime) ?timeStart .
            ?dobj cpmeta:hasEndTime | (cpmeta:wasAcquiredBy / prov:endedAtTime) ?timeEnd .
                FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?dobj}
    """ + filter_sampling_chars_to_replace + """            
    }
    order by desc(?submTime)
    """


def get_query_dataset_full():
    return query_sparql\
        .replace(filter_station_chars_to_replace, '')\
        .replace(filter_sampling_chars_to_replace, '')\
        .replace(filter_data_type_chars_to_replace, filter_data_type_all)


def get_url_download_dobj(id_dobj):
    return 'https://data.icos-cp.eu/licence_accept?ids=%5B%22' + id_dobj + '%22%5D'
