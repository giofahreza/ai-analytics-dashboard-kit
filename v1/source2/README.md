# TINSIG Production API

Simple API for tin ore production data.

## Quick Start
```bash
cd source2
php -S localhost:8002
```

## Usage
```bash
# Get all data
curl http://localhost:8002/

# With pagination
curl http://localhost:8002/?page=1&limit=3

# Filter by kabupaten
curl "http://localhost:8002/?kabupaten=Bangka"
```

## Response Format
```json
{
    "status": "success",
    "message": "Tin ore production data retrieved successfully",
    "timestamp": "2025-08-18 10:30:00",
    "data": {
        "data": [...],
        "pagination": {...}
    }
}
```
