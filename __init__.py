"""
travel_agent package

Note: importing the package does not automatically import submodules to avoid
double-import side effects when running modules with `python -m`.

To access the root agent, import the module directly:

	from travel_agent import agent
	root = agent.root_agent

"""

__all__ = ["agent"]
