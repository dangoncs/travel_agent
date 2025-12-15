import os
import requests
from google import adk


def search_google_hotels(
    *,
    location: str,
    check_in_date: str,
    check_out_date: str,
    adults: int = 1,
    currency: str = "USD",
    tool_context=None,
):
    """
    Search for hotels using Google Hotels API via SerpAPI.

    Args:
        location: City or area to search for hotels (e.g., 'Paris, France', 'New York, NY')
        check_in_date: Check-in date in YYYY-MM-DD format
        check_out_date: Check-out date in YYYY-MM-DD format
        adults: Number of adults (default: 1)
        currency: Currency code (default: 'USD')

    Returns:
        Hotel search results from Google Hotels
    """
    # Note: You need to set SERPAPI_KEY environment variable
    api_key = os.environ.get("SERPAPI_KEY", "")

    if not api_key:
        return {
            "error": "SERPAPI_KEY not set. Please set your SerpAPI key as an environment variable.",
            "instructions": "Get your API key from https://serpapi.com/",
        }

    params = {
        "engine": "google_hotels",
        "q": location,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "adults": adults,
        "currency": currency,
        "hl": "en",
        "api_key": api_key,
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Extract relevant hotel information
        if "properties" in data:
            hotels = data.get("properties", [])[:10]  # Get top 10 hotels
            result = {
                "hotels": hotels,
                "search_params": {
                    "location": location,
                    "check_in_date": check_in_date,
                    "check_out_date": check_out_date,
                    "adults": adults,
                },
            }
            return result
        else:
            return {"message": "No hotels found", "raw_response": data}
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch hotel data: {str(e)}"}


hotel_agent = adk.Agent(
    name="HotelRecommender",
    model="gemini-2.5-pro",
    tools=[search_google_hotels],
    description="Suggests hotel or stay options for a destination using Google Hotels API.",
    instruction=(
        "Given a destination, travel dates, and budget, use the search_google_hotels tool to find real hotel options. "
        "Call the tool with the location, check-in/check-out dates, and number of guests. "
        "Analyze the results and suggest 2-3 best hotel options that fit within the budget. "
        "Include hotel name, price per night, total price, rating, location/address, and key amenities. "
        "If the API key is not set or there's an error, provide helpful instructions to the user."
    ),
)
