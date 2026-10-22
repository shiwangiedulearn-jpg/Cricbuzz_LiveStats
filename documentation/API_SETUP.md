# API Setup

## Cricbuzz RapidAPI

The application expects the RapidAPI key in a `.env` file at the project root.

Example:

```text
RAPIDAPI_KEY=your_rapidapi_key_here
```

The application loads this value using `python-dotenv`.

The key must never be placed directly in source code or committed to Git.

## API Header

The Cricbuzz RapidAPI client uses:

```text
x-rapidapi-key: <RAPIDAPI_KEY>
x-rapidapi-host: cricbuzz-cricket.p.rapidapi.com
```

## Rate Limit

During development the RapidAPI account reached its monthly request quota.
For that reason, the existing collected database is used for SQL analytics
and dashboard demonstrations where possible.

Do not fabricate API results when the API is unavailable.
