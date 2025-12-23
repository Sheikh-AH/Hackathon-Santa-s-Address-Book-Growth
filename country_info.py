'''
Helpers to fetch and format country data from the REST Countries API.

Resources:
- REST Countries API: https://restcountries.com/
- fields documentation: https://gitlab.com/restcountries/restcountries/-/blob/master/FIELDS.md
'''
import json
import requests

URL = "https://restcountries.com/v3.1/name/{name}?fullText=true&fields={fields}"


def get_cached_country_info(filepath: str) -> dict:
    '''
    Retrieve cached country data from a local file.

    Args:
        name (str): The name of the country.
        filepath (str): Path to the cached file.

    Returns:
        dict: Cached country data if found, else None.
    '''
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def get_country_info(name: str, fields: str) -> dict:
    '''
    Fetch country data from the REST Countries API.

    Args:
        name (str): The full name of the country.
        fields (str): Comma-separated fields to retrieve.

    Returns:
        dict: Country data if found, else None. 
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


def cache_country_info(filepath: str, data: dict) -> None:
    '''
    Cache country data to a local file.

    Args:
        filepath (str): Path to the cached file.
        data (dict): Country data to cache.
    '''
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def country_info_main(country_name: str) -> dict:
    '''
    main function to handle get-format-cache process.

    Args:
        country_name (str): The name of the country.

    Returns:
        dict: Formatted country information.
    '''
    filename = f"{country_name.replace(' ', '_').lower()}_info.json"
    filepath = f"resources/country_info/{filename}"
    data = get_cached_country_info(filepath)

    if data is None:
        fields = "capital,area,languages,currencies,flags,timezones"
        data = get_country_info(country_name, fields)
        cache_country_info(filepath, data)
        print(f"{country_name}fetched from API and cached.")

    formatted_info = format_country_info(data)

    return formatted_info


if __name__ == "__main__":
    country_info = country_info_main("China")
    for line, value in country_info.items():
        print(f"{line}: {value}")
