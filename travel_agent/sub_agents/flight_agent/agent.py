import os
import requests
from typing import Optional
from datetime import datetime, timedelta
from google import adk


def validate_and_fix_date(date_str: str) -> tuple[str, str]:
    """
    Validate a date string and ensure it's in the future.
    If the date is in the past, adjust it to the nearest future occurrence.
    
    Args:
        date_str: Date in YYYY-MM-DD format
        
    Returns:
        Tuple of (validated_date, warning_message)
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.now()
        
        # If date is in the past, find the next occurrence
        if date_obj < today:
            # Calculate how many years to add to make it future
            years_diff = today.year - date_obj.year
            future_date = date_obj.replace(year=today.year + 1)
            
            # If the month/day already passed this year, use next year
            # Otherwise, we can use this year
            this_year_date = date_obj.replace(year=today.year)
            if this_year_date > today:
                future_date = this_year_date
                
            warning = f"Note: {date_str} is in the past. Using {future_date.strftime('%Y-%m-%d')} instead."
            return future_date.strftime("%Y-%m-%d"), warning
        
        return date_str, ""
    except ValueError:
        return date_str, ""


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
    # Validate and fix dates if they're in the past
    departure_date, departure_warning = validate_and_fix_date(departure_date)
    warnings = []
    if departure_warning:
        warnings.append(departure_warning)
    
    if return_date:
        return_date, return_warning = validate_and_fix_date(return_date)
        if return_warning:
            warnings.append(return_warning)
    
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

    # Add return_date if provided (API auto-detects round-trip)
    # Note: Don't use 'type' parameter - it causes confusion in the API
    if return_date:
        params["return_date"] = return_date

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
            if warnings:
                result["warnings"] = warnings
            return result
        else:
            response_data = {"message": "No flights found", "raw_response": data}
            if warnings:
                response_data["warnings"] = warnings
            return response_data
    except requests.exceptions.RequestException as e:
        error_response = {"error": f"Failed to fetch flight data: {str(e)}"}
        if warnings:
            error_response["warnings"] = warnings
        return error_response


flight_agent = adk.Agent(
    name="FlightFinder",
    model="gemini-2.5-flash",
    tools=[search_google_flights],
    description="Suggests flight options for a destination using Google Flights API.",
    instruction=(
        "Given a destination, travel dates, and budget, use the search_google_flights tool to find real flight options. "
        "IMPORTANT: When the user provides dates without a year (e.g., 'July 5th'), always interpret them as dates in the current or next year that haven't passed yet. "
        "If a date would be in the past, assume the user means next year. "
        "Call the tool with appropriate airport codes, dates in YYYY-MM-DD format, and passenger count. "
        "The tool will automatically adjust past dates to the next year and warn you. Pay attention to any warnings in the response. "
        "Analyze the results and suggest 1-2 best flight options that fit within the budget. "
        "Include airline name, price, departure time, arrival time, and any layover information. "
        "If the API key is not set or there's an error, provide helpful instructions to the user."
    ),
)
