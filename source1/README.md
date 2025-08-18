# TINSIG Illegal Mining API

Simple API for illegal mining survey data from Bangka Belitung.

## Quick Start
```bash
cd source1
php -S localhost:8001
```

## Usage
```bash
# Get all data
curl http://localhost:8001/

# With pagination
curl http://localhost:8001/?page=1&limit=3

# Filter by kabupaten
curl "http://localhost:8001/?kabupaten=Bangka%20Selatan"
```

## Response Format
```json
{
    "status": "success",
    "message": "Illegal mining data retrieved successfully",
    "timestamp": "2025-08-18 10:30:00",
    "data": {
        "data": [...],
        "pagination": {...}
    }
}
```
