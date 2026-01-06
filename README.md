# 🎯 RecruitIQ — Intelligent HR Analytics & Interview Evaluation Platform

RecruitIQ is an end-to-end Human Resource Intelligence system built to modernize how companies evaluate talent, predict workforce risks, and make data-driven hiring decisions. Designed for HR teams, interview panels, and decision-makers, RecruitIQ blends interactive dashboards, candidate scoring, session-based interview tracking, data visualization, and predictive analytics into a single unified platform.

## ✨ Features

### 🔍 1. Session-Based Interview Evaluation
- Create dedicated interview sessions for each hiring round
- Add candidate profiles with complete information
- Assign scores across standardized metrics:
  - Communication
  - Technical Skills
  - Projects
  - Problem Solving
  - Culture Fit
- Record detailed interviewer notes
- Automatic data storage for analytics & comparison

### 📊 2. Advanced Candidate Ranking Engine
- Rank candidates by any individual metric
- Display dynamic Top-N lists
- Comparative multi-metric visualization
- Normalized scores for fairness
- Non-destructive filtering (data never deleted)

### 🎨 3. Visual Intelligence for Hiring Decisions
- Single-parameter comparison charts
- Multi-parameter grouped bar charts
- Radar charts for skill distribution
- Performance heatmaps
- Score distribution analysis
- Real-time visualization updates

### 🧠 4. Predictive Analytics for HR
- Attrition risk prediction (ML-ready)
- Workforce stability & retention insights
- Promotion readiness analysis
- Employee performance cluster analysis
- Department-level workforce health overview

### 💾 5. Lightweight Local Database
- SQLite for local persistence
- Seamless candidate save functions
- Historical session integrity
- No data overwriting or forced deletions

### ⚡ 6. Built for Scalability & Extensibility
- Clean modular architecture
- Easy to add new metrics
- ML integration ready
- Database agnostic (easily switch to MySQL/Postgres)
- Modular authentication support
- Cloud/Docker deployment ready

### 🛡 7. Simple UI with Powerful Controls
- Clean, intuitive interface
- Card-based sections
- Responsive layout
- Easy navigation across modules
- High readability for decision-makers

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip package manager

### Installation

1. **Clone or download the repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run recrute.py
   ```

4. **Access the application:**
   - Open your browser and navigate to `http://localhost:8501`
   - The application will automatically create the database on first run

## 📁 Project Structure

```
RecruitIQ/
├── recrute.py              # Main entry point
├── src/
│   ├── __init__.py
│   ├── data.py             # Database operations & data management
│   ├── tab_interview.py    # Interview UI & evaluation logic
│   └── plots.py            # Visualization helpers
├── database/               # SQLite database (auto-created)
│   └── recruitiq.db
├── data/                   # Data storage (optional)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🗄️ Database Schema

### Sessions Table
```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    interviewer TEXT,
    date TEXT,
    notes TEXT
);
```

### Candidates Table
```sql
CREATE TABLE candidates (
    id TEXT PRIMARY KEY,
    session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
    name TEXT,
    email TEXT,
    phone TEXT,
    position TEXT,
    experience_years INTEGER,
    notes TEXT
);
```

### Scores Table
```sql
CREATE TABLE scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id TEXT REFERENCES candidates(id) ON DELETE CASCADE,
    metric TEXT NOT NULL,
    value REAL NOT NULL
);
```

## 📖 Usage Guide

### Creating a Session
1. Navigate to **Interview Evaluation** → **Session Management**
2. Fill in session details:
   - Session Name
   - Interviewer
   - Date
   - Position/Role
   - Notes (optional)
3. Click **Create Session**

### Adding Candidates
1. Select your session
2. Go to **Candidate Evaluation** tab
3. Fill in candidate information
4. Click **Add Candidate**

### Evaluating Candidates
1. Find the candidate in the list
2. Click **Score** button
3. Use sliders to assign scores (0-10) for each metric:
   - Communication
   - Technical Skills
   - Projects
   - Problem Solving
   - Culture Fit
4. Add interviewer notes
5. Click **Save Scores**

### Viewing Analytics
1. Navigate to **Analytics Dashboard**
2. Select a session
3. View key metrics and visualizations
4. Explore score distributions and comparisons

### Ranking Candidates
1. Go to **Candidate Ranking**
2. Select session
3. Choose ranking method:
   - Single Metric
   - Weighted Average
   - Composite Score
4. Set parameters and view rankings
5. Explore radar charts for detailed skill profiles

### Exporting Data
1. Navigate to **Data Management**
2. Select session to export
3. Click **Download as CSV**

## 🎨 Visualization Features

- **Multi-Metric Comparison**: Compare all candidates across all metrics
- **Score Distribution**: Analyze score distributions by metric
- **Performance Heatmap**: Visual heatmap of all scores
- **Radar Charts**: Individual candidate skill profiles
- **Ranking Charts**: Visual representation of rankings

## 🔧 Configuration

### Adding New Metrics
1. Edit `METRICS` list in `src/tab_interview.py`
2. The system will automatically adapt to new metrics

### Database Migration
To switch from SQLite to MySQL/Postgres:
1. Update connection functions in `src/data.py`
2. Adjust SQL syntax if needed
3. Update connection parameters

## 🤝 Contributing

Feel free to fork, modify, and extend RecruitIQ for your needs!

## 📝 License

This project is open source and available for use and modification.

## 🆘 Support

For issues or questions:
1. Check the documentation above
2. Review the code comments
3. Open an issue on the repository

## 🔮 Future Enhancements

- [ ] Machine learning models for attrition prediction
- [ ] Authentication and user management
- [ ] Cloud deployment configurations
- [ ] Advanced filtering and search
- [ ] Email notifications
- [ ] API integration
- [ ] Mobile responsive improvements
- [ ] Batch import/export
- [ ] Interview scheduling
- [ ] Integration with ATS systems

---

**Built with ❤️ for modern HR teams**
