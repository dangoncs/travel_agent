from google import adk

hotel_agent = adk.Agent(
    name="HotelRecommender",
    model="gemini-2.5-pro",
    description="Suggests hotel or stay options for a destination.",
    instruction=(
        "Given a destination, travel dates, and budget, suggest 2-3 hotel or stay options. "
        "Include hotel name, price per night, and location. Ensure suggestions are within budget."
    ),
)
