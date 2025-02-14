from fastapi import FastAPI 
import uuid
import os
import json
import math
from datetime import datetime

app = FastAPI()
STORAGE_DIR = "receipts"
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.post("/receipts/process")
async def post_receipt(payload: dict):
    random_id = str(uuid.uuid4())
    file_path = os.path.join(STORAGE_DIR, f"{random_id}.json")

    with open(file_path, "w") as file:
        json.dump(payload, file, indent=4)

    required_fields = ['retailer', 'purchaseDate', 'purchaseTime', 'items', 'total']

    if any(not payload.get(field) for field in required_fields):
        return {"error": "The receipt is invalid."}

    return {"id": random_id}

@app.get("/receipts/{id}/points")
async def get_points(id: str):

    file_path = os.path.join(STORAGE_DIR, f"{id}.json")

    if not os.path.exists(file_path):
        return {"error": "No receipt found for that ID."}

    with open(file_path, "r") as file:
        data = json.load(file)

    points = 0

    retailer_name = ''.join(char for char in data['retailer'] if char.isalnum())
    points += len(retailer_name)

    if float(data['total']) % 1 == 0:
        points += 50
    if float(data['total']) % 0.25 == 0:
        points += 25
    
    points += (len(data['items']) // 2) * 5

    for item in data['items']:
        price = float(item['price'])
        if len(item['shortDescription'].strip()) % 3 == 0:
            price *= 0.2
            price = math.ceil(price)
            points += price

    if int(datetime.strptime(data['purchaseDate'], "%Y-%m-%d").day) % 2 == 1:
        points += 6

    if 14 <= datetime.strptime(data['purchaseTime'], "%H:%M").hour <= 16:
        points += 10
    
    return points
