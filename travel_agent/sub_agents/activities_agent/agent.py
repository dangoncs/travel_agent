import os
import requests
from google import adk


def search_google_maps_places(
    *,
    location: str,
    query: str = "tourist attractions",
    radius: int = 5000,
    tool_context=None,
):
    """
    Search for places and activities using Google Maps Places API.
    
    Args:
        location: Location to search around (e.g., 'Paris, France', 'New York, NY')
        query: Type of places to search for (e.g., 'tourist attractions', 'museums', 'restaurants')
        radius: Search radius in meters (default: 5000)
    
    Returns:
        Places and activities from Google Maps
    """
    # Note: You need to set GOOGLE_MAPS_API_KEY environment variable
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY", "")
    
    if not api_key:
        return {
            "error": "GOOGLE_MAPS_API_KEY not set. Please set your Google Maps API key as an environment variable.",
            "instructions": "Get your API key from https://console.cloud.google.com/ and enable Places API"
        }
    
    # First, geocode the location to get coordinates
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    geocode_params = {
        "address": location,
        "key": api_key
    }
    
    try:
        geocode_response = requests.get(geocode_url, params=geocode_params, timeout=10)
        geocode_response.raise_for_status()
        geocode_data = geocode_response.json()
        
        if geocode_data.get("status") != "OK" or not geocode_data.get("results"):
            return {
                "error": f"Could not geocode location: {location}",
                "details": geocode_data.get("status")
            }
        
        coordinates = geocode_data["results"][0]["geometry"]["location"]
        lat = coordinates["lat"]
        lng = coordinates["lng"]
        
        # Now search for places
        places_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        places_params = {
            "query": f"{query} in {location}",
            "location": f"{lat},{lng}",
            "radius": radius,
            "key": api_key
        }
        
        places_response = requests.get(places_url, params=places_params, timeout=10)
        places_response.raise_for_status()
        places_data = places_response.json()
        
        if places_data.get("status") == "OK":
            places = places_data.get("results", [])[:10]  # Get top 10 places
            
            # Get additional details for each place
            detailed_places = []
            for place in places:
                place_id = place.get("place_id")
                details_url = "https://maps.googleapis.com/maps/api/place/details/json"
                details_params = {
                    "place_id": place_id,
                    "fields": "name,rating,formatted_address,opening_hours,price_level,reviews,types,website",
                    "key": api_key
                }
                
                details_response = requests.get(details_url, params=details_params, timeout=10)
                if details_response.status_code == 200:
                    details_data = details_response.json()
                    if details_data.get("status") == "OK":
                        detailed_places.append(details_data.get("result", {}))
            
            return {
                "places": detailed_places if detailed_places else places,
                "search_params": {
                    "location": location,
                    "query": query,
                    "coordinates": {"lat": lat, "lng": lng}
                }
            }
        else:
            return {
                "message": "No places found",
                "status": places_data.get("status"),
                "raw_response": places_data
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch places data: {str(e)}"
        }


activities_agent = adk.Agent(
    name="ActivitiesAgent",
    model="gemini-2.5-flash",
    tools=[search_google_maps_places],
    description="Suggests interesting activities for the user at a destination using Google Maps API.",
    instruction=(
        "Given a destination, dates, and budget, use the search_google_maps_places tool to find real tourist attractions and activities. "
        "Call the tool with the destination location and relevant query terms (e.g., 'tourist attractions', 'museums', 'restaurants', 'parks'). "
        "Analyze the results and suggest 2-3 most engaging activities based on ratings, reviews, and relevance. "
        "For each activity, provide: name, description, address, rating, price level (if available), and what makes it special. "
        "Consider the user's budget and suggest activities that fit. "
        "If the API key is not set or there's an error, provide helpful instructions to the user. "
        "Respond in plain English (not JSON). Keep it concise and well-formatted."
    ),
)
