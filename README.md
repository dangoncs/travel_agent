# Travel Agent

This is an AI-powered travel planning assistant developed using Google ADK that coordinates specialized sub-agents for flights, hotels, and activities.

## Demo

https://github.com/user-attachments/assets/b33a9359-8730-4407-b406-314cb74d19c5

## Features

- **Flight Search**: Real-time flight search using Google Flights API via SerpAPI
- **Hotel Search**: Real-time hotel search using Google Hotels API via SerpAPI
- **Activities Search**: Find tourist attractions and activities using Google Maps Places API

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. API Keys Configuration

You need to set up the following API keys as environment variables:

#### SerpAPI (for Google Flights and Google Hotels)

1. Sign up at [SerpAPI](https://serpapi.com/)
2. Get your API key from the dashboard
3. Set the environment variable:

```bash
export SERPAPI_KEY="your_serpapi_key_here"
```

#### Google Maps API (for Activities/Places)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Places API
   - Geocoding API
   - Maps JavaScript API (optional)
4. Create credentials (API key)
5. Set the environment variable:

```bash
export GOOGLE_MAPS_API_KEY="your_google_maps_api_key_here"
```

### 3. Run the Agent

```bash
adk web
```

## Usage

Once running, you can ask the travel agent questions like:

- "Find me flights from JFK to Paris departing on 2025-12-01"
- "I need a hotel in London from December 15 to December 20"
- "What are the top tourist attractions in Tokyo?"
- "Plan a trip to Barcelona for 3 days with a budget of $2000"

## Architecture

The travel agent consists of:

- **RootAgent**: Orchestrates the overall travel planning
- **FlightFinder**: Searches for flights using Google Flights API
- **HotelRecommender**: Searches for hotels using Google Hotels API
- **ActivitiesAgent**: Finds activities and attractions using Google Maps Places API

## API Rate Limits

- **SerpAPI Free Tier**: 100 searches per month
- **Google Maps API**: Check your quota in Google Cloud Console

Consider upgrading to paid tiers for production use.
