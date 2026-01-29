"""
Smart Advisor Tool - NUS Programme Recommendation System
Final Year Project by Jiajian (Mechanical Engineering, NUS CDE)

This application helps pre-university students discover NUS undergraduate programmes
that match their interests and values using the RIASEC framework.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple
import os

# Page configuration
st.set_page_config(
    page_title="NUS Smart Advisor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #003D7C;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stProgress > div > div > div > div {
        background-color: #003D7C;
    }
    .recommendation-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #003D7C;
        margin-bottom: 1rem;
    }
    .score-badge {
        background-color: #003D7C;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        display: inline-block;
        margin-left: 0.5rem;
    }
    .riasec-badge {
        background-color: #e9ecef;
        color: #495057;
        padding: 0.2rem 0.6rem;
        border-radius: 5px;
        font-size: 0.85rem;
        margin: 0.2rem;
        display: inline-block;
    }
    /* Vertical radio buttons */
    div[role="radiogroup"] {
        flex-direction: column !important;
    }
    div[role="radiogroup"] label {
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data function with caching
@st.cache_data
def load_data():
    """Load the Excel data file"""
    try:
        # Try relative path first (for deployment)
        data_path = 'data/SmartAdvisorTool_Data_V2_COMPLETE.xlsx'
        if not os.path.exists(data_path):
            # Try current directory
            data_path = 'SmartAdvisorTool_Data_V2_COMPLETE.xlsx'
        
        questions_df = pd.read_excel(data_path, sheet_name='Questions')
        programmes_df = pd.read_excel(data_path, sheet_name='Programmes')
        values_df = pd.read_excel(data_path, sheet_name='Values_Mapping')
        riasec_desc_df = pd.read_excel(data_path, sheet_name='RIASEC_Descriptions')
        
        return questions_df, programmes_df, values_df, riasec_desc_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

# RIASEC type full names
RIASEC_NAMES = {
    'R': 'Realistic',
    'I': 'Investigative', 
    'A': 'Artistic',
    'S': 'Social',
    'E': 'Enterprising',
    'C': 'Conventional'
}

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'results' not in st.session_state:
        st.session_state.results = None

def calculate_riasec_scores(responses: Dict[str, int], questions_df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate RIASEC scores from questionnaire responses
    FIXED: Now properly handles neutral (3) as 50% instead of 60%
    """
    riasec_scores = {'R': 0, 'I': 0, 'A': 0, 'S': 0, 'E': 0, 'C': 0}
    
    # Interest questions (Q1-Q24: 4 questions per RIASEC type)
    for q_id, response in responses.items():
        if q_id.startswith('Q') and int(q_id[1:]) <= 24:
            question = questions_df[questions_df['Question_ID'] == q_id].iloc[0]
            riasec_type = question['RIASEC_Type']
            # Scale: 1-5 (Strongly Disagree to Strongly Agree)
            # Convert to 0-4 scale first, then to percentage
            riasec_scores[riasec_type] += (response - 1)  # Now 0-4 scale
    
    # Normalize scores (0-100 scale)
    for code in riasec_scores:
        # Max score per type = 4 questions × 4 points = 16
        # So neutral (3) across all questions = 2*4 = 8, which is 50%
        riasec_scores[code] = (riasec_scores[code] / 16) * 100
    
    return riasec_scores

def get_top_riasec(riasec_scores: Dict[str, float], n: int = 3) -> List[str]:
    """Get top N RIASEC codes sorted by score"""
    sorted_codes = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)
    return [code for code, score in sorted_codes[:n]]

def get_top_values(responses: Dict[str, int], n: int = 3) -> List[str]:
    """Extract top values from questions Q25-Q29"""
    value_responses = {}
    value_mapping = {
        'Q25': 'high-salary',
        'Q26': 'helping-people',
        'Q27': 'creativity',
        'Q28': 'technology',
        'Q29': 'work-life-balance'
    }
    
    for q_id in ['Q25', 'Q26', 'Q27', 'Q28', 'Q29']:
        if q_id in responses:
            value_responses[value_mapping[q_id]] = responses[q_id]
    
    # Sort by score and get top N
    sorted_values = sorted(value_responses.items(), key=lambda x: x[1], reverse=True)
    return [value for value, score in sorted_values[:n]]

def match_programmes(riasec_scores: Dict[str, float], top_values: List[str], 
                    programmes_df: pd.DataFrame, top_n: int = 8) -> pd.DataFrame:
    """
    Match programmes using IMPROVED weighted RIASEC scoring
    
    IMPROVED Scoring system for better differentiation:
    - Student's 1st RIASEC matches Programme Primary: +5 points (increased from 3)
    - Student's 1st RIASEC matches Programme Secondary: +3 points (increased from 2)
    - Student's 2nd RIASEC matches Programme Primary: +3 points (increased from 2)
    - Student's 2nd RIASEC matches Programme Secondary: +2 points (increased from 1)
    - Student's 3rd RIASEC matches Programme Primary: +1 point (NEW)
    - Student's 2nd RIASEC matches Programme Tertiary: +1 point (increased from 0.5)
    - Student's top value matches Programme value tag: +1.5 points per match (increased from 1)
    - Bonus: Top 2 RIASEC both match top 2 programme codes: +2 bonus points (NEW)
    """
    top_riasec = get_top_riasec(riasec_scores, n=3)
    
    scores = []
    for idx, row in programmes_df.iterrows():
        score = 0
        match_details = []
        
        # RIASEC matching
        prog_primary = row['Primary_RIASEC']
        prog_secondary = row['Secondary_RIASEC']
        prog_tertiary = row['Tertiary_RIASEC'] if pd.notna(row['Tertiary_RIASEC']) else None
        
        # Student's 1st RIASEC
        if top_riasec[0] == prog_primary:
            score += 5
            match_details.append(f"Your top interest ({RIASEC_NAMES[top_riasec[0]]}) matches the programme's primary focus")
        elif top_riasec[0] == prog_secondary:
            score += 3
            match_details.append(f"Your top interest ({RIASEC_NAMES[top_riasec[0]]}) matches a key component")
        
        # Student's 2nd RIASEC
        if len(top_riasec) > 1:
            if top_riasec[1] == prog_primary:
                score += 3
                match_details.append(f"Your secondary interest ({RIASEC_NAMES[top_riasec[1]]}) matches the programme's primary focus")
            elif top_riasec[1] == prog_secondary:
                score += 2
                match_details.append(f"Your secondary interest ({RIASEC_NAMES[top_riasec[1]]}) matches a component")
            elif prog_tertiary and top_riasec[1] == prog_tertiary:
                score += 1
                match_details.append(f"Your secondary interest ({RIASEC_NAMES[top_riasec[1]]}) aligns with programme aspects")
        
        # Student's 3rd RIASEC
        if len(top_riasec) > 2:
            if top_riasec[2] == prog_primary:
                score += 1
                match_details.append(f"Your third interest ({RIASEC_NAMES[top_riasec[2]]}) matches the programme focus")
        
        # Bonus for perfect top-2 match
        prog_top2 = [prog_primary, prog_secondary]
        if len(top_riasec) >= 2 and top_riasec[0] in prog_top2 and top_riasec[1] in prog_top2:
            score += 2
            match_details.append("Strong alignment: Your top 2 interests match this programme's core profile")
        
        # Value matching (increased weight)
        if pd.notna(row['Value_Tags']):
            prog_values = [v.strip() for v in str(row['Value_Tags']).split(',')]
            value_matches = []
            for val in top_values:
                if val in prog_values:
                    score += 1.5
                    value_matches.append(val)
            if value_matches:
                match_details.append(f"Shares your values: {', '.join(value_matches)}")
        
        scores.append({
            'Programme_ID': row['Programme_ID'],
            'Programme_Name': row['Programme_Name'],
            'Faculty': row['Faculty'],
            'Primary_RIASEC': prog_primary,
            'Secondary_RIASEC': prog_secondary,
            'Tertiary_RIASEC': prog_tertiary,
            'Value_Tags': row['Value_Tags'],
            'Match_Score': score,
            'Match_Details': match_details
        })
    
    # Convert to DataFrame and sort by score
    results_df = pd.DataFrame(scores)
    results_df = results_df.sort_values('Match_Score', ascending=False).head(top_n)
    
    return results_df

def show_welcome_page():
    """Display welcome page"""
    st.markdown('<div class="main-header">🎓 NUS Smart Advisor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Discover Your Best-Fit NUS Undergraduate Programme</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### Welcome! 👋
        
        This tool will help you discover NUS undergraduate programmes that match your:
        - **Interests** (what you enjoy doing)
        - **Work Style** (how you like to work)
        - **Values** (what matters to you in a career)
        
        #### How it works:
        1. **Answer 29 questions** (takes about 5-7 minutes)
        2. **Get your RIASEC profile** (your interest type)
        3. **See your top 8 programme matches** with explanations
        
        #### What is RIASEC?
        RIASEC is a research-backed framework that identifies 6 interest types:
        - **R**ealistic - hands-on, mechanical work
        - **I**nvestigative - research, analysis
        - **A**rtistic - creative expression
        - **S**ocial - helping people
        - **E**nterprising - leading, persuading
        - **C**onventional - organizing, data
        
        ---
        """)
        
        st.info("💡 **Tip:** Answer honestly based on what genuinely interests you, not what you think you *should* like.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Start Questionnaire", type="primary", use_container_width=True):
            st.session_state.page = 'questionnaire'
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.expander("📊 About This Tool"):
            st.markdown("""
            This Smart Advisor Tool was developed as a Final Year Project by Jiajian 
            (Mechanical Engineering, NUS CDE) to help pre-university students make 
            informed decisions about their programme choices.
            
            The tool uses:
            - **Holland's RIASEC Theory** for interest assessment
            - **Person-Environment Fit** research for matching
            - Data on all **75 NUS undergraduate programmes**
            
            All recommendations are based on academic research in career counseling 
            and vocational psychology.
            """)

def show_questionnaire_page(questions_df):
    """Display questionnaire page - IMPROVED with vertical layout and no default"""
    st.markdown('<div class="main-header">📝 Questionnaire</div>', unsafe_allow_html=True)
    
    # Progress bar
    total_questions = len(questions_df)
    current = st.session_state.current_question
    progress = current / total_questions
    
    st.progress(progress)
    st.markdown(f"**Question {current + 1} of {total_questions}**")
    
    # Display current question
    question = questions_df.iloc[current]
    q_id = question['Question_ID']
    category = question['Category']
    text = question['Question_Text']
    
    st.markdown(f"### {category}")
    st.markdown(f"*{text}*")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Response options - FIXED: No default selection, vertical layout
    response = st.radio(
        "How much do you agree with this statement?",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {
            1: "😟 Strongly Disagree",
            2: "🙁 Disagree", 
            3: "😐 Neutral",
            4: "🙂 Agree",
            5: "😃 Strongly Agree"
        }[x],
        index=None,  # FIXED: No default selection
        key=f"q_{q_id}_{current}",  # Unique key per question
        horizontal=False  # FIXED: Vertical layout
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            if st.session_state.responses:
                st.warning("⚠️ You will lose your progress. Are you sure?")
            st.session_state.page = 'welcome'
            st.session_state.responses = {}
            st.session_state.current_question = 0
            st.rerun()
    
    with col3:
        if current < total_questions - 1:
            if st.button("Next ➡️", type="primary", use_container_width=True, disabled=(response is None)):
                if response is not None:
                    st.session_state.responses[q_id] = response
                    st.session_state.current_question += 1
                    st.rerun()
        else:
            if st.button("✅ See Results", type="primary", use_container_width=True, disabled=(response is None)):
                if response is not None:
                    st.session_state.responses[q_id] = response
                    st.session_state.page = 'results'
                    st.rerun()

def show_results_page(questions_df, programmes_df, riasec_desc_df):
    """Display results page"""
    st.markdown('<div class="main-header">🎯 Your Results</div>', unsafe_allow_html=True)
    
    # Calculate scores
    riasec_scores = calculate_riasec_scores(st.session_state.responses, questions_df)
    top_riasec = get_top_riasec(riasec_scores, n=3)
    top_values = get_top_values(st.session_state.responses, n=3)
    
    # Match programmes
    matches = match_programmes(riasec_scores, top_values, programmes_df, top_n=8)
    
    # Display RIASEC Profile
    st.markdown("## 📊 Your RIASEC Profile")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Radar chart
        categories = list(RIASEC_NAMES.values())
        scores = [riasec_scores[code] for code in RIASEC_NAMES.keys()]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            fillcolor='rgba(0, 61, 124, 0.2)',
            line=dict(color='#003D7C', width=2)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Your Top Interests:")
        for i, code in enumerate(top_riasec, 1):
            name = RIASEC_NAMES[code]
            score = riasec_scores[code]
            desc = riasec_desc_df[riasec_desc_df['Code'] == code].iloc[0]['Description']
            
            st.markdown(f"""
            **{i}. {name} ({code}) - {score:.1f}%**  
            {desc}
            """)
        
        st.markdown("### Your Top Values:")
        for i, value in enumerate(top_values, 1):
            st.markdown(f"{i}. {value.replace('-', ' ').title()}")
    
    st.markdown("---")
    
    # Display programme recommendations
    st.markdown("## 🎓 Your Top Programme Matches")
    st.markdown("*These programmes best align with your interests and values*")
    
    for rank, (idx, row) in enumerate(matches.iterrows(), 1):
        # Programme recommendation card
        st.markdown(f"""
        <div class="recommendation-card">
            <h3>{rank}. {row['Programme_Name']} 
                <span class="score-badge">Match: {row['Match_Score']:.1f} points</span>
            </h3>
            <p><strong>Faculty:</strong> {row['Faculty']}</p>
            <p>
                <strong>RIASEC Profile:</strong> 
                <span class="riasec-badge">{row['Primary_RIASEC']} - {RIASEC_NAMES[row['Primary_RIASEC']]}</span>
                <span class="riasec-badge">{row['Secondary_RIASEC']} - {RIASEC_NAMES[row['Secondary_RIASEC']]}</span>
                {f'<span class="riasec-badge">{row["Tertiary_RIASEC"]} - {RIASEC_NAMES[row["Tertiary_RIASEC"]]}</span>' if pd.notna(row['Tertiary_RIASEC']) else ''}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Expandable match details
        with st.expander("📋 Why this match?"):
            st.markdown("**Match Reasons:**")
            for detail in row['Match_Details']:
                st.markdown(f"- {detail}")
            
            st.markdown(f"\n**Programme Values:** {row['Value_Tags']}")
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Retake Quiz", use_container_width=True):
            st.session_state.page = 'welcome'
            st.session_state.responses = {}
            st.session_state.current_question = 0
            st.rerun()
    
    with col2:
        # Export results - FIXED: Remove programme ID numbers
        results_text = f"""NUS SMART ADVISOR - YOUR RESULTS

YOUR RIASEC PROFILE:
1. {RIASEC_NAMES[top_riasec[0]]} ({riasec_scores[top_riasec[0]]:.1f}%)
2. {RIASEC_NAMES[top_riasec[1]]} ({riasec_scores[top_riasec[1]]:.1f}%)
3. {RIASEC_NAMES[top_riasec[2]]} ({riasec_scores[top_riasec[2]]:.1f}%)

YOUR TOP VALUES:
{', '.join([v.replace('-', ' ').title() for v in top_values])}

YOUR TOP PROGRAMME MATCHES:
"""
        for rank, (idx, row) in enumerate(matches.iterrows(), 1):
            # FIXED: Use rank number instead of programme ID
            results_text += f"\n{rank}. {row['Programme_Name']} ({row['Faculty']}) - Match Score: {row['Match_Score']:.1f}\n"
        
        st.download_button(
            label="📥 Download Results",
            data=results_text,
            file_name="nus_smart_advisor_results.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col3:
        if st.button("ℹ️ About Results", use_container_width=True):
            st.info("""
            **How matching works:**
            - Your top 3 RIASEC interests are matched against each programme's profile
            - Primary matches score higher than secondary matches
            - Perfect alignment bonus for top-2 matches
            - Your values are matched against programme characteristics
            - Programmes are ranked by total match score
            
            **Scoring scale:**
            - 10-15 points: Excellent match
            - 7-10 points: Very good match
            - 5-7 points: Good match
            - Below 5 points: Moderate match
            
            **Next steps:**
            - Research your top matches on the NUS website
            - Talk to current students in these programmes
            - Consider your academic strengths and interests
            - Apply to programmes that excite you!
            """)

def main():
    """Main application logic"""
    init_session_state()
    
    # Load data
    questions_df, programmes_df, values_df, riasec_desc_df = load_data()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎓 NUS Smart Advisor")
        st.markdown("---")
        
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'welcome'
            st.rerun()
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        **Smart Advisor Tool**  
        Version 1.0
        
        Developed by Jiajian  
        (Mechanical Engineering, NUS CDE)
        
        Final Year Project 2025/26
        """)
        
        st.markdown("---")
        st.markdown("### Quick Stats")
        st.metric("Total Programmes", len(programmes_df))
        st.metric("Questions", len(questions_df))
        
        if st.session_state.responses:
            st.metric("Progress", f"{len(st.session_state.responses)}/{len(questions_df)}")
    
    # Main content
    if st.session_state.page == 'welcome':
        show_welcome_page()
    elif st.session_state.page == 'questionnaire':
        show_questionnaire_page(questions_df)
    elif st.session_state.page == 'results':
        show_results_page(questions_df, programmes_df, riasec_desc_df)

if __name__ == "__main__":
    main()
