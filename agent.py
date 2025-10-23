from google import adk

from .sub_agents.flight_agent import agent as flight_agent_module
from .sub_agents.hotel_agent import agent as hotel_agent_module
from .sub_agents.activities_agent import agent as activities_agent_module

flight_agent = getattr(flight_agent_module, 'flight_agent', None)
hotel_agent = getattr(hotel_agent_module, 'hotel_agent', None)
activities_agent = getattr(activities_agent_module, 'activities_agent', None)

root_agent = adk.Agent(
    name="RootAgent",
    model="gemini-2.5-pro",
    sub_agents=[a for a in (flight_agent, hotel_agent, activities_agent) if a is not None],
    description="Coordinates travel planning by calling flight, stay, and activity agents.",
    instruction=(
        "You are an agent responsible for orchestrating trip planning tasks. "
        "You call external agents to gather flights, stays, and activities, then return a final result."
    )
)
