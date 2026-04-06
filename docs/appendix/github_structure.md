# Appendix E: GitHub Repository Structure

[← Back to Main Report](../index.md)

---

## Repository Overview

**Repository URL:** [https://github.com/JiajianZh/CDE4301-Smart-Advisor-Tool](https://github.com/JiajianZh/CDE4301-Smart-Advisor-Tool)

**Primary Branch:** main

**Deployment:** Continuous deployment to Streamlit Cloud (auto-updates on push to main branch)

---

## Directory Structure

```
CDE4301-Smart-Advisor-Tool/
│
├── README.md                                      # Project overview, quick start guide
├── app.py                                         # Main Streamlit application (~1750 lines)
├── requirements.txt                               # Python dependencies
├── .streamlit/
│   └── config.toml                               # Streamlit configuration
│
├── SmartAdvisorTool_Data_V2_COMPLETE.xlsx        # Programme database (4 sheets)
│
├── docs/                                         # GitHub Pages documentation
│   ├── index.md                                  # Full FYP report (this document)
│   ├── _config.yml                               # GitHub Pages theme configuration
│   │
│   ├── images/                                   # Application screenshots
│   │   ├── welcome-page.png
│   │   ├── questionnaire.png
│   │   ├── riasec-radar.png
│   │   ├── top-matches.png
│   │   ├── drill-down-trigger.png
│   │   ├── drill-down-questions.png
│   │   └── final-recommendation.png
│   │
│   └── appendix/                                 # Appendix documentation
│       ├── questionnaire.md                      # Complete questionnaire
│       ├── programme-coding.md                   # RIASEC coding examples
│       ├── algorithm.md                          # Algorithm pseudocode
│       ├── test-cases.md                         # Test documentation
│       ├── github-structure.md                   # This file
│       ├── deployment.md                         # Deployment guide
│       └── survey-results.md                     # Survey data
│
└── .gitignore                                    # Git ignore rules
```

---

## Key Files Explained

### `app.py`

**Size:** ~1750 lines of Python code

**Structure:**

```python
# Imports and setup
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuration
st.set_page_config(...)

# Data loading
@st.cache_data
def load_data():
    # Load Excel sheets
    programmes_df = pd.read_excel(...)
    questions_df = pd.read_excel(...)
    return programmes_df, questions_df

# Core functions
def calculate_riasec_profile(responses):
    # Convert 24 responses to 6 RIASEC scores
    ...

def calculate_match_scores(riasec_profile, values, programmes_df):
    # Implement scoring algorithm
    ...

def check_drill_down_trigger(top_results):
    # Detect faculty clustering
    ...

def run_drill_down(faculty, drill_down_responses):
    # Faculty-specific scoring
    ...

# Drill-down configurations (CDE, Computing, Business, etc.)
CDE_DRILL_DOWN = {
    "questions": [...],
    "programme_mappings": {...},
    "identity_statements": {...}
}

# Streamlit UI flow
if st.session_state.page == "welcome":
    # Welcome page with developer mode
    ...
elif st.session_state.page == "questionnaire":
    # 29-question survey with auto-advance
    ...
elif st.session_state.page == "results":
    # RIASEC radar chart + top matches
    ...
elif st.session_state.page == "drill_down":
    # Faculty-specific questions
    ...
elif st.session_state.page == "final_result":
    # Best-fit recommendation
    ...
```

**Key features implemented:**
- Session state management for multi-page flow
- Auto-advance questionnaire (0.4s delay)
- RIASEC radar chart (Plotly)
- Developer test mode (6 preset profiles)
- Drill-down trigger detection
- Identity statement generation

---

### `SmartAdvisorTool_Data_V2_COMPLETE.xlsx`

**Sheet 1: Programmes** (75 rows)

| Column | Description | Example |
|--------|-------------|---------|
| Programme | Official programme name | "Mechanical Engineering" |
| Faculty | NUS faculty | "College of Design and Engineering" |
| Primary | Primary RIASEC code | "R" |
| Secondary | Secondary RIASEC code | "I" |
| Tertiary | Tertiary RIASEC code (optional) | "" |
| Values | Comma-separated value tags | "technology,innovation,problem-solving" |

**Sheet 2: Questions** (29 rows)

| Column | Description | Example |
|--------|-------------|---------|
| Question_ID | Unique identifier | "R1" |
| Question_Text | Question wording | "I enjoy working with tools..." |
| RIASEC_Type | Type this question measures | "R" |

**Sheet 3: Values_Mapping** (5 rows)

| Column | Description | Example |
|--------|-------------|---------|
| Value_ID | Unique identifier | "V1" |
| Value_Name | Value keyword | "high-salary" |
| Value_Description | Full description | "Earning high income and having stable..." |

**Sheet 4: RIASEC_Descriptions** (6 rows)

| Column | Description | Example |
|--------|-------------|---------|
| Type | RIASEC letter | "R" |
| Full_Name | Type name | "Realistic" |
| Description | Type explanation | "Hands-on, practical, mechanical work" |

---

### `requirements.txt`

```
streamlit==1.31.0
pandas==2.1.4
plotly==5.18.0
openpyxl==3.1.2
```

**Purpose:** Specifies exact Python package versions for reproducible deployment.

---

### `README.md`

**Contents:**
- Project title and description
- Live application link
- Quick start instructions
- Technology stack
- Repository structure overview
- Developer test mode access code
- Contact information

**Target audience:** GitHub visitors, potential users, recruiters

---

### `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#0066CC"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

**Purpose:** Customizes Streamlit interface colors and fonts.

---

## Version Control Practices

### Commit History

**Major commits:**

1. `Initial commit: Basic HTML prototype` (Oct 2025)
2. `Migrate to Streamlit, add 35 programmes` (Nov 2025)
3. `Implement weighted scoring algorithm` (Nov 2025)
4. `Add CDE drill-down (15 programmes)` (Dec 2025)
5. `Expand to all 75 programmes` (Jan 2026)
6. `Add remaining 5 faculty drill-downs` (Feb 2026)
7. `Fix Computer Engineering classification bug` (Feb 2026)
8. `Add developer test mode` (Mar 2026)
9. `Final refinements for FYP submission` (Apr 2026)

### Branching Strategy

**main branch:** Production-ready code deployed to Streamlit Cloud

**Development workflow:**
1. Make changes locally in VS Code
2. Test thoroughly with developer mode
3. Commit to main branch via VS Code Source Control
4. Push to GitHub
5. Streamlit Cloud auto-deploys within 2 minutes

**No feature branches used:** As a solo developer project, all work done directly on main with careful testing before commits.

---

## Code Quality

**Linting:** Not enforced (Streamlit does not require strict linting)

**Documentation:** Inline comments explain complex logic blocks

**Code style:** PEP 8 mostly followed (automatic formatting via VS Code)

**Testing:** Manual testing via developer mode (no unit tests written)

---

## Data Management

**Why Excel instead of database?**

1. **Simplicity:** No database setup, credentials, or hosting costs
2. **Transparency:** Anyone can open the Excel file and see programme codings
3. **Version control:** Git tracks changes to programme data over time
4. **Easy updates:** Edit Excel file, commit, push → changes go live
5. **Small scale:** 75 programmes + 29 questions = <100 KB file size

**Data update workflow:**

1. Open `SmartAdvisorTool_Data_V2_COMPLETE.xlsx` in Excel
2. Modify programme codings, questions, or values
3. Save Excel file
4. Commit via VS Code: "Update programme X RIASEC coding"
5. Push to GitHub
6. Streamlit redeploys with new data automatically

---

## License

**Repository visibility:** Public

**License:** No formal license (all rights reserved to author)

**Open source considerations:** Code is visible but not explicitly licensed for reuse. Future consideration: Add MIT or Apache 2.0 license for broader adoption.

---

[← Back to Main Report](../index.md)
