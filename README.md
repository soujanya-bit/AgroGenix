Agri-Advisor AI Suite
Welcome to Agri-Advisor AI Suite, an innovative platform designed to empower farmers and agricultural researchers with AI-driven crop recommendations and market insights. This dual-mode solution offers a simple, multilingual interface for farmers and an advanced analytics dashboard for experts, all accessible via a unified website.
Overview

Farmer Mode: A Streamlit-based application providing quick crop recommendations based on soil type, rainfall, season, and farmer priorities (sustainability or profit). Supports five languages: English, Hindi, Tamil, Telugu, and Kannada.
Advanced Mode: A React frontend with a FastAPI backend, leveraging pre-trained ML models for detailed soil, weather, and market predictions, including market forecasts.
Landing Page: A central HTML page linking to both modes for seamless access.

This project aims to transform agriculture by making data-driven decisions accessible to all, from small-scale farmers to agribusiness researchers.
Features

Farmer Mode: 

Soil-driven crop recommendations with a 70% weight on soil compatibility.
Top-three crop visualization with Matplotlib charts.
Multilingual support for broader reach.
Optional integration with advanced predictions via API.


Advanced Mode: 

Detailed predictions using pre-trained models (soil_predictor.pkl, weather_predictor.pkl, market_predictor.pkl, market_forecast_model.pkl).
Interactive React interface with charts powered by react-chartjs-2.
RESTful API endpoints for scalable data access.


Unified Access: Single landing page and one-click launch script.


Installation
Prerequisites

Python 3.9+
Node.js 16+
Git

Setup Instructions

Clone the Repository
git clone https://github.com/your-username/agri-advisor-ai-suite.git
cd agri-advisor-ai-suite


Install Backend Dependencies

Navigate to farmer_mode and install Python packages:cd farmer_mode
pip install -r requirements.txt


Navigate to advanced_mode/backend and install Python packages:cd ../advanced_mode/backend
pip install -r requirements.txt




Install Frontend Dependencies

Navigate to advanced_mode/frontend and install Node dependencies:cd ../frontend
npm install




Run the Suite

Execute the launch script to start all components:chmod +x launch.sh
./launch.sh


This starts:
Landing page: http://localhost:8001
Farmer Mode (Streamlit): http://localhost:8501
Advanced Mode Backend (FastAPI): http://localhost:8000
Advanced Mode Frontend (React): http://localhost:3000





Usage

Landing Page: Open http://localhost:8001 to access the main page and navigate to either mode.
Farmer Mode: Use the Streamlit app at http://localhost:8501 to input soil type, rainfall, season, and priority. Toggle between "Basic" and "Advanced" modes for recommendations.
Advanced Mode: Visit http://localhost:3000 to explore the React interface. Submit a prediction form to see detailed analysis and charts.

File Structure
agri-advisor-ai-suite/
├── farmer_mode/                      # Farmer-friendly interface (Streamlit)
│   ├── app.py                        # Streamlit main app
│   ├── soil_model/
│   │   ├── soil_predictor.pkl         # ML model for soil-based crop prediction
│   │   └── soil_utils.py              # Helper functions (rules, preprocessing)
│   ├── weather_model/
│   │   ├── weather_predictor.pkl
│   │   └── weather_utils.py
│   ├── market_model/
│   │   ├── market_predictor.pkl
│   │   └── market_utils.py
│   ├── data/
│   │   ├── soil_dataset.csv
│   │   ├── weather_dataset.csv
│   │   └── market_dataset.csv
│   ├── assets/
│   │   └── logo.png                   # Logo for app
│   └── requirements.txt               # Python dependencies
│
├── advanced_mode/                    # Advanced Analysis (Typescript frontend + Python backend)
│   ├── backend/
│   │   ├── app/
│   │   │   ├── _init_.py
│   │   │   ├── main.py                 # FastAPI backend
│   │   │   ├── models.py               # Load models
│   │   │   ├── utils.py                # Advanced processing functions
│   │   │   └── market_forecast_model.pkl
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   ├── frontend/
│   │   ├── public/
│   │   │   └── index.html
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── Navbar.tsx
│   │   │   │   ├── PredictionForm.tsx
│   │   │   │   └── MarketCharts.tsx
│   │   │   ├── pages/
│   │   │   │   ├── Home.tsx
│   │   │   │   └── Analysis.tsx
│   │   │   ├── services/
│   │   │   │   └── api.ts
│   │   │   ├── App.tsx
│   │   │   ├── main.tsx
│   │   │   └── styles/
│   │   │       └── App.css
│   │   ├── package.json
│   │   └── tsconfig.json
│
├── documentation/
│   ├── architecture_diagram.png       # Architecture overview
│   ├── data_flow_diagram.png           # Data Flow Chart
│   ├── README.md                       # Full Project Description
│
├── launch.sh                           # (Optional) One-click script to run both modes
├── LICENSE
└── README.md                           # Top-level README (how to run the project)

Technical Details

Farmer Mode: Built with Streamlit, uses SoilAnalyzer to process real-time crop data from crop_data.py. Scores are weighted 70% on soil fit, visualized with Matplotlib.
Advanced Mode: 
Backend: FastAPI serves predictions from pre-trained models, hosted on localhost:8000.
Frontend: React with TypeScript, using react-router-dom for navigation and react-chartjs-2 for charts.


Launch Script: Orchestrates all services with port assignments (8501 for Streamlit, 8000 for FastAPI, 3000 for React).

Contributing
We welcome contributions! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m "Add new feature").
Push to the branch (git push origin feature-branch).
Open a Pull Request with a clear description.

License
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

Thanks to the open-source community for tools like Streamlit, FastAPI, and React.
Inspired by the need to support India’s agricultural sector with AI innovation.

Contact
For questions or collaboration, reach out at your-email@example.com.
