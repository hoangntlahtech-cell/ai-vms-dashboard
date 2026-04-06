from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import threading
import time
import random
from datetime import datetime
import os

app = FastAPI()

events = []
RESET_FLAG = False

os.makedirs("snapshot", exist_ok=True)

app.mount("/snapshot", StaticFiles(directory="snapshot"), name="snapshot")


@app.get("/events")
def get_events():
    return events


@app.get("/reset")
def reset():
    global events, RESET_FLAG
    events = []
    RESET_FLAG = True
    return {"status": "reset done"}


@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open("dashboard.html", "r", encoding="utf-8") as f:
        return f.read()


def fake_stream():
    global events, RESET_FLAG

    while True:
        time.sleep(0.5)

        if RESET_FLAG:
            RESET_FLAG = False
            continue

        persons = random.randint(1, 4)

        event = {
            "id": int(time.time()*1000),
            "time": datetime.now().isoformat(),
            "camera": f"CAM_POS_{random.randint(1,3)}",
            "type": "transaction",
            "persons": persons,
            "snapshot": "test.jpg"
        }

        events.append(event)

        if len(events) > 200:
            events.pop(0)


threading.Thread(target=fake_stream, daemon=True).start()