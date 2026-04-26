from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from db.database import get_all_signals, init_db
import datetime
import json
from config import POSITIONS_FILE

CURRENCY_MAP = {
    ".PA": "€",   # Paris
    ".DE": "€",   # Frankfurt
    ".L":  "£",   # London
    ".SW": "CHF", # Switzerland
    ".AS": "€",   # Amsterdam
}

def get_currency(ticker: str) -> str:
    for suffix, symbol in CURRENCY_MAP.items():
        if ticker.endswith(suffix):
            return symbol
    return "$"

app = FastAPI(title="AI Stock Market Agents")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", response_class=HTMLResponse)
def dashboard():
    signals = get_all_signals()

    rows = ""
    for s in signals:
        currency = get_currency(s.ticker)
        if s.signal == "BUY":
            signal_class = "buy"
            signal_icon = "▲"
        elif s.signal == "SELL":
            signal_class = "sell"
            signal_icon = "▼"
        else:
            signal_class = "hold"
            signal_icon = "◆"

        rows += f"""
        <tr class="table-row">
            <td>
                <div class="ticker-cell">
                    <span class="ticker-name">{s.ticker}</span>
                </div>
            </td>
            <td class="price-cell">{currency}{s.current_price:,.2f}</td>
            <td>
                <span class="signal-badge {signal_class}">
                    {signal_icon} {s.signal}
                </span>
            </td>
            <td class="ema-cell">{s.ema_status}</td>
            <td class="reason-cell">{s.reason[:120]}...</td>
            <td class="time-cell">{s.updated_at.strftime('%b %d, %H:%M')}</td>
        </tr>
        """

    buy_count = sum(1 for s in signals if s.signal == "BUY")
    sell_count = sum(1 for s in signals if s.signal == "SELL")
    hold_count = sum(1 for s in signals if s.signal == "HOLD")
    total = len(signals)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Stock Market Agents</title>
        <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg:        #080c14;
                --surface:   #0d1424;
                --card:      #111827;
                --border:    #1e293b;
                --accent:    #00e5ff;
                --accent2:   #7c3aed;
                --buy:       #00e676;
                --sell:      #ff1744;
                --hold:      #ffa726;
                --text:      #e2e8f0;
                --muted:     #64748b;
                --font-mono: 'Space Mono', monospace;
                --font-main: 'Syne', sans-serif;
            }}

            * {{ margin: 0; padding: 0; box-sizing: border-box; }}

            body {{
                background: var(--bg);
                color: var(--text);
                font-family: var(--font-main);
                min-height: 100vh;
                overflow-x: hidden;
            }}

            /* Animated background grid */
            body::before {{
                content: '';
                position: fixed;
                inset: 0;
                background-image:
                    linear-gradient(var(--border) 1px, transparent 1px),
                    linear-gradient(90deg, var(--border) 1px, transparent 1px);
                background-size: 40px 40px;
                opacity: 0.3;
                z-index: 0;
                animation: gridShift 20s linear infinite;
            }}

            @keyframes gridShift {{
                0%   {{ background-position: 0 0; }}
                100% {{ background-position: 40px 40px; }}
            }}

            /* Glow orbs */
            body::after {{
                content: '';
                position: fixed;
                top: -200px;
                left: -200px;
                width: 600px;
                height: 600px;
                background: radial-gradient(circle, rgba(0,229,255,0.06) 0%, transparent 70%);
                z-index: 0;
                animation: orbFloat 8s ease-in-out infinite alternate;
            }}

            @keyframes orbFloat {{
                0%   {{ transform: translate(0, 0); }}
                100% {{ transform: translate(100px, 80px); }}
            }}

            .container {{
                position: relative;
                z-index: 1;
                max-width: 1400px;
                margin: 0 auto;
                padding: 40px 24px;
            }}

            /* Header */
            .header {{
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                margin-bottom: 48px;
                flex-wrap: wrap;
                gap: 20px;
            }}

            .header-left {{}}

            .logo-line {{
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 8px;
            }}

            .logo-dot {{
                width: 10px;
                height: 10px;
                background: var(--accent);
                border-radius: 50%;
                box-shadow: 0 0 12px var(--accent);
                animation: pulse 2s ease-in-out infinite;
            }}

            @keyframes pulse {{
                0%, 100% {{ opacity: 1; transform: scale(1); }}
                50%       {{ opacity: 0.5; transform: scale(0.8); }}
            }}

            .logo-tag {{
                font-family: var(--font-mono);
                font-size: 11px;
                color: var(--accent);
                letter-spacing: 3px;
                text-transform: uppercase;
            }}

            h1 {{
                font-size: clamp(28px, 4vw, 48px);
                font-weight: 800;
                letter-spacing: -1px;
                line-height: 1.1;
                background: linear-gradient(135deg, #fff 0%, var(--accent) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}

            .subtitle {{
                font-family: var(--font-mono);
                font-size: 12px;
                color: var(--muted);
                margin-top: 8px;
                letter-spacing: 1px;
            }}

            .header-right {{
                display: flex;
                flex-direction: column;
                align-items: flex-end;
                gap: 8px;
            }}

            .live-badge {{
                display: flex;
                align-items: center;
                gap: 8px;
                background: rgba(0,230,118,0.08);
                border: 1px solid rgba(0,230,118,0.2);
                border-radius: 100px;
                padding: 6px 14px;
                font-family: var(--font-mono);
                font-size: 11px;
                color: var(--buy);
                letter-spacing: 2px;
            }}

            .live-dot {{
                width: 6px;
                height: 6px;
                background: var(--buy);
                border-radius: 50%;
                animation: pulse 1.5s ease-in-out infinite;
            }}

            .timestamp {{
                font-family: var(--font-mono);
                font-size: 11px;
                color: var(--muted);
            }}

            /* Stats row */
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 16px;
                margin-bottom: 40px;
            }}

            .stat-card {{
                background: var(--card);
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 24px;
                position: relative;
                overflow: hidden;
                transition: transform 0.2s, border-color 0.2s;
            }}

            .stat-card:hover {{
                transform: translateY(-2px);
                border-color: var(--accent);
            }}

            .stat-card::before {{
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 2px;
            }}

            .stat-card.total::before  {{ background: linear-gradient(90deg, var(--accent), var(--accent2)); }}
            .stat-card.buys::before   {{ background: var(--buy); }}
            .stat-card.sells::before  {{ background: var(--sell); }}
            .stat-card.holds::before  {{ background: var(--hold); }}

            .stat-label {{
                font-family: var(--font-mono);
                font-size: 10px;
                color: var(--muted);
                letter-spacing: 2px;
                text-transform: uppercase;
                margin-bottom: 12px;
            }}

            .stat-value {{
                font-size: 40px;
                font-weight: 800;
                line-height: 1;
            }}

            .stat-card.total .stat-value  {{ color: var(--accent); }}
            .stat-card.buys .stat-value   {{ color: var(--buy); }}
            .stat-card.sells .stat-value  {{ color: var(--sell); }}
            .stat-card.holds .stat-value  {{ color: var(--hold); }}

            /* Table */
            .table-container {{
                background: var(--card);
                border: 1px solid var(--border);
                border-radius: 20px;
                overflow: hidden;
            }}

            .table-header-bar {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 20px 28px;
                border-bottom: 1px solid var(--border);
            }}

            .table-title {{
                font-family: var(--font-mono);
                font-size: 11px;
                color: var(--accent);
                letter-spacing: 3px;
                text-transform: uppercase;
            }}

            .table-count {{
                font-family: var(--font-mono);
                font-size: 11px;
                color: var(--muted);
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            thead th {{
                padding: 14px 28px;
                text-align: left;
                font-family: var(--font-mono);
                font-size: 10px;
                color: var(--muted);
                letter-spacing: 2px;
                text-transform: uppercase;
                border-bottom: 1px solid var(--border);
                font-weight: 400;
            }}

            .table-row {{
                border-bottom: 1px solid rgba(30,41,59,0.5);
                transition: background 0.15s;
                animation: fadeIn 0.4s ease both;
            }}

            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(8px); }}
                to   {{ opacity: 1; transform: translateY(0); }}
            }}

            .table-row:hover {{ background: rgba(0,229,255,0.03); }}
            .table-row:last-child {{ border-bottom: none; }}

            td {{
                padding: 16px 28px;
                vertical-align: middle;
            }}

            .ticker-cell {{
                display: flex;
                align-items: center;
                gap: 12px;
            }}

            .ticker-name {{
                font-family: var(--font-mono);
                font-size: 15px;
                font-weight: 700;
                color: #fff;
                letter-spacing: 1px;
            }}

            .price-cell {{
                font-family: var(--font-mono);
                font-size: 15px;
                font-weight: 700;
                color: var(--accent);
            }}

            .signal-badge {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 5px 14px;
                border-radius: 100px;
                font-family: var(--font-mono);
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1px;
            }}

            .signal-badge.buy {{
                background: rgba(0,230,118,0.1);
                border: 1px solid rgba(0,230,118,0.3);
                color: var(--buy);
            }}

            .signal-badge.sell {{
                background: rgba(255,23,68,0.1);
                border: 1px solid rgba(255,23,68,0.3);
                color: var(--sell);
            }}

            .signal-badge.hold {{
                background: rgba(255,167,38,0.1);
                border: 1px solid rgba(255,167,38,0.3);
                color: var(--hold);
            }}

            .ema-cell {{
                font-family: var(--font-mono);
                font-size: 12px;
                color: var(--muted);
                max-width: 160px;
            }}

            .reason-cell {{
                font-size: 13px;
                color: var(--muted);
                max-width: 280px;
                line-height: 1.5;
            }}

            .time-cell {{
                font-family: var(--font-mono);
                font-size: 11px;
                color: var(--muted);
                white-space: nowrap;
            }}

            /* Empty state */
            .empty-state {{
                text-align: center;
                padding: 80px 40px;
                color: var(--muted);
            }}

            .empty-icon {{
                font-size: 48px;
                margin-bottom: 16px;
                opacity: 0.3;
            }}

            .empty-text {{
                font-family: var(--font-mono);
                font-size: 13px;
                letter-spacing: 1px;
            }}

            /* Footer */
            .footer {{
                margin-top: 32px;
                text-align: center;
                font-family: var(--font-mono);
                font-size: 11px;
                color: var(--muted);
                letter-spacing: 1px;
            }}

            .footer span {{ color: var(--accent); }}
        </style>
    </head>
    <body>
        <div class="container">

            <div class="header">
                <div class="header-left">
                    <div class="logo-line">
                        <div class="logo-dot"></div>
                        <span class="logo-tag">AI · Multi-Agent System</span>
                    </div>
                    <h1>Stock Market<br>Intelligence</h1>
                    <p class="subtitle">ORCHESTRATOR → RESEARCH AGENT + ANALYSIS AGENT</p>
                </div>
                <div class="header-right">
                    <div class="live-badge">
                        <div class="live-dot"></div>
                        LIVE
                    </div>
                    <div class="timestamp">{now}</div>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-card total">
                    <div class="stat-label">Total Signals</div>
                    <div class="stat-value">{total}</div>
                </div>
                <div class="stat-card buys">
                    <div class="stat-label">Buy Signals</div>
                    <div class="stat-value">{buy_count}</div>
                </div>
                <div class="stat-card sells">
                    <div class="stat-label">Sell Signals</div>
                    <div class="stat-value">{sell_count}</div>
                </div>
                <div class="stat-card holds">
                    <div class="stat-label">Hold Signals</div>
                    <div class="stat-value">{hold_count}</div>
                </div>
            </div>

            <div class="table-container">
                <div class="table-header-bar">
                    <span class="table-title">Signal Feed</span>
                    <span class="table-count">{total} instruments monitored</span>
                </div>
                {"<table><thead><tr><th>Ticker</th><th>Price</th><th>Signal</th><th>EMA Status</th><th>Reason</th><th>Updated</th></tr></thead><tbody>" + rows + "</tbody></table>" if signals else '<div class="empty-state"><div class="empty-icon">◎</div><div class="empty-text">No signals yet — agents are initializing</div></div>'}
            </div>

            <div class="footer">
                Powered by <span>Claude Haiku</span> · LangGraph · APScheduler · FastAPI
            </div>

        </div>
    </body>
    </html>
    """
    return html


@app.get("/positions")
def get_positions():
    with open(POSITIONS_FILE) as f:
        return json.load(f)


@app.get("/signals")
def get_signals():
    signals = get_all_signals()
    return [
        {
            "ticker": s.ticker,
            "price": s.current_price,
            "signal": s.signal,
            "ema_status": s.ema_status,
            "reason": s.reason,
            "updated_at": str(s.updated_at)
        }
        for s in signals
    ]