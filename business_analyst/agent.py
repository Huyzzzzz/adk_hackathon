"""Demonstration of AI Business Analyst using Agent Development Kit"""

from google.adk.agents import Agent

from business_analyst import prompt

from business_analyst.sub_agents.ur_agent.agent import ur_agent

# from src.tools.memory import _load_precreated_itinerary

root_agent = Agent(
    model="gemini-2.5-flash-preview-05-20",
    name="root_agent",
    description="An Business Analyst using the functions of multiple sub-agents",
    instruction=prompt.ROOT_AGENT_INSTRUCTION,
    sub_agents=[
        ur_agent,
    ],
    # before_agent_callback=_load_precreated_itinerary,
)