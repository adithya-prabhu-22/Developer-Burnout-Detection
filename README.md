Developer Burnout Detection via Git Commit Mining

A Data Mining project that analyzes public GitHub repository commit behavior to estimate developer burnout risk using behavioral pattern mining, anomaly detection, and machine learning.

Overview

This project mines developer activity patterns from Git commit history and identifies potential burnout risk indicators such as:

Late-night coding activity
Negative commit messages
Short low-effort commits
Irregular development behavior
Anomalous commit patterns

The system uses:

GitHub REST API
Feature Engineering
Isolation Forest
Streamlit Dashboard
Docker Deployment
Features
Analyze any public GitHub repository
Fetch real commit history using GitHub API
Detect late-night coding patterns
Mine negative sentiment commit messages
Generate burnout risk scores
Detect anomalous behavior using Isolation Forest
Interactive Streamlit dashboard
Dockerized deployment for cloud hosting
Tech Stack
Technology	Purpose
Python	Core backend
Streamlit	Frontend dashboard
Pandas	Data processing
Scikit-learn	Isolation Forest ML model
Matplotlib	Data visualization
GitHub REST API	Commit data collection
Docker	Deployment
Project Structure
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
How It Works
1. Data Collection

The system fetches commit history from public GitHub repositories using the GitHub REST API.

Collected data includes:

Commit timestamps
Commit messages
Author information
2. Feature Engineering

The following burnout-related features are extracted:

Feature	Description
Commit Hour	Detects late-night coding activity
Message Length	Identifies low-effort commits
Negative Score	Counts stress-related keywords
Late Night Activity	Commit between 10 PM – 4 AM
Short Message	Commit message length < 20
3. Burnout Risk Scoring

A weighted burnout score is computed using behavioral indicators.

Example:

Burnout Score =
Late Night * 3 +
Negative Sentiment * 2 +
Short Message * 1
4. Anomaly Detection

The project uses Isolation Forest to identify unusual developer behavior patterns.

Isolation Forest detects commits that significantly deviate from normal activity.

Installation
Clone Repository
git clone https://github.com/YOUR_USERNAME/Developer-Burnout-Detection.git

cd Developer-Burnout-Detection
Install Dependencies
pip install -r requirements.txt
Run Locally
streamlit run app.py

Open:

http://localhost:8501
Docker Deployment
Build Docker Image
docker build -t burnout-detector .
Run Docker Container
docker run -d -p 8501:8501 burnout-detector
AWS EC2 Deployment
Launch Ubuntu EC2 instance
Install Docker
Clone repository
Build Docker image
Run container
Open port 8501 in security group

Access application:

http://PUBLIC_IP:8501
Example Repository URLs
https://github.com/pallets/flask

https://github.com/tensorflow/tensorflow

https://github.com/streamlit/streamlit
Disclaimer

This project does not clinically diagnose burnout or mental health conditions.

It only estimates behavioral burnout risk patterns from Git commit activity using data mining and anomaly detection techniques.

Future Improvements
Contributor-wise burnout analysis
Advanced NLP sentiment models
Time-series forecasting
Real-time monitoring dashboard
Random Forest classification
GitHub OAuth integration
Kubernetes deployment
Historical trend analysis
Data Mining Concepts Used
Temporal Pattern Mining
Feature Engineering
Anomaly Detection
Behavioral Analytics
Time-Series Analysis
Machine Learning
NLP-based Feature Extraction
Author

Adithya Prabhu
National Institute of Engineering, Mysuru