from time_convert import duration_to_minutes

WEIGHT_PRICE = 0.6
WEIGHT_STOPS = 0.2
WEIGHT_DURATION = 0.2


def gather_max_values(flights):
    prices = []
    durations = []
    stops_list = []

    for flight in flights:
        prices.append(float(flight["price"]["total"]))

        total_minutes = 0
        total_stops = 0

        for itinerary in flight["itineraries"]:
            total_minutes += duration_to_minutes(itinerary["duration"])
            total_stops += len(itinerary["segments"]) - 1

        durations.append(total_minutes)
        stops_list.append(total_stops)

    return (
        max(prices),
        max(durations),
        max(stops_list) if max(stops_list) > 0 else 1
    )


def calculate_score(price, duration, stops, max_price, max_duration, max_stops):
    price_score = price / max_price
    duration_score = duration / max_duration
    stops_score = stops / max_stops

    return (
        price_score * WEIGHT_PRICE +
        stops_score * WEIGHT_STOPS +
        duration_score * WEIGHT_DURATION
    )


def apply_score(filtered_flights):
    scored_flights = []

    max_price, max_duration, max_stops = gather_max_values(filtered_flights)

    for flight in filtered_flights:
        price = float(flight["price"]["total"])

        total_minutes = 0
        total_stops = 0

        for itinerary in flight["itineraries"]:
            total_minutes += duration_to_minutes(itinerary["duration"])
            total_stops += len(itinerary["segments"]) - 1

        score = calculate_score(
            price,
            total_minutes,
            total_stops,
            max_price,
            max_duration,
            max_stops
        )

        scored_flights.append({
            "flight": flight,
            "score": round(score, 3),
            "price": price,
            "duration": total_minutes,
            "stops": total_stops
        })

    # menor score = melhor voo
    scored_flights.sort(key=lambda x: x["score"])
    return scored_flights