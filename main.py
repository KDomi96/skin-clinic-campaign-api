from typing import Literal

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, RedirectResponse

from analysis import build_tables, load_data

app = FastAPI(title="Skin Clinic Campaign Analysis")

# the csv is small and never changes, so just crunch it once on startup
df = load_data()
tables = build_tables(df)
overall_rate = round(df["responded"].mean() * 100, 2)

PAGE = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Campaign Analysis</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 760px; margin: 40px auto; padding: 0 16px; color: #222; }}
    h1 {{ margin-bottom: 4px; }}
    h2 {{ margin-top: 36px; font-size: 18px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ccc; padding: 8px 12px; text-align: left; }}
    th {{ background: #f2f2f2; }}
    .note {{ color: #666; }}
  </style>
</head>
<body>
  <h1>Skin Clinic Campaign Analysis</h1>
  <p class="note">{n} customers, overall response rate {rate}%</p>
  {sections}
</body>
</html>"""


@app.get("/")
def root():
    return RedirectResponse("/campaign-analysis")


@app.get("/campaign-analysis")
def campaign_analysis(fmt: Literal["html", "json"] = Query("html", alias="format")):
    # ?format=json if you want the raw numbers instead of the page
    if fmt == "json":
        return {
            "total_customers": len(df),
            "overall_response_rate_pct": overall_rate,
            "tables": {t: tbl.to_dict(orient="records") for t, tbl in tables.items()},
        }

    sections = "".join(
        f"<h2>{title}</h2>" + tbl.to_html(index=False, border=0)
        for title, tbl in tables.items()
    )
    return HTMLResponse(PAGE.format(n=len(df), rate=overall_rate, sections=sections))
