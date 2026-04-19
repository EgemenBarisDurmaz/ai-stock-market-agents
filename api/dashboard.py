from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from db.database import get_all_signals, init_db
import datetime

app = FastAPI(title="AI Stock Market Agents")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", response_class=HTMLResponse)
def dashboard():
    signals = get_all_signals()

    rows = ""
    for s in signals:
        color = "#4CAF50" if s.signal == "BUY" else "#f44336" if s.signal == "SELL" else "#FF9800"
        rows += f"""
        <tr>
            <td><b>{s.ticker}</b></td>
            <td>${s.current_price:,.2f}</td>
            <td style="color:{color}"><b>{s.signal}</b></td>
            <td>{s.ema_status}</td>
            <td>{s.reason[:100]}...</td>
            <td>{s.updated_at.strftime('%Y-%m-%d %H:%M')}</td>
        </tr>
        """

    html = f"""
    <html>
    <head>
        <title>AI Stock Market Agents</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
            h1 {{ color: #00d4ff; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th {{ background: #16213e; padding: 12px; text-align: left; color: #00d4ff; }}
            td {{ padding: 10px; border-bottom: 1px solid #333; }}
            tr:hover {{ background: #16213e; }}
        </style>
    </head>
    <body>
        <h1>AI Stock Market Agents Dashboard</h1>
        <p>Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <table>
            <tr>
                <th>Ticker</th>
                <th>Price</th>
                <th>Signal</th>
                <th>EMA Status</th>
                <th>Reason</th>
                <th>Updated</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """
    return html


@app.get("/positions")
def get_positions():
    import json
    from config import POSITIONS_FILE
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