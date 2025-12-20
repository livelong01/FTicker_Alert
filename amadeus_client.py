from amadeus import Client, ResponseError
from config import AMADEUS_API_KEY, AMADEUS_API_SECRET

amadeus = Client(
    client_id=AMADEUS_API_KEY,
    client_secret=AMADEUS_API_SECRET
)

def search_flights(origin, destination, departure_date, return_date=None, adults=1):
    try:
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "adults": adults,
            "currencyCode": "BRL"
        }

        if return_date:
            params["returnDate"] = return_date

        response = amadeus.shopping.flight_offers_search.get(**params)
        return response.data

    except ResponseError as error:
        print(error)
        return None
