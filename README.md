# Developer Burnout Detection via Git Commit Mining

A Data Mining project that analyzes public GitHub repository commit behavior to estimate developer burnout risk using behavioral pattern mining, anomaly detection, and machine learning.

---

# Overview

This project mines developer activity patterns from Git commit history and identifies potential burnout-risk indicators such as:

* Late-night coding activity
* Negative commit messages
* Short low-effort commits
* Irregular development behavior
* High coding intensity periods
* Long inactivity gaps
* Abnormal commit patterns

The system combines:

* Temporal Pattern Mining
* Feature Engineering
* Isolation Forest Anomaly Detection
* Behavioral Analytics
* Time-Series Analysis
* Streamlit Visualization
* Dockerized Cloud Deployment

---

# Features

* Analyze any public GitHub repository
* Fetch real commit history using GitHub REST API
* Detect late-night coding patterns
* Mine negative sentiment commit messages
* Analyze inter-commit inactivity gaps
* Detect daily and weekly coding intensity
* Analyze diff size using GitHub commit statistics
* Generate burnout risk scores
* Detect anomalous behavior using Isolation Forest
* Professional multi-tab analytics dashboard
* Dockerized deployment for cloud hosting
* Public AWS EC2 deployment

---

# Tech Stack

| Technology      | Purpose                   |
| --------------- | ------------------------- |
| Python          | Core backend              |
| Streamlit       | Frontend dashboard        |
| Pandas          | Data processing           |
| Scikit-learn    | Isolation Forest ML model |
| Matplotlib      | Data visualization        |
| GitHub REST API | Commit data collection    |
| Docker          | Containerized deployment  |
| AWS EC2         | Cloud hosting             |

---

# Project Structure

```text
Developer-Burnout-Detection/
│
├── app.py
├── github_fetcher.py
├── feature_engineering.py
├── burnout_model.py
├── utils.py
├── requirements.txt
├── Dockerfile
├── README.md
└── .gitignore
```

---

# How It Works

## 1. Data Collection

The system fetches commit history from public GitHub repositories using the GitHub REST API.

Collected data includes:

* Commit timestamps
* Commit messages
* Author information
* Lines added
* Lines deleted
* Total diff size

---

## 2. Feature Engineering

The following behavioral burnout-related features are extracted:

| Feature                 | Description                                 |
| ----------------------- | ------------------------------------------- |
| Commit Hour             | Detects late-night coding activity          |
| Message Length          | Identifies low-effort commits               |
| Negative Score          | Counts stress-related keywords              |
| Late Night Activity     | Commit between 10 PM – 4 AM                 |
| Short Message           | Commit message length < 20                  |
| Inter-commit Gap        | Measures inactivity periods between commits |
| Daily Commit Frequency  | Detects unusually high activity days        |
| Weekly Commit Frequency | Detects sustained coding intensity          |
| Diff Size               | Measures lines added/deleted in commits     |

---

## 3. Burnout Risk Scoring

A weighted burnout score is computed using behavioral indicators.

Example:

```text
Burnout Score =
Late Night Activity * 3 +
Negative Sentiment * 2 +
Short Message * 1 +
High Daily Activity * 2 +
Long Inactivity Gap * 2 +
Very Small Diff Size * 1
```

---

## 4. Anomaly Detection

The project uses Isolation Forest to identify unusual developer behavior patterns.

Isolation Forest detects commits that significantly deviate from normal behavioral activity.

Detected anomalies may indicate:

* irregular work behavior
* extreme coding bursts
* inconsistent activity
* suspicious burnout-like patterns

---

# Dashboard Analytics

The Streamlit dashboard provides:

* Burnout risk timeline visualization
* Commit activity analytics
* Daily commit frequency analysis
* Inter-commit gap analysis
* Diff size analytics
* Risk distribution visualization
* Isolation Forest anomaly reports
* Full commit-level behavioral analysis tables

---

# Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Developer-Burnout-Detection.git

cd Developer-Burnout-Detection
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Locally

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# Docker Deployment

## Build Docker Image

```bash
docker build -t burnout-detector .
```

---

## Run Docker Container

```bash
docker run -d -p 8501:8501 burnout-detector
```

---

# AWS EC2 Deployment

1. Launch Ubuntu EC2 instance
2. Install Docker
3. Clone repository
4. Build Docker image
5. Run container
6. Open port `8501` in EC2 security group

Access application:

```text
http://PUBLIC_IP:8501
```

---

# Example Repository URLs

```text
https://github.com/pallets/flask

https://github.com/tensorflow/tensorflow

https://github.com/streamlit/streamlit
```

---

# Future Improvements

* Contributor-wise burnout analysis
* Advanced NLP sentiment analysis using VADER/TextBlob
* Time-series forecasting
* Random Forest burnout classification
* Historical developer trend analysis
* Real-time monitoring dashboard
* GitHub OAuth integration
* Kubernetes deployment
* Multi-repository analytics
* Team-level burnout analysis

---

# Data Mining Concepts Used

* Temporal Pattern Mining
* Feature Engineering
* Behavioral Analytics
* Anomaly Detection
* Isolation Forest
* Time-Series Analysis
* NLP-based Feature Extraction
* Commit Pattern Mining
* Statistical Risk Scoring
* Software Repository Mining

---

# Disclaimer

This project does not clinically diagnose burnout or mental health conditions.

It only estimates behavioral burnout-risk patterns from Git commit activity using data mining and anomaly detection techniques.

---

# Author

Adithya Prabhu
National Institute of Engineering, Mysuru
