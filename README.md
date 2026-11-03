# DeadZone 📡

### Wi-Fi Dead Zone Detection and Visualization System

DeadZone is a data-driven system designed to identify, analyze, and visualize Wi-Fi coverage dead zones within indoor environments.

The project aims to help users understand wireless signal coverage, detect areas with weak or no connectivity, and improve network coverage through data analysis and floor-plan visualization.

---

## 🎯 Project Overview

Wi-Fi connectivity is essential in modern environments, but wireless signals can become weak or unavailable in certain areas due to walls, obstacles, distance, and interference.

DeadZone addresses this problem by providing a system for analyzing wireless signal data and identifying potential dead zones.

The system combines data science, algorithms, backend APIs, and an interactive frontend to make Wi-Fi coverage analysis more accessible and understandable.

---

## ✨ Key Features

- **Wi-Fi Dead Zone Detection:** Identify areas with weak or unavailable wireless signals.
- **Signal Strength Analysis:** Analyze wireless signal measurements to understand coverage quality.
- **Floor Plan Management:** Upload and manage floor-plan images for indoor coverage analysis.
- **Coverage Visualization:** Visualize signal strength and potential dead zones on floor plans.
- **Project Management:** Create and manage individual network analysis projects.
- **Algorithm-Based Analysis:** Apply algorithms to process signal data and identify coverage issues.
- **Interactive Dashboard:** Provide an interface for managing projects and viewing analysis results.

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic

### Frontend
- React
- TypeScript
- Vite
- HTML
- CSS

### Data Science & Algorithms
- Python
- Data Analysis
- Signal Strength Analysis
- Dead Zone Detection Algorithms

### Development Tools
- Git
- GitHub
- Visual Studio Code
- Antigravity IDE

---

## 📂 Project Structure

```text
DeadZone/
│
├── algorithms/
│   └── Detection algorithms
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── API/
│   ├── services/
│   ├── models/
│   └── database/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── data/
│   └── Dataset and signal data
│
├── .gitignore
└── README.md
```

*Note: The directory structure may evolve as development progresses.*

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.12 or compatible version
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/DeadZone.git
```

Navigate to the project directory:

```bash
cd DeadZone
```

### 2. Set Up the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

**Windows:**

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Set Up the Frontend

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at the local URL provided by Vite, typically:

```text
http://localhost:5173
```

---

## 🔬 How It Works

The system is designed around the following workflow:

1. **Project Creation:** Create a project for a particular indoor environment.
2. **Floor Plan Upload:** Upload the floor plan of the environment.
3. **Signal Data Collection:** Obtain wireless signal measurements for different locations.
4. **Data Processing:** Process and analyze the collected signal data.
5. **Dead Zone Detection:** Identify locations where wireless coverage is weak or unavailable.
6. **Visualization:** Display coverage information and detected dead zones on the floor plan.
7. **Analysis:** Use the results to understand coverage problems and identify areas that may require improvement.

---

## 🎓 Academic Project

DeadZone is being developed as an academic project for the **Bachelor of Science in Data Science** program.

The project integrates concepts from:

- Data Science
- Computer Networks
- Data Structures and Algorithms
- Software Engineering
- Database Management Systems
- Web Development

The objective is to apply theoretical concepts to a practical problem involving wireless network coverage analysis.

---

## 📌 Project Status

🚧 **Currently in Development**

The project is being developed incrementally, with backend APIs, database integration, frontend implementation, and coverage analysis capabilities being built and tested through development sprints.

---

## 👨‍💻 Contributors

Developed as a collaborative academic project.

---

## 📄 License

No license has been selected yet.

---

**DeadZone — Making Wi-Fi Coverage Visible.**
