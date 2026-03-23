# ⚡ AI Predictive Maintenance for Electric Submersible Pumps (ESP)

## 📌 Overview

This project presents a **real-time predictive maintenance system for Electric Submersible Pumps (ESPs)** using embedded sensing, signal processing, and machine learning. The system monitors the **electrical current drawn by the pump motor**—a key indicator of the pump’s operational state—to detect faults such as cavitation and mechanical degradation.

The project evolved from foundational signal analysis into a **fully integrated real-time system**, culminating in an interactive **Streamlit dashboard** for live monitoring and fault prediction.

---

## 🎯 Objectives

* Monitor ESP health using electrical current signals
* Understand fault characteristics through signal analysis
* Develop a machine learning model for fault classification
* Integrate embedded hardware with real-time analytics
* Build an interactive dashboard for live system monitoring

---

## 🧠 Project Evolution

### 🔹 Phase 1: Signal Understanding (FFT-Based Exploration)

The initial phase focused on understanding how faults in an Electric Submersible Pump affect its electrical behavior.

#### Key Approach:

* Generated and analyzed signals representing:

  * Normal operation
  * Bearing-related faults
  * Cavitation
* Applied **windowing techniques** to segment signals
* Used **Fast Fourier Transform (FFT)** to analyze frequency components

#### Insight:

* Faults introduce **distinct frequency patterns** in the current signal
* Electrical signals can serve as a **proxy for mechanical conditions**

#### Outcome:

This phase provided the **foundation for feature understanding**, guiding the transition to real-world data and machine learning.

---

### 🔹 Phase 2: Real-World Data Acquisition (Embedded System)

The system was then extended to collect **real-time data from a physical DC pump setup**.

#### Hardware Components:

* ESP32 microcontroller
* Current sensor (INA219)
* Electric submersible pump system
* Power supply and load configuration

<img width="1280" height="960" alt="image" src="https://github.com/user-attachments/assets/a15163f9-3064-4fe6-9f62-6b7bb6d9e89a" />


#### Data Pipeline:

```
ESP Pump → Current Sensor → ESP32 → Serial/WiFi → Python Environment
```

#### Key Decision:

Although multiple parameters were available (voltage, power, time), the system was streamlined to use:

> **Current as the primary feature**, due to its direct relationship with load, stress, and fault conditions.

---

### 🔹 Phase 3: Machine Learning Model Development

Using the real-world current data, a deep learning model was trained to classify pump conditions.

---

## 🤖 Model Architecture & Training

### 📊 Data Preparation

* Dataset: `pump_data (2).csv`
* Cleaned by:

  * Removing null values and duplicates
  * Converting current values to numeric
  * Dropping irrelevant columns (Voltage, Time)

### 🔢 Label Encoding

Pump states were encoded using a label encoder:

```python
label_encoder = LabelEncoder()
df["State"] = label_encoder.fit_transform(df["State"])
```

---

### ⚙️ Feature Engineering

* Only **Current** was used as input feature
* Standardized using:

```python
StandardScaler()
```

Saved normalization parameters:

* `pump_norm_mean.npy`
* `pump_norm_std.npy`

---

### 🔄 Windowing Strategy

To capture temporal patterns:

* Window size: **50 samples**
* Step size: **10 samples (overlap)**

Each window is labeled using **majority voting** within the segment.

---

### 🧠 Model Architecture

A hybrid deep learning model combining **CNN + LSTM**:

```python
Conv1D → MaxPooling → LSTM → Dropout → Dense
```

#### Purpose:

* **Conv1D** → Extract local patterns in signal
* **LSTM** → Capture temporal dependencies
* **Dense Layer** → Perform classification

---

### 🏋️ Training Details

* Loss: `sparse_categorical_crossentropy`
* Optimizer: `Adam`
* Epochs: 30
* Batch size: 16

---

### 📈 Model Performance

* Achieved strong classification performance across pump states
* Evaluated using:

  * Accuracy
  * Classification report
  * Confusion matrix

Artifacts:

* `esp_model.h5`
* `esp_label_encoder.pkl`
* `rf_confusion_matrix.png`
* `lstm_training_history.png`

---

## ⚡ Real-Time Prediction System

The trained model is used in a real-time pipeline:

```
Live Current Data → Buffer → Windowing → Normalization → Model → Prediction
```

Predictions are:

* Generated continuously
* Logged into `realtime_predictions.csv`
* Displayed via dashboard

---

## 📊 Streamlit Dashboard

A fully functional **Streamlit dashboard (`dashboard.py`)** was built to:

* Visualize live current signals
* Display real-time fault predictions
* Show system status dynamically
* Enable intuitive monitoring of ESP behavior

<img width="1365" height="568" alt="Screenshot 2026-03-22 215102" src="https://github.com/user-attachments/assets/2c3c0c7c-bb9b-4172-bab3-0f41999b057c" />

<img width="1343" height="509" alt="Screenshot 2026-03-22 215120" src="https://github.com/user-attachments/assets/d09e3aa2-676a-42fd-9e7a-5ec3bfbf9f31" />


---

## ⚙️ System Architecture

```
ESP Pump → Sensor → ESP32 → Python → ML Model → Streamlit Dashboard
```

---

## 📁 Project Structure

```
ESP Project/
│
├── ESP_INTEGRATION.ipynb        # End-to-end pipeline integration
├── dashboard.py                # Streamlit dashboard
├── esp_model.h5                # Trained ML model
├── esp_label_encoder.pkl       # Label encoder
├── pump_norm_mean.npy          # Normalization mean
├── pump_norm_std.npy           # Normalization std
├── pump_data.csv               # Raw dataset
├── pump_data (2).csv           # Cleaned dataset
├── realtime_predictions.csv    # Live prediction logs
├── lstm_training_history.png   # Training visualization
├── rf_confusion_matrix.png     # Model evaluation
└── README.md                   # Documentation
```

---

## 🛠️ Technologies Used

* Python
* TensorFlow / Keras
* NumPy
* Pandas
* Scikit-learn
* Matplotlib
* PySerial
* Streamlit
* ESP32

---

## 💡 Key Insight

> Electrical current signals from an Electric Submersible Pump can effectively capture mechanical and operational anomalies, enabling a low-cost and scalable approach to predictive maintenance without relying on expensive sensors.

---

## 🚀 Future Work

* Deploy as a **standalone application** (beyond Streamlit)
* Implement **edge AI on ESP32 (TinyML)**
* Expand dataset with more fault conditions
* Integrate additional sensors (temperature, vibration)
* Deploy in real industrial ESP environments

---

## 👤 Author

This project reflects a deep exploration into:

* Embedded systems
* Signal processing
* Machine learning
* Real-time intelligent diagnostics

with a focus on solving real-world engineering problems.

---

## 📌 License

Open-source for research, learning, and development purposes.
