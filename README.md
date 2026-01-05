# Weekend-Getaway-Ranker
A data engineering project that builds a travel recommendation engine using Python and Pandas. It ranks weekend getaways based on distance, user ratings, and popularity using a weighted scoring algorithm.
# ✈️ Weekend Getaway Ranker

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Weekend Getaway Ranker** is a recommendation engine designed to help travelers find the best short-trip destinations from their city. By analyzing a dataset of Indian tourist spots, the algorithm calculates a "Smart Score" for each destination, balancing travel distance against popularity and ratings.

---

## ✨ Features

* **📍 Distance Calculation:** Uses the `geopy` library to calculate the real-world geodesic distance between the source city and potential destinations.
* **📊 Weighted Ranking Algorithm:** Ranks destinations not just by rating, but by a weighted combination of **Rating (30%)**, **Popularity (20%)**, and **Distance (50%)**.
* **🧠 Intelligent Filtering:** Automatically filters out destinations that are too far (> 600km) for a practical weekend trip.
* **📉 Data Normalization:** Uses `MinMaxScaler` to normalize disparate data points (e.g., 5-star ratings vs. 200km distance) onto a comparable 0-1 scale.
* **⚡ Caching System:** Implements coordinate caching to minimize API calls and speed up execution.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Data Manipulation:** Pandas, NumPy
* **Geospatial Processing:** Geopy (Nominatim API)
* **Machine Learning (Preprocessing):** Scikit-learn (MinMaxScaler)

---

## 📐 The Ranking Logic

The core of this project is the weighted scoring formula. To ensure fair comparison, all metrics are normalized to a 0-1 scale.

**The Formula:**
```math'''
Score = (0.3 \times Rating) + (0.2 \times Popularity) + (1.0 - (0.5 \times Distance))

--- Top Weekend Getaways from Mumbai ---
📍 Calculating distances from Mumbai...
      Name             City      Type      Distance   Rating   Final_Score
1. Gateway of India   Mumbai    Monument     0.0 km     4.6      1.268
2. Calangute Beach    Goa       Beach      416.3 km     4.5      1.033
3. City Palace        Udaipur   Palace     618.5 km     4.5      0.890
