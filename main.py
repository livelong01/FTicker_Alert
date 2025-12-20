from amadeus_client import search_flights

flights = search_flights(
    origin="OPO",
    destination="RIO",
    departure_date="2026-03-14",
    return_date=None,
    adults=1
)

if flights:
    prices = [float(f["price"]["total"]) for f in flights]
    print("Preço atual mais barato:", min(prices), "BRL")
else:
    print("Nenhum voo encontrado.")
