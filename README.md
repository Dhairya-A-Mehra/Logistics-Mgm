# Logistics-Mgm

## file structure

```
/ (Project Root: Logistics-Mgm)
├── .env                  # Single source of truth for all environment variables
├── .env.example          # Example file for environment variables
├── requirements.txt      # Single file for all Python dependencies
├── .gitignore            # Global gitignore
├── README.md             # Project-level README
├── venv/                 # Virtual environment at the root (as requested)
|
├── apps/
│   └── web/              # Your Next.js frontend application
│       ├── src/
│       ├── public/
│       ├── package.json
│       └── ... (rest of the Next.js files)
|
└── src/                  # All Python backend source code lives here
    ├── __init__.py
    ├── main.py           # The single FastAPI application entry point
    ├── config.py         # Loads configuration from the root .env file
    ├── database.py       # SQLAlchemy setup, models, and session management
    ├── security.py       # Password hashing, JWT creation/decoding, dependencies
    |
    ├── api/              # Package for all API-related modules
    │   ├── __init__.py
    │   └── routers/      # All API endpoint routers
    │       ├── __init__.py
    │       └── auth.py   # The authentication router (/login, /register)
    │       └── ... (future routers: orders.py, shipments.py, etc.)
    |
    ├── services/         # Package for business logic (database interactions)
    │   ├── __init__.py
    │   └── user_service.py # Functions for creating/getting users
    |
    └── schemas/          # Package for all Pydantic models (data shapes)
        ├── __init__.py
        └── user.py       # Pydantic schemas for User and Token
```
