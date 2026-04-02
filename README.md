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

## 👨‍👩‍👦 Team Contributions

* **Frontend & UI/UX**
  Designed and implemented the user interface, map integration, and data visualization.

* **Machine Learning**
  Data preprocessing, model training, and AQI prediction.

* **Backend Development**
  Built APIs, handled data processing, and integrated ML models.

* **Integration & Testing**
  Connected frontend and backend, performed testing, and ensured system stability.

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
git clone https://github.com/your-username/ecoair-insight.git
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

## 📸 Screenshots (To be added)

* Dashboard view
* Map interaction
* AQI visualization
* Prediction graphs

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

## 📄 License

This project is developed as part of an academic assignment and is intended for educational purposes.
