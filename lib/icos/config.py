#!/usr/bin/python
import json
import pathlib
from dataclasses import dataclass

import dacite


@dataclass
class Configuration:
    path_datacube: pathlib.Path
    filename_datacube: str
    data_type_dictionary: dict
    path_output: pathlib.Path


def get_config():
    with open('/etc/cds/db-dataset/config.json') as f:
        raw_cfg = json.load(f)

    converters = {
        pathlib.Path: pathlib.Path,
    }

    return dacite.from_dict(
        data_class=Configuration, data=raw_cfg,
        config=dacite.Config(type_hooks=converters),
    )
