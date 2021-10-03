from bs4 import BeautifulSoup

from fiscal_service import AbstractSource


class Source(AbstractSource):
    """
    Switzerland source.
    """

    async def gather(self, number):
        """
        Gather by fiscal number.
        """
        response = await self.fetch_json(f'https://www.uid.admin.ch/Detail.aspx?uid_id=CHE-{number}')
        soup = BeautifulSoup(response.body)

        tags = soup.find(id='cphContent_sectionCoreProperties')
        if tags:
            fieldsets = tags.find_all('fieldset')

            vat_data = fieldsets[5].div.find_all('div')[0].div.find_all(class_='col-sm-4')
            is_valid = vat_data[0].div.text == 'Aktiv'

            address_data = fieldsets[1].find_all('div', class_='col-sm-10')
            city = address_data[-1].text.strip().split(' ')
            city_name = city[1]
            postal_code = city[0]
            address = address_data[5].text.strip()
            if not address:
                address = address_data[4].text.strip()

            name = address_data[0].div.text

            return {
                'address': address,
                'city': city_name,
                'postal_code': postal_code,
                'name': name,
                'country': 'Switzerland',
                'valid': is_valid,
            }
