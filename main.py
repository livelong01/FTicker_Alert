from amadeus_client import search_flights

flights = search_flights(
    origin="OPO",
    destination="RIO",
    departure_date="2026-03-14",
    return_date="2026-04-01",
    adults=1
)

if not flights:
    print("Nenhum voo encontrado.")
    exit()

ALLOWED_AIRLINES = {"TP", "AD", "IB"}  # TAP Air Portugal, Azul, Iberia , 

filtered_flights = [
    f for f in flights
    if any(code in ALLOWED_AIRLINES for code in f["validatingAirlineCodes"])
]

for i, flight in enumerate(flights[:5], start=1):
    price = flight["price"]["total"]
    currency = flight["price"]["currency"]
    airlines = flight["validatingAirlineCodes"]

    itinerary = flight["itineraries"][0]
    segments = itinerary["segments"]
    stops = len(segments) - 1
    duration = itinerary["duration"]

    print(f"\n✈️ VOO {i}")
    print("Companhia(s):", airlines)
    print("Preço:", price, currency)
    print("Duração:", duration)
    print("Paradas:", stops)

    for seg in segments:
        print(
            f"  {seg['departure']['iataCode']} → "
            f"{seg['arrival']['iataCode']} | "
            f"{seg['carrierCode']}{seg['number']}"
        )
