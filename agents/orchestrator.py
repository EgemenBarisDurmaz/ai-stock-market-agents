from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from agents.research_agent import create_research_agent
from agents.analysis_agent import create_analysis_agent
from config import WATCHLIST


def run_orchestrator(ticker: str) -> str:
    print(f"\n{'='*50}")
    print(f"Analyzing {ticker}...")
    print(f"{'='*50}")

    print(f"\n[1/2] Research Agent working on {ticker}...")
    research_agent = create_research_agent()
    research_result = research_agent.invoke({
        "messages": [HumanMessage(content=f"Research {ticker} stock")]
    })
    research_summary = research_result["messages"][-1].content
    print(f"Research done: {research_summary[:100]}...")

    print(f"\n[2/2] Analysis Agent analyzing {ticker}...")
    analysis_agent = create_analysis_agent()
    analysis_result = analysis_agent.invoke({
        "messages": [HumanMessage(content=f"""
        Analyze {ticker} stock.
        Here is the research summary: {research_summary}
        Check EMA values and open positions, then give final buy/sell/hold recommendation.
        """)]
    })
    analysis_summary = analysis_result["messages"][-1].content

    llm = ChatAnthropic(model="claude-3-haiku-20240307")
    final_report = llm.invoke([
        HumanMessage(content=f"""
    Based on the following research and analysis for {ticker}, 
    produce a concise alert message (5-7 lines max).
    You MUST use the actual numerical price from the research data, never use placeholder text.
    
    RESEARCH: {research_summary}
    ANALYSIS: {analysis_summary}
    
    Format:
    TICKER: {ticker}
    PRICE: [extract exact price number from research above]
    SIGNAL: [BUY/SELL/HOLD]
    REASON: [2-3 sentences]
    EMA STATUS: [above/below key EMAs]
    """)
    ])

    return final_report.content


def run_all():
    reports = []
    for ticker in WATCHLIST:
        report = run_orchestrator(ticker)
        reports.append(report)
        print(f"\n{report}")
    return reports


if __name__ == "__main__":
    run_all()