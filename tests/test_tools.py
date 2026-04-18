from tools.stock_tools import get_stock_price, get_recent_news
from tools.analysis_tools import calculate_ema, check_positions
from agents.research_agent import create_research_agent
from agents.analysis_agent import create_analysis_agent
from agents.orchestrator import run_orchestrator

print("=== STOCK PRICE ===")
price = get_stock_price("AAPL")
print(price)

print("\n=== RECENT NEWS ===")
news = get_recent_news("AAPL")
for article in news:
    print(article)

print("\n=== EMA ===")
ema = calculate_ema("AAPL")
print(ema)

print("\n=== POSITIONS ===")
positions = check_positions()
print(positions)

print("\n=== RESEARCH AGENT ===")
research_agent = create_research_agent()
result = research_agent.invoke({"messages": [{"role": "user", "content": "Research AAPL stock"}]})
print(result["messages"][-1].content)

print("\n=== ANALYSIS AGENT ===")
analysis_agent = create_analysis_agent()
result = analysis_agent.invoke({"messages": [{"role": "user", "content": "Analyze AAPL stock and give recommendation"}]})
print(result["messages"][-1].content)

print("\n=== ORCHESTRATOR ===")
report = run_orchestrator("AAPL")
print(report)