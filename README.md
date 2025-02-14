# fetch-rewards
Receipt Processor Challenge - Fetch Coding Assessment



## Endpoints
### POST /receipts/process
JSON must contain:
- retailer
- purchaseDate
- purchaseTime
- items
- total

### GET /receipts/{id}/points
JSON must contain:
- id



## Usage
In the receipt_processor directory, run:
docker-compose up --build

Navigate to localhost:8000 and test it out!