# Golf Fantasy Cloud Functions

Cloud functions to handle scheduled tasks for the Golf Fantasy application.

## Overview

This repo contains Google Cloud Functions that handle scheduled data updates previously managed by the main backend's scheduler. Functions include:

- Tournament field updates (Wed/Thu)
- OWGR rankings fetch (Mondays)
- Entry list updates (Multiple times Wed-Thu)
- Points calculation (Mondays)

## Setup

1. Create virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2. Set up environment variables:

```bash
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
SPORTCONTENTAPI_KEY=your_key_here
DATAGOLF_KEY=your_key_here
```

## Function Schedule

| Function | Schedule | Description |
|----------|----------|-------------|
| update_tournament_field | Wed 8:00 AM ET | Updates tournament field data |
| update_owgr_rankings | Mon 8:00 AM ET | Fetches latest OWGR rankings |
| update_entry_list | Multiple times | Updates tournament entries (Wed-Thu) |
| calculate_points | Mon 8:00 AM ET | Calculates tournament points |

## Deployment

Deploy individual functions:
```bash
gcloud functions deploy update_tournament_field \
--runtime python310 \
--trigger-http \
--schedule="0 8 3" \
--time-zone="America/New_York"
```


## Related Repositories

- Main Backend: [golf-fantasy-backend](https://github.com/your-username/golf-fantasy-backend)
- Frontend: [golf-fantasy-frontend](https://github.com/your-username/golf-fantasy-frontend)