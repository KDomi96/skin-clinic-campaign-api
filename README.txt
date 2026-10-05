Skin clinic campaign analysis (FastAPI)

Run it locally
  pip install -r requirements.txt
  uvicorn main:app --reload
  open http://127.0.0.1:8000/campaign-analysis

  Add ?format=json to the url if you want raw json instead of the tables.

Print the tables in the terminal
  python analysis.py

Deploy on Render
  1. Push this folder to a GitHub repo (the csv in data/ has to go with it).
  2. On render.com: New > Web Service > connect the repo.
  3. Build command:  pip install -r requirements.txt
     Start command:  uvicorn main:app --host 0.0.0.0 --port $PORT
     (render.yaml already has both, so Render may fill them in for you)
  4. Deploy, then submit  https://<your-service>.onrender.com/campaign-analysis

Python is pinned to 3.10.12 in render.yaml (what I tested on). If you set up the service
by hand instead of using render.yaml, add PYTHON_VERSION = 3.10.12 under Environment.

The free plan sleeps after a while, so the first request can take around 50 seconds.
Open the link once before you submit it so it is awake.
