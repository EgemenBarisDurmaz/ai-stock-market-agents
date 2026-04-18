from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from tools.stock_tools import get_stock_price, get_recent_news


@tool
def stock_price_tool(ticker: str) -> dict:
    """Fetches current stock price and daily change for a given ticker symbol."""
    return get_stock_price(ticker)


@tool
def recent_news_tool(ticker: str) -> list:
    """Fetches recent news articles for a given stock ticker symbol."""
    return get_recent_news(ticker)


def create_research_agent():
    llm = ChatAnthropic(model="claude-3-haiku-20240307")
    tools = [stock_price_tool, recent_news_tool]

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt="You are a stock research agent. Always fetch both the current price and recent news for the given ticker. Summarize findings clearly."
    )
    return agent