# File: visualization/dashboard.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import os

app = FastAPI()
# Mount static files (if any)
static_dir = "visualization/static"
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
# Templates directory
templates = Jinja2Templates(directory="visualization/templates")

DB_PATH = "data/packets.db"


def get_summary():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT classification, COUNT(*) FROM packets GROUP BY classification")
    data = {row[0] or 'UNCLASSIFIED': row[1] for row in c.fetchall()}
    conn.close()
    return data


def get_recent_logs(limit: int = 50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT rowid, timestamp, src_ip, dst_ip, src_port, dst_port, protocol, classification "
        "FROM packets ORDER BY rowid LIMIT ?",
        (limit,)
    )
    rows = c.fetchall()
    conn.close()
    return rows


@app.get("/")
async def dashboard(request: Request, limit: int = 50):
    summary = get_summary()
    logs = get_recent_logs(limit)
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "summary": summary, "logs": logs}
    )
