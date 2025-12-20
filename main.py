from amadeus_client import search_flights
#import json

flights = search_flights(
    origin="OPO",
    destination="RIO",
    departure_date="2026-03-16",
    return_date="2026-04-01",
    adults=2,
    children=0,
    infants=1
)

if not flights:
    print("Nenhum voo encontrado.")
    exit()

"""
x = json.dumps(flights[0], indent=2)
#agora vou salvar esse json em um arquivo para analisar melhor
with open("flight_sample.json", "w") as f:
    f.write(x)
"""
# --------------- FILTERING ---------------
ALLOWED_AIRLINES = {"TP", "AD", "IB"}  # TAP Air Portugal, Azul, Iberia

MIN_STOPS = 0  # ex: direto
MAX_STOPS = 1  # ex: até 1 parada

filtered_flights = []

for flight in flights:
    if not any(a in ALLOWED_AIRLINES for a in flight["validatingAirlineCodes"]):
        continue

    itineraries = flight["itineraries"]
    valido = True

    for itinerary in itineraries:
        stops = len(itinerary["segments"]) - 1
        if not (MIN_STOPS <= stops <= MAX_STOPS):
            valido = False
            break

    if valido:
        filtered_flights.append(flight)
# ------------------------ ----------------

for i, flight in enumerate(filtered_flights[:3], start=1):
    price = flight["price"]["total"]
    currency = flight["price"]["currency"]
    airlines = flight["validatingAirlineCodes"]

    itineraries = flight["itineraries"]

    print(f"\n✈️ VOO {i}")
    print("Companhia(s):", airlines)
    print("Preço:", price, currency)

    for idx, itinerary in enumerate(itineraries):
        tipo = "IDA" if idx == 0 else "VOLTA"
        segments = itinerary["segments"]
        stops = len(segments) - 1
        duration = itinerary["duration"]

        print(f"\n  🧭 {tipo}")
        print("  Duração:", duration)
        print("  Paradas:", stops)

        for seg in segments:
            print(
                f"    {seg['departure']['iataCode']} → "
                f"{seg['arrival']['iataCode']} | "
                f"{seg['carrierCode']}{seg['number']}"
            )

    cabin = flight["travelerPricings"][0]["fareDetailsBySegment"][0]["cabin"]
    baggage = flight["travelerPricings"][0]["fareDetailsBySegment"][0] \
        .get("includedCheckedBags", {}) \
        .get("quantity", 0)

    print("\n  Cabine:", cabin)
    print("  Bagagem despachada incluída:", baggage)
