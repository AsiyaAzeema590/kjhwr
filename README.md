# UK Wind Forecast Dashboard

A full-stack dashboard for analysing UK wind generation forecasts against actual wind generation data for January 2026. The application helps energy procurement teams understand forecast accuracy and evaluate potential differences between predicted and actual wind generation.

## Live Demo

- **Frontend:** https://wind-forecast-frontend-mu.vercel.app
- **Backend API:** https://wind-forecast-backend-rho.vercel.app
- **API Health Check:** https://wind-forecast-backend-rho.vercel.app/health
- **Analysis API:** https://wind-forecast-backend-rho.vercel.app/api/analysis

## Technologies Used

### Frontend
- React.js
- JavaScript
- HTML5
- CSS3
- Recharts

### Backend
- Python
- FastAPI
- Pandas
- NumPy
- Requests

### Data Source
- Elexon BMRS API

### Deployment
- Vercel

## Project Features

- Fetches UK wind generation actuals and forecast data.
- Analyses January 2026 wind generation data.
- Compares forecast values with actual generation.
- Calculates forecast accuracy metrics.
- Displays forecast and actual generation charts.
- Provides a REST API using FastAPI.
- Uses saved analysis data to avoid repeatedly fetching large datasets.

## Forecast Accuracy Metrics

The current saved analysis contains 743 matched records.

| Metric | Value |
|---|---:|
| MAE | 1055.76 |
| RMSE | 1372.43 |
| MAPE | 8.59% |
| Bias | -431.73 |
| Records | 743 |

## Project Structure


wind-forecast-dashboard/
│
├── Backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── main.py
│   │   └── config.py
│   ├── data/
│   │   └── analysis.json
│   ├── tests/
│   ├── requirements.txt
│   └── save_analysis.py
│
├── Frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
│
├── .gitignore
└── README.md


## Run Locally

### 1. Clone the repository

bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd wind-forecast-dashboard

2. Start the backend

bash
cd Backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload


Backend runs at:

`http://localhost:8000`

API documentation:

http://localhost:8000/docs

### 3. Start the frontend

Open another terminal:

bash
cd Frontend
npm install
npm run dev


Frontend runs at:

`http://localhost:5173`

## API Endpoints

| Endpoint | Description |

| `/health` | Backend health check |
| `/api/status` | API status |
| `/api/data/actual` | Actual wind generation data |
| `/api/data/forecast` | Wind generation forecast data |
| `/api/analysis` | Saved forecast analysis and metrics |

## Environment Configuration

The frontend uses the following environment variable:


VITE_API_URL=http://localhost:8000/api


For production, the deployed backend URL is configured through Vercel environment variables.

## Data Processing

The backend processes actual and forecast wind generation data obtained from the Elexon BMRS API. It prepares matching delivery-hour records and calculates forecast error and accuracy metrics.

The dashboard reads the generated `Backend/data/analysis.json` file through the analysis API.

## Author

Developed as a full-stack UK wind generation forecasting and analysis project.
