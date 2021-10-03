from bs4 import BeautifulSoup

from fiscal_service import AbstractSource


class Source(AbstractSource):
    """
    Norway source.
    """

    async def gather(self, number):
        """
        Gather by fiscal number.
        """
        response = await self.fetch_json(f'https://w2.brreg.no/enhet/sok/detalj.jsp?orgnr={number}')
        soup = BeautifulSoup(response.body)

        page_content = soup.find(id='pagecontent')
        if page_content:
            fieldsets = page_content.find_all('div', class_='row')

            name = fieldsets[2].contents[3].get_text(strip=True)

            address_data = fieldsets[3].contents[3].contents[1].get_text(strip=True, separator='<br>').split('<br>')
            address = address_data[0]
            postal_code = address_data[1].split(' ')[0]
            city_name = address_data[1].split(' ')[1].title()

            return {
                'address': address,
                'city': city_name,
                'postal_code': postal_code,
                'name': name,
                'country': 'Norway',
                'valid': name and address,
            }
