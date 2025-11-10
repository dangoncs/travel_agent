import os
import requests
from typing import Optional
from google import adk


def search_google_flights(
    *,
    origin: str,
    destination: str,
    departure_date: str,
    return_date: Optional[str] = None,
    adults: int = 1,
    tool_context=None,
):
    """
    Search for flights using Google Flights API via SerpAPI.

    Args:
        origin: Origin airport code (e.g., 'JFK', 'LAX')
        destination: Destination airport code (e.g., 'LHR', 'CDG')
        departure_date: Departure date in YYYY-MM-DD format
        return_date: Return date in YYYY-MM-DD format (optional, for round trips)
        adults: Number of adult passengers (default: 1)

    Returns:
        Flight search results from Google Flights
    """
    # Note: You need to set SERPAPI_KEY environment variable
    api_key = os.environ.get("SERPAPI_KEY", "")

    if not api_key:
        return {
            "error": "SERPAPI_KEY not set. Please set your SerpAPI key as an environment variable.",
            "instructions": "Get your API key from https://serpapi.com/",
        }

    params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date": departure_date,
        "adults": adults,
        "currency": "USD",
        "hl": "en",
        "api_key": api_key,
    }

    if return_date:
        params["return_date"] = return_date
        params["type"] = "2"  # Round trip
    else:
        params["type"] = "1"  # One way

    try:
        response = requests.get("https://serpapi.com/search", params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Extract relevant flight information
        if "best_flights" in data:
            flights = data.get("best_flights", [])[:5]  # Get top 5 flights
            result = {
                "flights": flights,
                "search_params": {
                    "origin": origin,
                    "destination": destination,
                    "departure_date": departure_date,
                    "return_date": return_date,
                },
            }
            return result
        else:
            return {"message": "No flights found", "raw_response": data}
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch flight data: {str(e)}"}


flight_agent = adk.Agent(
    name="FlightFinder",
    model="gemini-2.5-pro",
    tools=[search_google_flights],
    description="Suggests flight options for a destination using Google Flights API.",
    instruction=(
        "Given a destination, travel dates, and budget, use the search_google_flights tool to find real flight options. "
        "Call the tool with appropriate airport codes, dates, and passenger count. "
        "Analyze the results and suggest 1-2 best flight options that fit within the budget. "
        "Include airline name, price, departure time, arrival time, and any layover information. "
        "If the API key is not set or there's an error, provide helpful instructions to the user."
    ),
)
