# EcoAir Insight - Technical Architecture & Engineering Deep Dive

EcoAir Insight is an AI-powered air quality intelligence platform designed to analyze, forecast, and visualize air pollution data across India. This document serves as a comprehensive technical overview of the system's architecture, ML pipeline, backend services, and frontend engineering decisions.

---

## 1. System Architecture

EcoAir Insight adopts a decoupled architecture separating the machine learning pipeline, the RESTful backend, and the interactive frontend.

- **Frontend**: React SPA (Single Page Application) built with Vite, utilizing Leaflet for geospatial mapping and Framer Motion for fluid UX.
- **Backend**: Python FastAPI service orchestrating data retrieval, spatial queries, and external AI integrations.
- **Database**: SQLite (`ecoair.db`), utilizing SQLAlchemy ORM. Serves as the central data store for monitoring stations, historic AQI, and precomputed ML predictions.
- **ML Pipeline**: A standalone Python batch processing system using `scikit-learn` and `joblib` for parallelized model training and inference.

### Data Flow Execution
1. **User Interaction**: User clicks on the Leaflet map or searches for a location (managed by `MapPage.jsx`).
2. **Geospatial Resolution**: The frontend sends the `(lat, lon)` to the FastAPI backend (`GET /analysis`).
3. **Orchestration**:
   - `find_nearest_station_with_data` calculates the Haversine distance to locate the closest active monitoring station in SQLite.
   - `get_current_aqi` retrieves the latest pollution metrics.
   - `get_prediction` queries the 5-year precomputed forecast.
   - `generate_ai_insights` calls an LLM to generate contextual analysis based on the specific pollutant mix.
4. **Presentation**: Data is returned to the client and rendered in a glassmorphic React `InfoPanel` with interactive Chart.js visualizations.

---

## 2. Machine Learning Pipeline Internals

Rather than running inference synchronously on the backend, the ML pipeline operates as an offline batch process (`train_model.py`) that precomputes forecasts. This architectural decision ensures the API remains highly responsive.

### 2.1 Algorithm & Setup
The core predictive model is the **`HistGradientBoostingRegressor`** from `sklearn.ensemble`. It was chosen for its native support for missing values and fast execution on large datasets.
- **Hyperparameters**: `max_depth=6`, `learning_rate=0.05`, `max_iter=200`, `random_state=42`.
- **Parallelization**: Training is distributed across available CPU cores using `joblib.Parallel` with the `loky` backend. A separate model is trained for *each individual monitoring station*.

### 2.2 Feature Engineering
For each station, historic data is aggregated by month. The time-series nature of the data is captured through engineered features:
- **Cyclical Temporal Features**: `Month_Index`, `Month`, `sin_month`, and `cos_month` (capturing seasonal pollution patterns).
- **Autoregressive Features**: `lag_1`, `lag_2`, and `lag_3` (the AQI of the previous 3 months).
- **Rolling Statistics**: `rolling_mean_3` and `rolling_std_3` to capture short-term trends and volatility.

### 2.3 5-Year Autoregressive Forecasting
The pipeline generates a 60-month (5-year) forecast using an autoregressive loop. 
1. The model predicts the next month's AQI.
2. The predicted AQI is appended to the feature set, simulating `lag_1` for the subsequent step.
3. Rolling means and temporal features are recalculated for `t+1`, and the cycle repeats 60 times.
4. **Confidence Intervals**: An upper bound and a lower bound (`max(0, val - std_dev)`) are computed using the standard deviation of the forecasted trajectory.

### 2.4 Data Processing (`process_raw_data.py`)
Raw data arrives as multi-tab Excel files. The script normalizes column headers, filters out non-data sheets, enforces `date` and `aqi` validity, and extracts a canonical set of stations (`stations.csv`) and cleaned metrics (`cleaned_data.csv`).

---

## 3. Backend Architecture (FastAPI)

The backend (`backend/app/main.py`) acts as the high-performance orchestration layer.

### 3.1 API Routes
The primary endpoint powering the application is:
- **`GET /analysis`**:
  - **Query Parameters**: `lat` (float), `lon` (float)
  - **Response Shape**: Returns a heavily nested JSON payload including `station` metadata, `is_fallback` flag, `distance_km`, `current` (PM2.5, PM10, etc.), `prediction` (forecast array), `health` (risk level and advice), and `ai_insights` (LLM-generated markdown).

### 3.2 Database & Async Migration
To simplify deployment, the backend utilizes SQLite. A notable engineering decision is the **Background Migration Thread**:
- During FastAPI startup (via the `@asynccontextmanager async def lifespan`), the app checks if the `Station` table is empty.
- If empty, it spawns a daemon thread `threading.Thread(target=run_migration, daemon=True)` to execute `migrate_to_db.py`.
- This ensures the FastAPI server starts immediately and is ready to accept requests without blocking, returning a graceful `"Database is currently being populated"` error to early API callers until the CSV data is fully loaded into SQLite.

---

## 4. Frontend Architecture (React)

The frontend is engineered for a premium, highly responsive user experience.

### 4.1 State Management & Component Wiring
State is managed locally in top-level components (e.g., `MapPage.jsx`) and passed down via props. 
- The `handleClick` function translates Leaflet map click events (yielding `latlng`) into asynchronous Axios calls to the `/analysis` backend endpoint.
- To prevent UI jank, a dedicated `loading` state toggles a `<Loader />` component while the backend aggregates data and resolves the LLM prompt.

### 4.2 UI/UX Engineering
- **Glassmorphism & Fluid Animation**: `framer-motion` handles the entrance and exit of the `<InfoPanel />`. The panel uses a glassmorphic design (`backdropFilter: "blur(16px)"`) to overlay data cleanly above the interactive map.
- **Graceful Fallbacks**: If the user clicks an area without immediate coverage, the backend returns `is_fallback=True` with the `distance_km` to the nearest station. The UI renders a specific warning state to inform the user of the spatial approximation.
- **Data Visualization**: Forecast data is routed into the `<PredictionChart />` component, which manages Chart.js configuration for rendering the predicted AQI alongside its confidence intervals.

---

## 5. Engineering Decisions & Future Work

### 5.1 Tradeoffs & Decisions
1. **Offline ML Inference over Real-time**: Serving a scikit-learn model in the request-response cycle can introduce latency spikes, especially when forecasting 60 steps autoregressively. By precomputing predictions and storing them in SQLite alongside station data, the `/analysis` endpoint guarantees low-latency O(1) reads for predictions.
2. **SQLite for Production?**: Given the read-heavy nature of the application (monitoring stations don't change frequently, and historical/predicted data is batch-updated), SQLite is highly efficient. The background migration thread makes cold-start deployments (e.g., on Render or Vercel) seamless.
3. **FastAPI**: Selected over Flask/Django for its native async capabilities and automatic Pydantic validation. The `@asynccontextmanager` made the background database initialization trivial to implement.

### 5.2 Future Roadmap (Productionization)
- **Spatial Interpolation**: Currently, the system falls back to the nearest station. Implementing Inverse Distance Weighting (IDW) or Kriging could provide estimated AQI for unmonitored coordinates based on a web of nearby stations.
- **Database Migration**: Moving from SQLite to PostgreSQL + PostGIS would allow for native bounding-box and spatial queries (`ST_DWithin`), optimizing the `find_nearest_station` logic which currently relies on application-level Haversine distance calculations.
- **Model CI/CD**: Integrating Airflow or Prefect to automatically trigger `train_model.py` as new monthly data arrives, seamlessly updating the `predictions` table.
