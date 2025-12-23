'''
Helpers to fetch and format country data from the REST Countries API.
'''

import requests

URL = "https://restcountries.com/v3.1/name/{name}?fullText=true&fields={fields}"


def get_country_info(name: str, fields: str) -> dict:
    '''
    Fetch country data from the REST Countries API.

    Args:
        name (str): The full name of the country.
        fields (str): Comma-separated fields to retrieve.

    Returns:
        dict: Country data if found, else None. Contains:
            - 'area' (float): Area of the country in square kilometers.
            - 'capital' (list): List of capital cities.
            - 'currencies' (dict): Currencies used in the country.
            - 'flags' (dict): URLs to flag images and alt text.
            - 'languages' (dict): Languages spoken in the country.
            - 'timezones' (list): List of timezones in the country.

    '''
    response = requests.get(URL.format(name=name, fields=fields), timeout=10)
    if response.status_code == 200:
        return response.json()[0]
    return None


def format_country_info(data: dict) -> dict:
    '''
    Format country data into a readable strings.

    Args:
        data (dict): Country data dictionary.

    Returns:
        dict: Formatted strings with country information.
    '''
    info_lines = {}

    if 'area' in data:
        info_lines['area'] = f"Area: {data['area']} sq km"

    if 'capital' in data:
        info_lines['capital'] = f"Capital: {', '.join(data['capital'])}"

    if 'languages' in data:
        languages = ', '.join(data['languages'].values())
        info_lines['languages'] = f"Languages: {languages}"

    if 'currencies' in data:
        currencies = []
        for currency in data['currencies'].values():
            currencies.append(f"{currency['name']} ({currency['symbol']})")
        info_lines['currencies'] = f"Currencies: {', '.join(currencies)}"

    if 'timezones' in data:
        info_lines['timezones'] = f"Timezones: {', '.join(data['timezones'])}"

    if 'flags' in data:
        info_lines['flag_png'] = data['flags'].get('png', 'N/A')
        info_lines['flag_alt'] = data['flags'].get('alt', 'N/A')

    if len(info_lines) == 0:
        return {"No data available."}
    return info_lines


def main() -> None:
    '''
    Example usage of the country info functions.
    '''
    country_name = "China"
    fields = "capital,area,languages,currencies,flags,timezones"
    data = get_country_info(country_name, fields)
    formatted_info = format_country_info(data)
    for line, value in formatted_info.items():
        print(f"{line}: {value}")


if __name__ == "__main__":
    main()
