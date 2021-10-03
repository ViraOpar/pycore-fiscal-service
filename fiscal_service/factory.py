from importlib import import_module
from fiscal_service.abstract_source import AbstractSource


def get_source(country_code: str) -> AbstractSource:
    module = import_module(f'fiscal_service.countries.{country_code}')
    return module.Source()
