from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from tools.analysis_tools import calculate_ema, check_positions


@tool
def ema_tool(ticker: str) -> dict:
    """Calculates EMA for 20, 50, 100, 200 days for a given stock ticker."""
    return calculate_ema(ticker)


@tool
def positions_tool() -> list:
    """Returns all currently open trading positions."""
    return check_positions()


def create_analysis_agent():
    llm = ChatAnthropic(model="claude-3-haiku-20240307")
    tools = [ema_tool, positions_tool]

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt="You are a stock analysis agent. Check EMA values and open positions for the given ticker. Provide a clear buy/sell/hold recommendation with reasoning."
    )
    return agent