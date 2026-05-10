# 🌍 EcoAir Insight

EcoAir Insight is a data-driven web application that provides real-time air quality monitoring, future pollution prediction, and health risk analysis based on user-selected locations.

---

## 🚀 Features

* 📍 Interactive map to select any location
* 🌫️ Displays current air pollution levels (AQI, PM2.5, PM10, etc.)
* 🔮 Predicts future air quality trends (next 5 years) using Machine Learning
* ⚠️ Provides health risk analysis based on AQI levels
* 🛠️ Suggests preventive measures to reduce exposure
* 🎨 Clean and modern dashboard UI

---

## 🧠 Problem Statement

Air pollution is one of the leading environmental risks to health. However, most platforms only provide current data without meaningful insights into future trends or actionable health guidance.

EcoAir Insight bridges this gap by combining:

* Real-time environmental data
* Predictive analytics
* Health awareness

---

## 🏗️ Tech Stack

### Frontend

* React (Vite)
* Tailwind CSS
* Leaflet (Map integration)
* Chart.js (Data visualization)

### Backend

* FastAPI (Python)
* REST APIs

### Machine Learning

* Scikit-learn
* Pandas

### Data Sources

* Air pollution datasets (provided)
* External APIs (optional)

---

## 🧩 System Architecture

User → Frontend (React) → Backend (FastAPI) → ML Model + Dataset → Response → UI Display

---

## 📊 Core Functionalities

### 1. Location-Based AQI

Users can click on a map to retrieve air quality data for a specific location.

### 2. Future Prediction

Machine learning models predict AQI trends for the next 5 years.

### 3. Health Risk Analysis

AQI levels are categorized into health risk levels:

* Good
* Moderate
* Unhealthy
* Hazardous

### 4. Preventive Measures

System provides actionable suggestions based on pollution levels.

---

---

## 📅 Development Timeline

### Week 1

* Project setup
* Dataset cleaning
* Basic UI and backend setup

### Week 2

* Core feature implementation
* API integration
* Prediction model integration

### Week 3

* UI improvements
* Testing and debugging
* Final optimization

---

## ⚙️ Installation & Setup

### Clone the repository

```bash
git clone https://github.com/karthik768990/EcoAir-Insight.git
cd ecoair-insight
```

### Frontend setup

```bash
cd frontend
npm install
npm run dev
```

### Backend setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---



---

## 🚀 Future Enhancements

* Pollution heatmaps
* Real-time alerts
* Mobile responsiveness
* Advanced ML models (LSTM)

---

## 📌 Conclusion

EcoAir Insight provides a comprehensive platform for understanding air pollution and its future impact, helping users make informed decisions for healthier living.

---

