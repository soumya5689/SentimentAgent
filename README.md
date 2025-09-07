🚀 Project Overview
-----------------------

This project analyzes YouTube content to measure brand visibility and audience sentiment. It calculates Share of Voice (SOV) for a given search query (e.g., “Atomberg smart fan”) and provides sentiment insights from video comments.
The system generates charts, CSV reports, and API responses that can be integrated with any frontend dashboard.

✨ Features
-------------
🔎 Search YouTube Videos by keyword and fetch top N results.
📝 Analyze Comments for sentiment (positive, neutral, negative).
📈 Share of Voice (SOV) Calculation → % of videos mentioning the brand.
🥧 Visual Reports (Pie & Bar Charts in API response).
📂 CSV Export → Download full report of videos + sentiment.
🌐 REST API (FastAPI) → Can be connected to React frontend.
🎨 Frontend (React + Tailwind) → Input search query, view insights, download results.

🛠️ Tech Stack
---------------
Backend
Python (FastAPI, Pandas, Matplotlib)
YouTube Data API v3 (for fetching video & comment data)
VADER Sentiment Analysis
Frontend
React + Vite + TailwindCSS
Axios for API calls
Charts displayed from backend (base64 images)


📂 Project Structure
------------------------
backend/
│── main.py               # FastAPI app (API endpoints)
│── youtube_api.py        # YouTube API integration
│── sentiment.py          # Sentiment analysis logic
│── requirements.txt      # Dependencies
│── results.csv           # Auto-generated CSV output

frontend/
│── src/
│   ├── App.tsx           # React frontend logic
│   ├── components/       # UI components
│── public/
│   └── index.html        # Page title + favicon

⚙️ Setup & Installation
------------------------
1️⃣ Clone Repository
git clone https://github.com/your-username/atomberg-youtube-insights.git
cd atomberg-youtube-insights

2️⃣ Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
uvicorn main:app --reload
Runs at: http://127.0.0.1:8000

3️⃣ Frontend Setup
cd frontend
npm install
npm run dev


Runs at: http://localhost:5173

🔑 YouTube API Key
---------------------

Go to Google Cloud Console
Enable YouTube Data API v3.
Generate an API Key.
Replace the API_KEY in main.py with your key.

📊 Example API Usage
curl -X 'GET' \
  'http://127.0.0.1:8000/analyze?query=atomberg&results=20' \
  -H 'accept: application/json'

📷 Sample Output
Pie Chart → Share of Voice (Atomberg vs Others)
Bar Chart → Sentiment score per channel
CSV File → Detailed video-level data

📌 Future Improvements
-------------------------
Add support for other platforms (Twitter, Instagram).
Store results in a database (Postgres/MySQL).
Enhance sentiment analysis with transformer-based models.

👤 Author

Developed by Soumya Kanta Sahoo for Atomberg AI Internship Project.
✨ Focused on Marketing Insights, Analytics, and AI Applications.

