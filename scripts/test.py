import requests

params = {
    "scientificName": "Sus scrofa",
    "country": "BR",
    "year": 2020,
    "limit": 1
}

res = requests.get("https://api.gbif.org/v1/occurrence/search", params=params)
print(res.status_code)
print(res.json())
