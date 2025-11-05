from google import adk

flight_agent = adk.Agent(
    name="FlightFinder",
    model="gemini-2.5-pro",
    description="Suggests flight options for a destination.",
    instruction=(
        "Given a destination, travel dates, and budget, suggest 1-2 realistic flight options. "
        "Include airline name, price, and departure time. Ensure flights fit within the budget."
    ),
)
