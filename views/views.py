import json
from abc import ABC
from tornado.web import RequestHandler

from fiscal_service import factory


class BaseView(RequestHandler, ABC):
    """
    Base view for application.
    """

    def set_default_headers(self):
        """
        Set the default response header to be JSON.
        """
        self.set_header('Content-Type', 'application/json; charset="utf-8"')

    def send_response(self, data, status=200):
        """
        Construct and send a JSON response with appropriate status code.
        """
        self.set_status(status)
        self.write(json.dumps(data))


class FiscalServiceView(BaseView, ABC):
    """
    View for getting legal data by fiscal number.
    """

    async def get(self, fiscal_number):
        try:
            country_code = fiscal_number[0:2].lower()
            number = fiscal_number[2:]

            module = factory.get_source(country_code)
            response = await module.gather(number)
            if not response:
                response = {
                    'error': 'Invalid fiscal number.'
                }
        except ModuleNotFoundError:
            response = {
                'error': 'Country code not found.'
            }

        self.send_response(response)
