from time_convert import duration_to_minutes

USER_PROFILES = {
    "cost_benefit": {
        "price": 0.5,
        "stops": 0.3,
        "duration": 0.2,
        "max_stops": 1
    },
    "cheap_only": {
        "price": 0.8,
        "stops": 0.1,
        "duration": 0.1,
        "max_stops": 3
    },
    "direct_priority": {
        "price": 0.3,
        "stops": 0.5,
        "duration": 0.2,
        "max_stops": 0
    }
}


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


def apply_score(filtered_flights, profile_name="cost_benefit"):
    profile = USER_PROFILES[profile_name]

    max_price, max_duration, max_stops = gather_max_values(filtered_flights)

    scored_flights = []

    for flight in filtered_flights:
        price = float(flight["price"]["total"])

        total_minutes = 0
        total_stops = 0

        for itinerary in flight["itineraries"]:
            total_minutes += duration_to_minutes(itinerary["duration"])
            total_stops += len(itinerary["segments"]) - 1

        # regra dura (ex: voo direto)
        if total_stops > profile["max_stops"]:
            continue

        price_score = price / max_price
        duration_score = total_minutes / max_duration
        stops_score = total_stops / max_stops if max_stops else 0

        score = (
            price_score * profile["price"] +
            stops_score * profile["stops"] +
            duration_score * profile["duration"]
        )

        scored_flights.append({
            "flight": flight,
            "score": round(score, 3),
            "price": price,
            "duration": total_minutes,
            "stops": total_stops,
            "profile": profile_name
        })

    scored_flights.sort(key=lambda x: x["score"])
    return scored_flights
