from pathlib import Path
import sqlite3
import sys

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import plotly

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "expense.db"


def get_connection():
    connection = sqlite3.connect(
        DB_PATH,
        check_same_thread=False,
    )
    connection.row_factory = sqlite3.Row
    return connection


connection = get_connection()

connection.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL CHECK (Amount > 0) 
)
""")

connection.commit()

# Ensure `from Home import connection` in `services.methods` resolves to this module
sys.modules.setdefault("Home", sys.modules[__name__])

from pages.Expense_Tracker import router as expense_tracker_router  # noqa: E402
from pages.Expenses import router as expenses_router  # noqa: E402

app = FastAPI(title="Welcome to our Expense Tracker")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
PLOTLY_JS_PATH = Path(plotly.__file__).resolve().parent / "package_data" / "plotly.min.js"


@app.get("/static/plotly.min.js")
def serve_plotly_js():
    return FileResponse(PLOTLY_JS_PATH, media_type="application/javascript")


app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(expense_tracker_router)
app.include_router(expenses_router)


@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"active_page": "home"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
