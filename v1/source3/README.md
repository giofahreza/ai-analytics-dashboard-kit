# TINSIG IUP API

Simple API for marine IUP (mining permits) data.

## Quick Start
```bash
cd source3
php -S localhost:8003
```

## Usage
```bash
# Get all data
curl http://localhost:8003/

# With pagination
curl http://localhost:8003/?page=1&limit=3

# Filter by daerah
curl "http://localhost:8003/?daerah=Sungailiat"
```

## Response Format
```json
{
    "status": "success",
    "message": "Marine IUP data retrieved successfully",
    "timestamp": "2025-08-18 10:30:00",
    "data": {
        "data": [...],
        "pagination": {...}
    }
}
```
