from google import adk

activities_agent = adk.Agent(
    name="ActivitiesAgent",
    model="gemini-2.5-pro",
    description="Suggests interesting activities for the user at a destination.",
    instruction=(
        "Given a destination, dates, and budget, suggest 2-3 engaging tourist or cultural activities. "
        "For each activity, provide name, a short description, price estimate, and duration in hours. "
        "Respond in plain English (not JSON). Keep it concise and well-formatted."
    ),
)
