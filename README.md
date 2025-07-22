# Diamond Details API

This API accepts a list of diamond IDs and returns detailed polished and rough carat information 
for each diamond, along with a summary of carat differences.

## Features
- Fetch polished and rough carat weights for diamonds
- Calculate difference between rough and polished carats
- Provide summary statistics including total diamonds, mean, min, and max differences

## Usage
Send a POST request with a JSON array of diamond IDs to `/diamond_details` 
to get detailed diamond data and a summary.

## Setup
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```
2. Configure environment variables (e.g., BEARER_TOKEN, PLATFORM_ID, TRACR_BULK_URL) in a .env file or your shell environment.
3. ```bash
   pip install -r requirements.txt
   ```
4. Run locally
```bash
uvicorn app.main:app --reload
```
The API will be available at http://127.0.0.1:8000.
Send POST requests to /diamond_details with a JSON array of diamond IDs to get diamond details and summary.


