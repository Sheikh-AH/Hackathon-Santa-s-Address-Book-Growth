import requests
from pprint import pprint

URL = "https://restcountries.com/v3.1/name/{name}?fullText=true&fields={fields}"


def get_data_of_country(name, fields) -> dict:
    response = requests.get(URL.format(name=name, fields=fields))
    if response.status_code == 200:
        return response.json()
    else:
        return None


if __name__ == "__main__":
    country_name = "China"
    fields = "capital,area,languages,currencies"
    data = get_data_of_country(country_name, fields)

    if data:
        for item in data:
            pprint(item)
    else:
        print(f"Could not retrieve data for {country_name}.")
