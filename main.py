from amadeus_client import search_flights
from score import apply_score
from database import create_table, upsert_flight

create_table()

DEPARTURE_DATE = "2026-03-13"
RETURN_DATE = "2026-04-01"
ITINEARRY = ["OPO", "RIO"]

flights = search_flights(
    origin=ITINEARRY[0],
    destination=ITINEARRY[1],
    departure_date=DEPARTURE_DATE,
    return_date=RETURN_DATE,
    adults=2,
    children=0,
    infants=1
)

if not flights:
    print("Nenhum voo encontrado.")
    exit()

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

scored_flights = apply_score(
    filtered_flights,
    profile_name="cheap_only"
)

for i, item in enumerate(scored_flights[:10], start=1):
    flight = item["flight"]

    print(f"\n🥇 RANK {i}")
    print("Score:", item["score"])
    print("Preço:", item["price"], flight["price"]["currency"])
    print("Paradas totais:", item["stops"])
    print("Duração total (min):", item["duration"])
    print("Companhia(s):", flight["validatingAirlineCodes"])

    for idx, itinerary in enumerate(flight["itineraries"]):
        tipo = "IDA" if idx == 0 else "VOLTA"
        segments = itinerary["segments"]

        print(f"\n  🧭 {tipo}")
        print("  Duração:", itinerary["duration"])
        print("  Paradas:", len(segments) - 1)

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

    upsert_flight({
        "route": f"{ITINEARRY[0]}-{ITINEARRY[1]}",
        "departure_date": DEPARTURE_DATE,
        "return_date": RETURN_DATE,
        "price_current": item["price"],
        "airline": ",".join(flight["validatingAirlineCodes"]),
        "stops": item["stops"],
        "profile": item["profile"]
    })