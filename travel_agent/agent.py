from google import adk
from google.adk.tools.transfer_to_agent_tool import transfer_to_agent

from travel_agent.sub_agents.flight_agent import agent as flight_agent_module
from travel_agent.sub_agents.hotel_agent import agent as hotel_agent_module
from travel_agent.sub_agents.activities_agent import agent as activities_agent_module

flight_agent = getattr(flight_agent_module, "flight_agent", None)
hotel_agent = getattr(hotel_agent_module, "hotel_agent", None)
activities_agent = getattr(activities_agent_module, "activities_agent", None)


def find_flights(
    *,
    destination: str | None = None,
    dates: str | None = None,
    budget: float | None = None,
    tool_context=None,
):
    """Tool entrypoint exposed to the model as `find_flights`.

    This function simply requests a transfer to the `FlightFinder` agent so
    that the specialized sub-agent handles the actual flight search logic.

    The signature is permissive so the model can call it with different
    argument shapes; `tool_context` is populated by the framework when the
    tool is invoked.
    """
    # transfer_to_agent sets tool_context.actions.transfer_to_agent to the
    # given agent name. It doesn't need to return a value.
    return transfer_to_agent("FlightFinder", tool_context)


root_agent = adk.Agent(
    name="RootAgent",
    model="gemini-2.5-pro",
    sub_agents=[
        a for a in (flight_agent, hotel_agent, activities_agent) if a is not None
    ],
    # Register the callable so the ADK exposes `find_flights` in tools_dict.
    tools=[find_flights],
    description="Coordinates travel planning by calling flight, stay, and activity agents.",
    instruction=(
        "You are an agent responsible for orchestrating trip planning tasks. "
        "You call external agents to gather flights, stays, and activities, then return a final result."
    ),
)
