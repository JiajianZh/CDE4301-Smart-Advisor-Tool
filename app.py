"""
Smart Advisor Tool - NUS Programme Recommendation System
Final Year Project by Jiajian (Mechanical Engineering, NUS CDE)

This application helps pre-university students discover NUS undergraduate programmes
that match their interests and values using the RIASEC framework.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, List
import os
import time

# Page configuration
st.set_page_config(
    page_title="NUS Smart Advisor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
    div[role="radiogroup"] {
        flex-direction: column !important;
    }
    div[role="radiogroup"] label {
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():
    try:
        data_path = 'data/SmartAdvisorTool_Data_V2_COMPLETE.xlsx'
        if not os.path.exists(data_path):
            data_path = 'SmartAdvisorTool_Data_V2_COMPLETE.xlsx'
        questions_df = pd.read_excel(data_path, sheet_name='Questions')
        programmes_df = pd.read_excel(data_path, sheet_name='Programmes')
        values_df = pd.read_excel(data_path, sheet_name='Values_Mapping')
        riasec_desc_df = pd.read_excel(data_path, sheet_name='RIASEC_Descriptions')
        return questions_df, programmes_df, values_df, riasec_desc_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()


# ============================================================
# CONSTANTS
# ============================================================

RIASEC_NAMES = {
    'R': 'Realistic',
    'I': 'Investigative',
    'A': 'Artistic',
    'S': 'Social',
    'E': 'Enterprising',
    'C': 'Conventional'
}

TEST_PROFILES = {
    # R=100%, I=75% — strongly physical/hands-on + analytical
    # Pushes CDE engineering programmes to top 5
    "Engineering/CDE (R+I)": {
        'Q1': 5, 'Q2': 5, 'Q3': 5, 'Q4': 5,   # R = 100%
        'Q5': 4, 'Q6': 4, 'Q7': 4, 'Q8': 4,   # I = 75%
        'Q9': 1, 'Q10': 1, 'Q11': 1, 'Q12': 1, # A = 0%
        'Q13': 1, 'Q14': 1, 'Q15': 1, 'Q16': 1, # S = 0%
        'Q17': 2, 'Q18': 2, 'Q19': 2, 'Q20': 2, # E = 25%
        'Q21': 2, 'Q22': 2, 'Q23': 2, 'Q24': 2, # C = 25%
        'Q25': 4, 'Q26': 1, 'Q27': 2, 'Q28': 5, 'Q29': 3
    },
    # E=100%, C=75% — strongly enterprising + systematic
    # Pushes Business programmes to top 5
    "Business (E+C)": {
        'Q1': 1, 'Q2': 1, 'Q3': 1, 'Q4': 1,   # R = 0%
        'Q5': 2, 'Q6': 2, 'Q7': 2, 'Q8': 2,   # I = 25%
        'Q9': 2, 'Q10': 2, 'Q11': 2, 'Q12': 2, # A = 25%
        'Q13': 3, 'Q14': 3, 'Q15': 3, 'Q16': 3, # S = 50%
        'Q17': 5, 'Q18': 5, 'Q19': 5, 'Q20': 5, # E = 100%
        'Q21': 4, 'Q22': 4, 'Q23': 4, 'Q24': 4, # C = 75%
        'Q25': 5, 'Q26': 2, 'Q27': 3, 'Q28': 3, 'Q29': 3
    },
    # A=100%, S=75% — strongly creative + people-oriented
    # Pushes Humanities/Arts programmes to top 5
    "Humanities/Arts (A+S)": {
        'Q1': 1, 'Q2': 1, 'Q3': 1, 'Q4': 1,   # R = 0%
        'Q5': 2, 'Q6': 2, 'Q7': 2, 'Q8': 2,   # I = 25%
        'Q9': 5, 'Q10': 5, 'Q11': 5, 'Q12': 5, # A = 100%
        'Q13': 4, 'Q14': 4, 'Q15': 4, 'Q16': 4, # S = 75%
        'Q17': 2, 'Q18': 2, 'Q19': 2, 'Q20': 2, # E = 25%
        'Q21': 2, 'Q22': 2, 'Q23': 2, 'Q24': 2, # C = 25%
        'Q25': 2, 'Q26': 5, 'Q27': 5, 'Q28': 2, 'Q29': 4
    },
    # I=100%, C=75%, R=25% — strongly investigative + systematic, low hands-on
    # Computing programmes are I primary, C secondary — this profile avoids CDE (R primary)
    "Computing (I+C)": {
        'Q1': 2, 'Q2': 2, 'Q3': 2, 'Q4': 2,   # R = 25%
        'Q5': 5, 'Q6': 5, 'Q7': 5, 'Q8': 5,   # I = 100%
        'Q9': 1, 'Q10': 1, 'Q11': 1, 'Q12': 1, # A = 0%
        'Q13': 1, 'Q14': 1, 'Q15': 1, 'Q16': 1, # S = 0%
        'Q17': 2, 'Q18': 2, 'Q19': 2, 'Q20': 2, # E = 25%
        'Q21': 4, 'Q22': 4, 'Q23': 4, 'Q24': 4, # C = 75%
        'Q25': 4, 'Q26': 1, 'Q27': 2, 'Q28': 5, 'Q29': 3
    },
    # I=100%, R=25%, everything else very low
    # Science programmes are I primary — low R avoids CDE domination
    # Low values scores avoid Business Analytics appearing
    "Science (I only)": {
        'Q1': 2, 'Q2': 2, 'Q3': 2, 'Q4': 2,   # R = 25%
        'Q5': 5, 'Q6': 5, 'Q7': 5, 'Q8': 5,   # I = 100%
        'Q9': 1, 'Q10': 1, 'Q11': 1, 'Q12': 1, # A = 0%
        'Q13': 2, 'Q14': 2, 'Q15': 2, 'Q16': 2, # S = 25%
        'Q17': 1, 'Q18': 1, 'Q19': 1, 'Q20': 1, # E = 0%
        'Q21': 2, 'Q22': 2, 'Q23': 2, 'Q24': 2, # C = 25%
        'Q25': 2, 'Q26': 2, 'Q27': 1, 'Q28': 4, 'Q29': 5
    },
    # A=100%, E=75% — strongly artistic + enterprising
    # Music/YST programmes are A primary, E secondary
    "Music/YST (A+E)": {
        'Q1': 1, 'Q2': 1, 'Q3': 1, 'Q4': 1,   # R = 0%
        'Q5': 1, 'Q6': 1, 'Q7': 1, 'Q8': 1,   # I = 0%
        'Q9': 5, 'Q10': 5, 'Q11': 5, 'Q12': 5, # A = 100%
        'Q13': 2, 'Q14': 2, 'Q15': 2, 'Q16': 2, # S = 25%
        'Q17': 4, 'Q18': 4, 'Q19': 4, 'Q20': 4, # E = 75%
        'Q21': 1, 'Q22': 1, 'Q23': 1, 'Q24': 1, # C = 0%
        'Q25': 1, 'Q26': 3, 'Q27': 5, 'Q28': 1, 'Q29': 4
    }
}


# ============================================================
# CDE DRILL-DOWN DATA
# ============================================================

CDE_PROGRAMMES = [
    "Architecture", "Biomedical Engineering", "Chemical Engineering",
    "Civil Engineering", "Computer Engineering", "Electrical Engineering",
    "Engineering Science", "Environmental and Sustainability Engineering",
    "Industrial Design", "Industrial and Systems Engineering",
    "Infrastructure and Project Management", "Landscape Architecture",
    "Materials Science and Engineering", "Mechanical Engineering",
    "Robotics and Machine Intelligence"
]

CDE_IDENTITY_STATEMENTS = {
    "Architecture": "Based on your responses, you are someone who sees the world through space, form and human experience. You thrive when you can blend creative vision with technical precision, turning ideas into physical environments that people live and work in. Your love for design, visual thinking and spatial reasoning makes Architecture a natural fit. Graduates go on to become licensed architects, urban designers, or design consultants shaping Singapore's and the world's built environment.",
    "Biomedical Engineering": "Based on your responses, you are someone who sits at the intersection of science and humanity — you want technology to heal. You thrive in lab environments where biology meets engineering, solving problems that directly improve patient lives. Your interest in biology, chemistry and medical applications, combined with an engineering mindset, makes Biomedical Engineering your natural home. Graduates work in medical device companies, hospitals, research institutes or pursue medicine.",
    "Chemical Engineering": "Based on your responses, you are someone who thinks at the molecular level — fascinated by how materials and substances transform and interact. You thrive in lab and process environments, designing systems that turn raw materials into useful products at scale. Your strength in chemistry and mathematics, combined with a love for systematic problem-solving, makes Chemical Engineering a strong fit. Graduates work in pharmaceuticals, petrochemicals, food technology and sustainability sectors.",
    "Civil Engineering": "Based on your responses, you are someone who thinks big — you want to build things that last generations. You thrive when working on large-scale physical challenges, from bridges and tunnels to water systems and transport networks. Your preference for tangible, real-world problems and your interest in mathematics and physics makes Civil Engineering a natural fit. Graduates shape the infrastructure of cities and countries, working with government bodies, construction firms and consultancies.",
    "Computer Engineering": "Based on your responses, you are someone who lives at the boundary of hardware and software — you love understanding how machines think and communicate. You thrive when coding, designing circuits or building systems that bridge the physical and digital worlds. Your passion for computing, electronics and logical problem-solving makes Computer Engineering your natural home. Graduates work in tech companies, semiconductor firms, cybersecurity and embedded systems across the globe.",
    "Electrical Engineering": "Based on your responses, you are someone energised by the invisible forces that power the modern world. You thrive when designing and analysing electrical systems, from power grids to microchips to wireless communications. Your strength in physics and mathematics, combined with a fascination for electronics and energy, makes Electrical Engineering a strong fit. Graduates work in energy, telecommunications, semiconductor and smart systems industries.",
    "Engineering Science": "Based on your responses, you are someone who loves engineering at its most fundamental — you want to understand the deep principles behind how things work. You thrive in intellectually challenging environments that blend mathematics, physics and computational thinking. Your curiosity-driven, analytical mindset makes Engineering Science a natural fit. Graduates go into research, finance, data science, defence technology and advanced engineering roles.",
    "Environmental and Sustainability Engineering": "Based on your responses, you are someone driven by purpose — you want engineering to protect and restore the planet. You thrive when working on challenges at the intersection of technical solutions and environmental impact, from clean water systems to carbon reduction. Your interest in environmental science, chemistry and sustainability makes this programme a natural fit. Graduates work in environmental consultancies, government agencies and green energy firms.",
    "Industrial Design": "Based on your responses, you are someone who believes great design improves everyday life. You thrive in creative studio environments, sketching, prototyping and refining products that are both beautiful and functional. Your blend of artistic sensibility, human empathy and technical curiosity makes Industrial Design a natural fit. Graduates work as product designers, UX designers and innovation consultants across consumer electronics, healthcare and lifestyle industries.",
    "Industrial and Systems Engineering": "Based on your responses, you are someone who sees inefficiency as a problem worth solving. You thrive when optimising complex systems — whether it's a supply chain, a hospital workflow or a manufacturing process. Your analytical mindset, love for data and ability to see the big picture makes Industrial and Systems Engineering a natural fit. Graduates work in operations, logistics, consulting and data analytics across virtually every industry.",
    "Infrastructure and Project Management": "Based on your responses, you are someone who makes things happen at scale. You thrive when coordinating large teams, managing timelines and delivering complex projects from vision to reality. Your strength in planning, systems thinking and leadership makes Infrastructure and Project Management a natural fit. Graduates become project managers, quantity surveyors and construction consultants delivering major infrastructure across Singapore and beyond.",
    "Landscape Architecture": "Based on your responses, you are someone who sees nature and human spaces as inseparable. You thrive when designing outdoor environments — parks, waterfronts, green corridors — that balance ecological health with human wellbeing. Your love for spatial design, environmental sensitivity and creative thinking makes Landscape Architecture a natural fit. Graduates work with urban planning agencies and landscape consultancies shaping liveable cities.",
    "Materials Science and Engineering": "Based on your responses, you are someone fascinated by what things are made of and why they behave the way they do. You thrive in lab environments, experimenting with metals, polymers, ceramics and composites to unlock new material properties. Your interest in chemistry, physics and hands-on experimentation makes Materials Science and Engineering a natural fit. Graduates work in semiconductor, aerospace, biomedical and advanced manufacturing industries.",
    "Mechanical Engineering": "Based on your responses, you are someone who sees the world as a system of forces, motion and energy waiting to be harnessed. You thrive when designing, building and testing physical things — from engines and robots to medical devices and renewable energy systems. Your love for physics, mathematics and hands-on making makes Mechanical Engineering a natural fit. Graduates work across aerospace, automotive, robotics, energy and manufacturing industries.",
    "Robotics and Machine Intelligence": "Based on your responses, you are someone captivated by the idea of machines that can sense, think and act. You thrive at the cutting edge — combining mechanical engineering, electronics and artificial intelligence to build systems that were once science fiction. Your passion for coding, intelligent systems and pushing boundaries makes Robotics and Machine Intelligence a natural fit. Graduates lead in automation, AI research, autonomous vehicles and smart manufacturing."
}

CDE_DRILL_DOWN_QUESTIONS = [
    {
        "id": "CDE_Q1",
        "text": "Which subject genuinely excites you the most?",
        "options": {
            "A": ("Mathematics & Physics", {"Mechanical Engineering": 2, "Civil Engineering": 2, "Engineering Science": 2, "Electrical Engineering": 2, "Infrastructure and Project Management": 1}),
            "B": ("Biology & Chemistry", {"Biomedical Engineering": 2, "Chemical Engineering": 2, "Environmental and Sustainability Engineering": 2}),
            "C": ("Computing & Electronics", {"Computer Engineering": 2, "Electrical Engineering": 2, "Robotics and Machine Intelligence": 2}),
            "D": ("Art, Design & Spatial Thinking", {"Architecture": 2, "Landscape Architecture": 2, "Industrial Design": 2}),
            "E": ("Systems, Statistics & Management", {"Industrial and Systems Engineering": 2, "Infrastructure and Project Management": 2, "Engineering Science": 1})
        }
    },
    {
        "id": "CDE_Q2",
        "text": "In school projects, which role do you naturally take on?",
        "options": {
            "A": ("Calculating and solving equations", {"Mechanical Engineering": 2, "Civil Engineering": 2, "Engineering Science": 2}),
            "B": ("Coding and building software or hardware", {"Computer Engineering": 2, "Electrical Engineering": 2, "Robotics and Machine Intelligence": 2}),
            "C": ("Designing visuals, layouts or models", {"Architecture": 2, "Industrial Design": 2, "Landscape Architecture": 2}),
            "D": ("Running experiments in a lab", {"Biomedical Engineering": 2, "Chemical Engineering": 2, "Materials Science and Engineering": 2}),
            "E": ("Planning, organising and coordinating", {"Industrial and Systems Engineering": 2, "Infrastructure and Project Management": 2})
        }
    },
    {
        "id": "CDE_Q3",
        "text": "Where would you feel most at home learning?",
        "options": {
            "A": ("Workshop or fabrication lab — building physical things", {"Mechanical Engineering": 2, "Materials Science and Engineering": 2, "Civil Engineering": 1}),
            "B": ("Design studio — sketching, modelling, critiquing", {"Architecture": 2, "Industrial Design": 2, "Landscape Architecture": 2}),
            "C": ("Computer lab — coding, simulating, analysing data", {"Computer Engineering": 2, "Robotics and Machine Intelligence": 2, "Electrical Engineering": 2, "Industrial and Systems Engineering": 1}),
            "D": ("Science lab — running experiments, testing samples", {"Biomedical Engineering": 2, "Chemical Engineering": 2, "Environmental and Sustainability Engineering": 2}),
            "E": ("Field or construction site — real-world environments", {"Civil Engineering": 2, "Infrastructure and Project Management": 2, "Environmental and Sustainability Engineering": 1})
        }
    },
    {
        "id": "CDE_Q4",
        "text": "You have one full semester for a project. Which excites you most?",
        "options": {
            "A": ("Design and build a working mechanical prototype", {"Mechanical Engineering": 2, "Materials Science and Engineering": 2}),
            "B": ("Develop an AI system or smart device", {"Robotics and Machine Intelligence": 2, "Computer Engineering": 2, "Electrical Engineering": 1}),
            "C": ("Design a building or public space from scratch", {"Architecture": 2, "Landscape Architecture": 2, "Industrial Design": 1}),
            "D": ("Research a solution to an environmental or health problem", {"Biomedical Engineering": 2, "Chemical Engineering": 2, "Environmental and Sustainability Engineering": 2}),
            "E": ("Optimise a real company's operations or supply chain", {"Industrial and Systems Engineering": 2, "Infrastructure and Project Management": 2, "Engineering Science": 1})
        }
    },
    {
        "id": "CDE_Q5",
        "text": "Which problem would you most want to spend your career solving?",
        "options": {
            "A": ("Building infrastructure that lasts 100 years", {"Civil Engineering": 2, "Infrastructure and Project Management": 2}),
            "B": ("Creating machines and products people use daily", {"Mechanical Engineering": 2, "Materials Science and Engineering": 2, "Industrial Design": 2}),
            "C": ("Making computers, robots and devices smarter", {"Computer Engineering": 2, "Electrical Engineering": 2, "Robotics and Machine Intelligence": 2, "Engineering Science": 1}),
            "D": ("Improving human health through technology", {"Biomedical Engineering": 2, "Chemical Engineering": 2}),
            "E": ("Protecting and restoring the natural environment", {"Environmental and Sustainability Engineering": 2, "Landscape Architecture": 2})
        }
    },
    {
        "id": "CDE_Q6",
        "text": "Which best describes the kind of work you'd enjoy day-to-day?",
        "options": {
            "A": ("Physical and tangible — I can touch and test what I build", {"Mechanical Engineering": 2, "Civil Engineering": 2, "Materials Science and Engineering": 2}),
            "B": ("Digital and computational — I work through screens and code", {"Computer Engineering": 2, "Electrical Engineering": 2, "Robotics and Machine Intelligence": 2}),
            "C": ("Visual and spatial — I work with shapes, spaces and aesthetics", {"Architecture": 2, "Landscape Architecture": 2, "Industrial Design": 2}),
            "D": ("Biological and chemical — I work with living systems or materials", {"Biomedical Engineering": 2, "Chemical Engineering": 2, "Environmental and Sustainability Engineering": 1}),
            "E": ("Analytical and process-driven — I optimise how systems run", {"Industrial and Systems Engineering": 2, "Engineering Science": 2, "Infrastructure and Project Management": 2})
        }
    },
    {
        "id": "CDE_Q7",
        "text": "Which workday sounds most like you?",
        "options": {
            "A": ("In a workshop prototyping and testing a new product", {"Mechanical Engineering": 2, "Materials Science and Engineering": 2, "Industrial Design": 1}),
            "B": ("At a computer designing simulations or writing algorithms", {"Computer Engineering": 2, "Robotics and Machine Intelligence": 2, "Electrical Engineering": 2, "Engineering Science": 1}),
            "C": ("In a studio presenting design concepts to clients", {"Architecture": 2, "Landscape Architecture": 2, "Industrial Design": 2}),
            "D": ("In a lab analysing samples or running experiments", {"Biomedical Engineering": 2, "Chemical Engineering": 2, "Environmental and Sustainability Engineering": 2}),
            "E": ("On a construction site or managing a large project", {"Civil Engineering": 2, "Infrastructure and Project Management": 2})
        }
    },
    {
        "id": "CDE_Q8",
        "text": "Which best describes the scale of impact you want to create?",
        "options": {
            "A": ("Design a product millions of people use every day", {"Mechanical Engineering": 2, "Industrial Design": 2, "Materials Science and Engineering": 1}),
            "B": ("Build systems that make cities smarter and more connected", {"Computer Engineering": 2, "Electrical Engineering": 2, "Robotics and Machine Intelligence": 2}),
            "C": ("Shape the skyline — design buildings and spaces that inspire", {"Architecture": 2, "Landscape Architecture": 2}),
            "D": ("Save lives through medical devices or treatments", {"Biomedical Engineering": 2, "Chemical Engineering": 2}),
            "E": ("Solve large-scale environmental or infrastructure challenges", {"Environmental and Sustainability Engineering": 2, "Civil Engineering": 2, "Infrastructure and Project Management": 2})
        }
    },
    {
        "id": "CDE_Q9",
        "text": "Which career title appeals to you most in 10 years?",
        "options": {
            "A": ("Product or Mechanical Engineer at a manufacturing company", {"Mechanical Engineering": 2, "Materials Science and Engineering": 2}),
            "B": ("Software, Robotics or AI Engineer at a tech company", {"Computer Engineering": 2, "Robotics and Machine Intelligence": 2, "Electrical Engineering": 1}),
            "C": ("Architect or Designer shaping built environments", {"Architecture": 2, "Landscape Architecture": 2, "Industrial Design": 2}),
            "D": ("Biomedical or Process Engineer in healthcare or pharmaceuticals", {"Biomedical Engineering": 2, "Chemical Engineering": 2}),
            "E": ("Project Manager or Systems Consultant", {"Industrial and Systems Engineering": 2, "Infrastructure and Project Management": 2, "Engineering Science": 1})
        }
    },
    {
        "id": "CDE_Q10",
        "text": "Which statement feels most like you?",
        "options": {
            "A": ("I am a maker — I love building things that work in the real world", {"Mechanical Engineering": 2, "Civil Engineering": 2, "Materials Science and Engineering": 2}),
            "B": ("I am a coder/thinker — I love logic, systems and intelligent machines", {"Computer Engineering": 2, "Robotics and Machine Intelligence": 2, "Electrical Engineering": 2, "Engineering Science": 1}),
            "C": ("I am a creator — I love beauty, space and human-centred design", {"Architecture": 2, "Industrial Design": 2, "Landscape Architecture": 2}),
            "D": ("I am a healer or scientist — I want technology to improve lives", {"Biomedical Engineering": 2, "Chemical Engineering": 2, "Environmental and Sustainability Engineering": 1}),
            "E": ("I am an organiser — I love making complex systems run smoothly", {"Industrial and Systems Engineering": 2, "Infrastructure and Project Management": 2})
        }
    }
]


# ============================================================
# COMPUTING DRILL-DOWN DATA
# ============================================================

COMPUTING_PROGRAMMES = [
    "Computer Science", "Artificial Intelligence", "Information Security",
    "Computer Engineering", "Business Analytics", "Business Artificial Intelligence Systems"
]

COMPUTING_IDENTITY_STATEMENTS = {
    "Computer Science": "Based on your responses, you are someone energised by abstract thinking and elegant problem-solving. You gravitate toward logic, algorithms and building software systems from the ground up. Your love for computational theory and software development makes Computer Science a natural fit. Graduates work as software engineers, researchers and tech leads at top technology companies and research institutions worldwide.",
    "Artificial Intelligence": "Based on your responses, you are someone captivated by machines that can learn, reason and make decisions. You are drawn to the cutting edge where mathematics, data and computing collide to create intelligent systems. Your passion for algorithms, pattern recognition and the future of technology makes Artificial Intelligence a natural fit. Graduates work in AI research labs, tech giants, autonomous systems and healthcare technology.",
    "Information Security": "Based on your responses, you are someone who thinks like both a builder and a protector — you want to understand systems deeply enough to defend them. Your analytical mindset, attention to detail and interest in cybersecurity makes Information Security a natural fit. Graduates work in cybersecurity firms, government agencies, banking and critical infrastructure protection.",
    "Computer Engineering": "Based on your responses, you are someone who lives at the boundary of hardware and software — you love understanding how machines think at the deepest level. Your passion for both electronics and computing makes Computer Engineering a natural fit. Graduates work in semiconductor companies, tech hardware firms, robotics and IoT industries.",
    "Business Analytics": "Based on your responses, you are someone who sees data as a lens for better decisions. You are drawn to the intersection of technology and business — turning messy real-world data into clear insights that drive strategy. Your blend of analytical thinking and interest in statistics makes Business Analytics a natural fit. Graduates work as data analysts and business intelligence specialists across finance, retail, healthcare and tech.",
    "Business Artificial Intelligence Systems": "Based on your responses, you are someone who wants AI to solve real business problems. You are excited by how machine learning and intelligent systems can transform how companies operate and serve customers. Your combination of business acumen and interest in AI applications makes Business AI Systems a natural fit. Graduates work at the frontier of AI adoption in enterprises, consulting firms and fintech companies."
}

COMPUTING_DRILL_DOWN_QUESTIONS = [
    {
        "id": "COMP_Q1",
        "text": "Which excites you more?",
        "options": {
            "A": ("Building and writing software — I love coding and creating programs", {"Computer Science": 2, "Artificial Intelligence": 1, "Information Security": 1}),
            "B": ("Understanding how hardware and software work together at the chip level", {"Computer Engineering": 2}),
            "C": ("Using data and AI to solve business problems", {"Business Analytics": 2, "Business Artificial Intelligence Systems": 2}),
            "D": ("Protecting systems and outsmarting cyber attackers", {"Information Security": 2}),
            "E": ("Teaching machines to learn and make intelligent decisions", {"Artificial Intelligence": 2, "Business Artificial Intelligence Systems": 1})
        }
    },
    {
        "id": "COMP_Q2",
        "text": "Which subject combination appeals to you most?",
        "options": {
            "A": ("Mathematics + Computer Science — pure logic and algorithms", {"Computer Science": 2, "Artificial Intelligence": 1}),
            "B": ("Mathematics + Statistics + Economics", {"Business Analytics": 2, "Business Artificial Intelligence Systems": 1}),
            "C": ("Physics + Electronics + Computing", {"Computer Engineering": 2}),
            "D": ("Computing + Cryptography + Networks", {"Information Security": 2}),
            "E": ("Mathematics + Data Science + AI", {"Artificial Intelligence": 2, "Business Artificial Intelligence Systems": 1})
        }
    },
    {
        "id": "COMP_Q3",
        "text": "Which project would you be most excited to work on?",
        "options": {
            "A": ("Build a fast, efficient algorithm that solves a complex computational problem", {"Computer Science": 2}),
            "B": ("Design a microprocessor or embedded system from scratch", {"Computer Engineering": 2}),
            "C": ("Train a machine learning model to predict customer behaviour", {"Business Analytics": 2, "Business Artificial Intelligence Systems": 1, "Artificial Intelligence": 1}),
            "D": ("Find and fix vulnerabilities in a company's entire digital infrastructure", {"Information Security": 2}),
            "E": ("Build an AI system that automates a real business process", {"Artificial Intelligence": 1, "Business Artificial Intelligence Systems": 2})
        }
    },
    {
        "id": "COMP_Q4",
        "text": "How do you feel about the business side of technology?",
        "options": {
            "A": ("Not very interested — I prefer pure technical depth", {"Computer Science": 2, "Computer Engineering": 1, "Information Security": 1}),
            "B": ("Somewhat interested — I like tech but also want to understand real-world impact", {"Artificial Intelligence": 1, "Computer Science": 1}),
            "C": ("Very interested — I want to use technology to directly drive business outcomes", {"Business Analytics": 2, "Business Artificial Intelligence Systems": 2}),
            "D": ("I want to bridge both worlds equally", {"Business Artificial Intelligence Systems": 2, "Business Analytics": 1})
        }
    },
    {
        "id": "COMP_Q5",
        "text": "Which career environment sounds most exciting?",
        "options": {
            "A": ("A top tech company (Google, Meta) as a software engineer", {"Computer Science": 2, "Artificial Intelligence": 1}),
            "B": ("A semiconductor or hardware company designing next-gen chips", {"Computer Engineering": 2}),
            "C": ("A cybersecurity firm or government agency protecting national infrastructure", {"Information Security": 2}),
            "D": ("A bank, consultancy or retail giant using data to drive decisions", {"Business Analytics": 2, "Business Artificial Intelligence Systems": 1}),
            "E": ("An AI startup or research lab building intelligent systems", {"Artificial Intelligence": 2, "Business Artificial Intelligence Systems": 1})
        }
    },
    {
        "id": "COMP_Q6",
        "text": "Which statement feels most true about you?",
        "options": {
            "A": ("I am drawn to the theoretical elegance of algorithms and computation", {"Computer Science": 2}),
            "B": ("I want to understand computers all the way down to the hardware", {"Computer Engineering": 2}),
            "C": ("I am fascinated by how AI systems learn from data", {"Artificial Intelligence": 2, "Business Artificial Intelligence Systems": 1}),
            "D": ("I want to be the person who keeps digital systems safe from attack", {"Information Security": 2}),
            "E": ("I want to turn data into decisions that make businesses smarter", {"Business Analytics": 2, "Business Artificial Intelligence Systems": 1})
        }
    },
    {
        "id": "COMP_Q7",
        "text": "How do you feel about working with data and statistics?",
        "options": {
            "A": ("I love it — data analysis and statistics are genuinely exciting to me", {"Business Analytics": 2, "Artificial Intelligence": 1, "Business Artificial Intelligence Systems": 1}),
            "B": ("I like it as a tool but I prefer building software systems", {"Computer Science": 2, "Artificial Intelligence": 1}),
            "C": ("I prefer working at the hardware and systems level over data", {"Computer Engineering": 2, "Information Security": 1}),
            "D": ("I like data but mainly when it helps solve security or systems problems", {"Information Security": 2})
        }
    },
    {
        "id": "COMP_Q8",
        "text": "Which real-world problem excites you most?",
        "options": {
            "A": ("Making software faster, smarter and more reliable", {"Computer Science": 2}),
            "B": ("Building the next generation of chips and computing devices", {"Computer Engineering": 2}),
            "C": ("Stopping hackers from stealing data or disrupting critical systems", {"Information Security": 2}),
            "D": ("Helping companies understand their customers better through data", {"Business Analytics": 2, "Business Artificial Intelligence Systems": 1}),
            "E": ("Building AI that helps doctors, teachers or businesses make better decisions", {"Artificial Intelligence": 2, "Business Artificial Intelligence Systems": 2})
        }
    },
    {
        "id": "COMP_Q9",
        "text": "How important is it that your work has direct business or commercial impact?",
        "options": {
            "A": ("Not important — I care about technical excellence above all", {"Computer Science": 2, "Computer Engineering": 1}),
            "B": ("Somewhat important — I'm drawn to deep technical problems but want them to matter", {"Artificial Intelligence": 2, "Information Security": 1}),
            "C": ("Very important — I want to see clear, measurable business results", {"Business Analytics": 2, "Business Artificial Intelligence Systems": 2}),
            "D": ("Extremely important — I want to be at the intersection of tech and business strategy", {"Business Artificial Intelligence Systems": 2, "Business Analytics": 1})
        }
    },
    {
        "id": "COMP_Q10",
        "text": "Which identity feels most like you?",
        "options": {
            "A": ("I am a builder — I write clean code and engineer elegant software systems", {"Computer Science": 2}),
            "B": ("I am a hardware person — I want to understand machines at the deepest level", {"Computer Engineering": 2}),
            "C": ("I am an AI person — I am fascinated by intelligent systems and machine learning", {"Artificial Intelligence": 2, "Business Artificial Intelligence Systems": 1}),
            "D": ("I am a guardian — I want to protect digital systems and fight cyber threats", {"Information Security": 2}),
            "E": ("I am a data strategist — I turn numbers into decisions that drive real outcomes", {"Business Analytics": 2, "Business Artificial Intelligence Systems": 1})
        }
    }
]


# ============================================================
# BUSINESS DRILL-DOWN DATA
# ============================================================

BUSINESS_PROGRAMMES = [
    "Applied Business Analytics", "Business Economics", "Finance",
    "Innovation and Entrepreneurship", "Leadership and Human Capital Management",
    "Marketing", "Operations and Supply Chain Management", "Accountancy", "Real Estate"
]

BUSINESS_IDENTITY_STATEMENTS = {
    "Applied Business Analytics": "Based on your responses, you are someone who believes data is the most powerful tool in modern business. You thrive when turning complex datasets into actionable strategies, combining your quantitative skills with business intuition. Your love for numbers, technology and business decision-making makes Applied Business Analytics a natural fit. Graduates work as data analysts, business intelligence specialists and strategy consultants across every industry.",
    "Business Economics": "Based on your responses, you are someone who wants to understand why markets, companies and economies behave the way they do. You thrive in analytical environments where theory meets policy and real-world decision-making. Your interest in economics, critical thinking and problem-solving makes Business Economics a natural fit. Graduates work in government agencies, economic consultancies, banking, policy research and international organisations.",
    "Finance": "Based on your responses, you are someone energised by the flow of capital and the mechanics of financial markets. You thrive when analysing investments, managing risk and navigating complex financial instruments. Your interest in numbers, markets and wealth creation makes Finance a natural fit. Graduates work in investment banking, asset management, corporate finance, private equity and financial services across Singapore and globally.",
    "Innovation and Entrepreneurship": "Based on your responses, you are someone who sees problems as opportunities waiting to be turned into businesses. You thrive in fast-moving, uncertain environments where creativity, resilience and hustle matter more than convention. Your entrepreneurial mindset and appetite for building something new makes Innovation and Entrepreneurship a natural fit. Graduates launch startups, lead innovation teams and drive transformation in organisations.",
    "Leadership and Human Capital Management": "Based on your responses, you are someone who believes people are an organisation's greatest asset. You thrive when developing talent, resolving workplace challenges and building cultures where teams flourish. Your empathy, interpersonal skills and interest in organisational behaviour makes Leadership and Human Capital Management a natural fit. Graduates work in HR, talent management, organisational development and leadership roles.",
    "Marketing": "Based on your responses, you are someone who understands that great products need great stories. You thrive when understanding consumer psychology, crafting campaigns and building brands that people love. Your creativity, curiosity about human behaviour and communication skills makes Marketing a natural fit. Graduates work in brand management, digital marketing, advertising agencies, market research and consumer insights.",
    "Operations and Supply Chain Management": "Based on your responses, you are someone who sees the hidden complexity behind every product on a shelf. You thrive when optimising processes, reducing waste and making global supply chains run smoothly and efficiently. Your systematic thinking and interest in logistics and operations makes this programme a natural fit. Graduates work in operations management, logistics, consulting and supply chain strategy roles.",
    "Accountancy": "Based on your responses, you are someone who finds clarity and power in numbers. You thrive in structured, detail-oriented environments where accuracy, integrity and analytical rigour matter. Your methodical mindset and interest in financial reporting makes Accountancy a natural fit. Graduates become certified public accountants, auditors, financial analysts and tax advisors at Big Four firms, banks and corporations.",
    "Real Estate": "Based on your responses, you are someone fascinated by how land, buildings and urban spaces create — and hold — value. You thrive at the intersection of finance, law and the built environment, analysing markets and making investment decisions. Your interest in property, investment and urban development makes Real Estate a natural fit. Graduates work in property development, real estate investment, urban planning and asset management."
}

BUSINESS_DRILL_DOWN_QUESTIONS = [
    {
        "id": "BIZ_Q1",
        "text": "What excites you most about the world of business?",
        "options": {
            "A": ("How financial markets work and how money flows through the economy", {"Finance": 2, "Business Economics": 2}),
            "B": ("How data and analytics can drive smarter business decisions", {"Applied Business Analytics": 2}),
            "C": ("Building a brand that people genuinely love and connect with", {"Marketing": 2}),
            "D": ("Starting something from scratch and making it succeed", {"Innovation and Entrepreneurship": 2}),
            "E": ("How people and organisations work — and how to make them better", {"Leadership and Human Capital Management": 2})
        }
    },
    {
        "id": "BIZ_Q2",
        "text": "Which subject combination appeals to you most?",
        "options": {
            "A": ("Statistics, programming and data visualisation", {"Applied Business Analytics": 2}),
            "B": ("Economics, mathematics and policy analysis", {"Business Economics": 2, "Finance": 1}),
            "C": ("Accounting, taxation and financial reporting", {"Accountancy": 2}),
            "D": ("Psychology, sociology and organisational behaviour", {"Leadership and Human Capital Management": 2, "Marketing": 1}),
            "E": ("Strategy, design thinking and entrepreneurship", {"Innovation and Entrepreneurship": 2})
        }
    },
    {
        "id": "BIZ_Q3",
        "text": "Which project would excite you most?",
        "options": {
            "A": ("Analyse a company's financial statements and recommend an investment decision", {"Finance": 2, "Accountancy": 1}),
            "B": ("Design and launch a marketing campaign for a new product", {"Marketing": 2}),
            "C": ("Build a predictive model to forecast sales across different markets", {"Applied Business Analytics": 2}),
            "D": ("Redesign a company's hiring and talent development process", {"Leadership and Human Capital Management": 2}),
            "E": ("Map out a supply chain and find where costs can be reduced", {"Operations and Supply Chain Management": 2})
        }
    },
    {
        "id": "BIZ_Q4",
        "text": "Which career environment sounds most like you?",
        "options": {
            "A": ("Investment bank or hedge fund — fast-paced, high-stakes financial decisions", {"Finance": 2}),
            "B": ("Startup or innovation hub — building new things, moving fast, taking risks", {"Innovation and Entrepreneurship": 2}),
            "C": ("Big Four accounting firm — rigorous, detail-oriented, trusted financial work", {"Accountancy": 2}),
            "D": ("Consulting firm — solving complex business problems across many industries", {"Applied Business Analytics": 1, "Business Economics": 1, "Operations and Supply Chain Management": 1}),
            "E": ("Property developer or real estate firm — physical assets, investment and urban development", {"Real Estate": 2})
        }
    },
    {
        "id": "BIZ_Q5",
        "text": "Which problem would you most enjoy solving?",
        "options": {
            "A": ("Why is this product not selling, and how do we fix that?", {"Marketing": 2}),
            "B": ("How do we get goods from factory to customer faster and cheaper?", {"Operations and Supply Chain Management": 2}),
            "C": ("How do we value this company accurately before acquiring it?", {"Finance": 2, "Accountancy": 1}),
            "D": ("How do we use data to predict which customers will churn next month?", {"Applied Business Analytics": 2}),
            "E": ("Which property investment will generate the best returns over 10 years?", {"Real Estate": 2})
        }
    },
    {
        "id": "BIZ_Q6",
        "text": "How do you feel about working with numbers and quantitative analysis?",
        "options": {
            "A": ("I love it — the more complex the numbers, the better", {"Finance": 2, "Applied Business Analytics": 2, "Accountancy": 1}),
            "B": ("I enjoy it, especially when it connects to economic theory and policy", {"Business Economics": 2}),
            "C": ("I like numbers but prefer combining them with strategy and people insights", {"Operations and Supply Chain Management": 1, "Leadership and Human Capital Management": 1, "Marketing": 1}),
            "D": ("I prefer qualitative work — creativity, strategy and human behaviour matter more to me", {"Marketing": 2, "Innovation and Entrepreneurship": 2, "Leadership and Human Capital Management": 1})
        }
    },
    {
        "id": "BIZ_Q7",
        "text": "Which daily work activity appeals to you most?",
        "options": {
            "A": ("Analysing financial reports and market data at my desk", {"Finance": 2, "Accountancy": 2}),
            "B": ("Running workshops, interviews and brainstorming sessions with teams", {"Leadership and Human Capital Management": 2, "Innovation and Entrepreneurship": 1}),
            "C": ("Building dashboards and data models to track business performance", {"Applied Business Analytics": 2}),
            "D": ("Meeting clients, pitching ideas and developing brand campaigns", {"Marketing": 2}),
            "E": ("Visiting warehouses, logistics centres or construction sites", {"Operations and Supply Chain Management": 2, "Real Estate": 1})
        }
    },
    {
        "id": "BIZ_Q8",
        "text": "What kind of impact do you want your career to have?",
        "options": {
            "A": ("Help businesses grow by connecting with customers more effectively", {"Marketing": 2}),
            "B": ("Make financial markets more efficient and create wealth responsibly", {"Finance": 2, "Business Economics": 1}),
            "C": ("Build companies and innovations that didn't exist before", {"Innovation and Entrepreneurship": 2}),
            "D": ("Help organisations attract, develop and retain great talent", {"Leadership and Human Capital Management": 2}),
            "E": ("Shape the physical landscape of cities through property and development", {"Real Estate": 2})
        }
    },
    {
        "id": "BIZ_Q9",
        "text": "Which professional title appeals most to you in 10 years?",
        "options": {
            "A": ("Investment Banker or Portfolio Manager", {"Finance": 2}),
            "B": ("Founder or Chief Innovation Officer", {"Innovation and Entrepreneurship": 2}),
            "C": ("Data Scientist or Business Analytics Manager", {"Applied Business Analytics": 2}),
            "D": ("HR Director or Chief People Officer", {"Leadership and Human Capital Management": 2}),
            "E": ("Property Developer or Real Estate Fund Manager", {"Real Estate": 2})
        }
    },
    {
        "id": "BIZ_Q10",
        "text": "Which identity feels most like you?",
        "options": {
            "A": ("I am a numbers person — I find clarity and power in financial data", {"Finance": 2, "Accountancy": 2}),
            "B": ("I am a builder — I want to create companies and disrupt industries", {"Innovation and Entrepreneurship": 2}),
            "C": ("I am an analyst — I make sense of data so organisations can act smarter", {"Applied Business Analytics": 2, "Business Economics": 1}),
            "D": ("I am a people person — I unlock potential in teams and organisations", {"Leadership and Human Capital Management": 2, "Marketing": 1}),
            "E": ("I am a strategist — I see how systems, logistics and supply chains connect", {"Operations and Supply Chain Management": 2, "Real Estate": 1})
        }
    }
]


# ============================================================
# HUMANITIES & SOCIAL SCIENCES DRILL-DOWN DATA
# ============================================================

HUMANITIES_PROGRAMMES = [
    "Chinese Language", "Chinese Studies", "English Language and Linguistics",
    "English Literature", "Global Studies", "History", "Japanese Studies",
    "Malay Studies", "Philosophy", "South Asian Studies", "Southeast Asian Studies",
    "Theatre and Performance Studies", "Anthropology", "Communications and News Media",
    "Economics", "Geography", "Political Science", "Psychology", "Social Work", "Sociology"
]

HUMANITIES_IDENTITY_STATEMENTS = {
    "Chinese Language": "Based on your responses, you are someone captivated by the structure, history and evolution of the Chinese language itself. You thrive in analytical and cultural environments where linguistics meets heritage. Your passion for language systems and Chinese culture makes Chinese Language a natural fit. Graduates work in education, translation, publishing, media and cultural diplomacy.",
    "Chinese Studies": "Based on your responses, you are someone fascinated by Chinese civilisation, literature, culture and society across the ages. You thrive when exploring how history, philosophy and culture shape modern Chinese-speaking communities. Graduates work in education, diplomacy, cultural institutions, journalism and business roles involving China.",
    "English Language and Linguistics": "Based on your responses, you are someone who loves language not just as a communication tool but as a system to be studied and understood. You thrive in analytical environments examining grammar, phonetics, discourse and how language shapes thought. Graduates work in education, language technology, editorial, speech therapy and communications.",
    "English Literature": "Based on your responses, you are someone moved by stories, ideas and the power of written language to illuminate the human condition. You thrive in creative, interpretive environments where close reading and critical thinking come alive. Graduates work in publishing, writing, education, media, arts administration and cultural industries.",
    "Global Studies": "Based on your responses, you are someone drawn to the big picture — how nations, cultures and economies interact and shape each other. You thrive in interdisciplinary environments connecting history, politics, economics and culture on a global scale. Graduates work in international organisations, NGOs, diplomacy, research and policy.",
    "History": "Based on your responses, you are someone who believes understanding the past is the key to understanding the present. You thrive in research-intensive environments, piecing together evidence to construct compelling narratives about how the world came to be. Graduates work in education, archiving, museums, journalism, law and public policy.",
    "Japanese Studies": "Based on your responses, you are someone fascinated by Japanese language, culture, society and its unique place in the world. You thrive in cultural and linguistic environments bridging East and West. Graduates work in Japan-facing business roles, diplomacy, education, translation, tourism and cultural exchange.",
    "Malay Studies": "Based on your responses, you are someone passionate about Malay language, literature, culture and the rich diversity of the Malay world. You thrive in environments connecting language, history and community. Graduates work in education, media, government, cultural institutions and community development.",
    "Philosophy": "Based on your responses, you are someone who cannot stop asking why. You thrive in rigorous intellectual environments where logic, ethics, metaphysics and the foundations of knowledge are examined from every angle. Graduates work in law, policy, academia, consulting, technology ethics and any field requiring deep critical thinking.",
    "South Asian Studies": "Based on your responses, you are someone captivated by the history, cultures, languages and politics of South Asia. You thrive in interdisciplinary environments connecting civilisational studies with contemporary issues. Graduates work in diplomacy, development organisations, journalism, research and business roles involving South Asia.",
    "Southeast Asian Studies": "Based on your responses, you are someone with a deep curiosity about the region you live in — its diversity, histories and futures. You thrive exploring the politics, cultures and societies of Southeast Asia across disciplinary boundaries. Graduates work in regional policy, NGOs, journalism, tourism, research and diplomacy.",
    "Theatre and Performance Studies": "Based on your responses, you are someone who understands that performance is how humans make meaning. You thrive in creative, collaborative environments where your body, voice and imagination are the tools of inquiry. Graduates work in theatre, film, arts education, cultural management, community engagement and creative industries.",
    "Anthropology": "Based on your responses, you are someone endlessly curious about what it means to be human across different cultures and contexts. You thrive doing fieldwork, observing and listening deeply to communities very different from your own. Graduates work in research, international development, NGOs, corporate cultural consulting, healthcare and policy.",
    "Communications and News Media": "Based on your responses, you are someone who believes information shapes society and that how we communicate matters enormously. You thrive in fast-paced, creative environments producing, analysing and distributing stories across media platforms. Graduates work in journalism, public relations, digital media, broadcasting and strategic communications.",
    "Economics": "Based on your responses, you are someone who wants to understand how societies allocate resources, make decisions and respond to incentives. You thrive in analytical environments combining theory, mathematics and real-world data to explain human and market behaviour. Graduates work in banking, government, consulting, research and policy organisations.",
    "Geography": "Based on your responses, you are someone fascinated by the relationship between people and place — how physical and human systems interact across space. You thrive in fieldwork and research environments combining spatial analysis with social and environmental questions. Graduates work in urban planning, environmental management, GIS, policy and consulting.",
    "Political Science": "Based on your responses, you are someone drawn to the study of power — how governments work, how policies are made and how international relations shape the world. You thrive in analytical, debate-rich environments engaging with big questions about justice, governance and change. Graduates work in government, diplomacy, law, journalism, NGOs and policy research.",
    "Psychology": "Based on your responses, you are someone fascinated by the human mind — why people think, feel and behave the way they do. You thrive in research and interpersonal environments combining scientific rigour with genuine empathy. Graduates work in clinical psychology, counselling, human resources, UX research, marketing and public health.",
    "Social Work": "Based on your responses, you are someone who feels called to stand alongside the most vulnerable members of society. You thrive in deeply human environments where empathy, advocacy and practical support change lives. Your commitment to social justice and community wellbeing makes Social Work a natural fit. Graduates work in social service agencies, hospitals, schools, prisons and government welfare bodies.",
    "Sociology": "Based on your responses, you are someone who looks beyond individual behaviour to ask how society itself shapes who we are. You thrive in analytical, research-driven environments examining inequality, institutions, culture and social change. Graduates work in research, policy, NGOs, media, education, human resources and social enterprise."
}

HUMANITIES_DRILL_DOWN_QUESTIONS = [
    {
        "id": "HUM_Q1",
        "text": "Which area draws you in the most?",
        "options": {
            "A": ("Language — how it works, evolves and shapes thought", {"Chinese Language": 2, "English Language and Linguistics": 2, "Malay Studies": 1, "Japanese Studies": 1}),
            "B": ("Society and human behaviour — why people and communities act as they do", {"Sociology": 2, "Anthropology": 2, "Psychology": 1, "Social Work": 1}),
            "C": ("Power, politics and global affairs", {"Political Science": 2, "Global Studies": 2, "History": 1, "Economics": 1}),
            "D": ("Culture, creativity and artistic expression", {"Theatre and Performance Studies": 2, "English Literature": 2, "Chinese Studies": 1}),
            "E": ("Media, communication and how stories shape the world", {"Communications and News Media": 2, "Sociology": 1})
        }
    },
    {
        "id": "HUM_Q2",
        "text": "Which research activity appeals most to you?",
        "options": {
            "A": ("Fieldwork — going out to communities, interviewing people, observing cultures", {"Anthropology": 2, "Social Work": 2, "Geography": 1, "Southeast Asian Studies": 1}),
            "B": ("Archival research — digging through documents, records and historical sources", {"History": 2, "Chinese Studies": 1, "Philosophy": 1}),
            "C": ("Quantitative analysis — using data and statistics to study social patterns", {"Economics": 2, "Psychology": 1, "Sociology": 1}),
            "D": ("Close reading — analysing texts, performances or cultural artefacts in depth", {"English Literature": 2, "Theatre and Performance Studies": 2, "Philosophy": 1}),
            "E": ("Policy analysis — studying how decisions are made and what their effects are", {"Political Science": 2, "Global Studies": 1, "Economics": 1})
        }
    },
    {
        "id": "HUM_Q3",
        "text": "Which geographic or cultural focus excites you most?",
        "options": {
            "A": ("East Asia — China, Japan, Korea and their civilisations", {"Chinese Studies": 2, "Japanese Studies": 2, "Chinese Language": 1}),
            "B": ("Southeast Asia and the Malay world", {"Southeast Asian Studies": 2, "Malay Studies": 2}),
            "C": ("South Asia — India, Sri Lanka, Bangladesh and beyond", {"South Asian Studies": 2}),
            "D": ("The whole world — global systems and international affairs", {"Global Studies": 2, "Political Science": 1, "Economics": 1}),
            "E": ("Singapore and local society — the communities around me", {"Sociology": 2, "Social Work": 2, "Anthropology": 1})
        }
    },
    {
        "id": "HUM_Q4",
        "text": "Which career path excites you most?",
        "options": {
            "A": ("Journalist, documentary filmmaker or media producer", {"Communications and News Media": 2}),
            "B": ("Counsellor, therapist or social worker helping vulnerable people", {"Psychology": 2, "Social Work": 2}),
            "C": ("Diplomat, policy analyst or international organisation professional", {"Political Science": 2, "Global Studies": 2, "Economics": 1}),
            "D": ("Researcher, academic or curator at a university or museum", {"History": 2, "Anthropology": 2, "Philosophy": 1}),
            "E": ("Performer, director or arts education professional", {"Theatre and Performance Studies": 2})
        }
    },
    {
        "id": "HUM_Q5",
        "text": "Which question most keeps you up at night?",
        "options": {
            "A": ("Why do some societies prosper while others struggle?", {"Economics": 2, "Political Science": 1, "Sociology": 1}),
            "B": ("What is the right thing to do — and how do we know?", {"Philosophy": 2, "Social Work": 1}),
            "C": ("How does the environment shape communities and vice versa?", {"Geography": 2, "Anthropology": 1, "Southeast Asian Studies": 1}),
            "D": ("Why do people behave the way they do — what drives human choices?", {"Psychology": 2, "Sociology": 1, "Anthropology": 1}),
            "E": ("How does where and how we grew up shape who we become?", {"Sociology": 2, "Anthropology": 1, "Social Work": 1})
        }
    },
    {
        "id": "HUM_Q6",
        "text": "Which type of work environment appeals to you?",
        "options": {
            "A": ("A newsroom or media organisation — fast-paced, public-facing storytelling", {"Communications and News Media": 2}),
            "B": ("A social service agency or community organisation — direct impact on people's lives", {"Social Work": 2, "Psychology": 1}),
            "C": ("A think tank, government ministry or international organisation", {"Political Science": 2, "Economics": 2, "Global Studies": 1}),
            "D": ("A university, research institute or cultural heritage body", {"History": 2, "Philosophy": 2, "Anthropology": 1}),
            "E": ("A creative company, theatre or cultural institution", {"Theatre and Performance Studies": 2, "English Literature": 1})
        }
    },
    {
        "id": "HUM_Q7",
        "text": "Which skill do you most want to develop at university?",
        "options": {
            "A": ("Writing — crafting clear, compelling and persuasive prose", {"English Literature": 2, "Communications and News Media": 2, "History": 1}),
            "B": ("Critical thinking — dismantling arguments and constructing logical ones", {"Philosophy": 2, "Political Science": 1, "Economics": 1}),
            "C": ("Empathy and counselling — understanding and supporting people", {"Psychology": 2, "Social Work": 2}),
            "D": ("Cross-cultural competency — navigating different cultural contexts", {"Anthropology": 2, "Southeast Asian Studies": 1, "South Asian Studies": 1, "Global Studies": 1}),
            "E": ("Research and data analysis — finding patterns in complex information", {"Economics": 2, "Sociology": 1, "Geography": 1})
        }
    },
    {
        "id": "HUM_Q8",
        "text": "Which issue do you care most about?",
        "options": {
            "A": ("Mental health and emotional wellbeing in society", {"Psychology": 2, "Social Work": 2}),
            "B": ("Income inequality, poverty and social justice", {"Social Work": 2, "Economics": 1, "Sociology": 1}),
            "C": ("Media literacy, misinformation and freedom of the press", {"Communications and News Media": 2, "Political Science": 1}),
            "D": ("Preserving cultural heritage and minority languages", {"Malay Studies": 2, "Chinese Studies": 2, "South Asian Studies": 1, "Southeast Asian Studies": 1}),
            "E": ("Climate change and its impact on human communities", {"Geography": 2, "Sociology": 1, "Anthropology": 1})
        }
    },
    {
        "id": "HUM_Q9",
        "text": "Which statement describes how you engage with the world?",
        "options": {
            "A": ("I observe and ask questions — I want to understand before I judge", {"Anthropology": 2, "Sociology": 1, "Geography": 1}),
            "B": ("I debate and argue — I enjoy testing ideas against strong opposition", {"Philosophy": 2, "Political Science": 2}),
            "C": ("I create and perform — I express ideas through storytelling and art", {"Theatre and Performance Studies": 2, "English Literature": 1}),
            "D": ("I report and communicate — I want to inform and hold power to account", {"Communications and News Media": 2}),
            "E": ("I support and advocate — I want to stand up for people who need help", {"Social Work": 2, "Psychology": 1})
        }
    },
    {
        "id": "HUM_Q10",
        "text": "Which identity feels most like you?",
        "options": {
            "A": ("I am a thinker — I love exploring ideas, arguments and big philosophical questions", {"Philosophy": 2, "Political Science": 1}),
            "B": ("I am a storyteller — I believe narrative is how humans make meaning", {"English Literature": 2, "Communications and News Media": 2, "Theatre and Performance Studies": 1}),
            "C": ("I am a healer — I want to support and uplift people in need", {"Psychology": 2, "Social Work": 2}),
            "D": ("I am a bridge-builder — I connect cultures, languages and communities", {"Global Studies": 2, "Southeast Asian Studies": 1, "South Asian Studies": 1, "Anthropology": 1}),
            "E": ("I am an analyst — I want to understand how societies and economies work", {"Economics": 2, "Sociology": 2, "Geography": 1})
        }
    }
]


# ============================================================
# SCIENCES DRILL-DOWN DATA
# ============================================================

SCIENCES_PROGRAMMES = [
    "Chemistry", "Data Science and Analytics", "Food Science and Technology",
    "Life Sciences", "Mathematics", "Pharmaceutical Science",
    "Physics", "Quantitative Finance", "Statistics"
]

SCIENCES_IDENTITY_STATEMENTS = {
    "Chemistry": "Based on your responses, you are someone who finds beauty in the periodic table and excitement in molecular reactions. You thrive in lab environments where you can probe the fundamental building blocks of matter. Your passion for chemical principles and experimental work makes Chemistry a natural fit. Graduates work in research, pharmaceuticals, materials science, environmental chemistry and chemical industries.",
    "Data Science and Analytics": "Based on your responses, you are someone who sees data everywhere and instinctively asks what it means. You thrive combining statistical rigour with computational tools to extract insight from complex datasets. Your curiosity for patterns, programming and problem-solving makes Data Science and Analytics a natural fit. Graduates work across tech, finance, healthcare, government and any data-driven organisation.",
    "Food Science and Technology": "Based on your responses, you are someone fascinated by the science behind what we eat — from molecular gastronomy to food safety and sustainable nutrition. You thrive in applied lab environments where chemistry meets biology meets everyday life. Graduates work in food manufacturing, regulatory agencies, research institutes and nutrition consulting.",
    "Life Sciences": "Based on your responses, you are someone captivated by living systems — from cells and genes to organisms and ecosystems. You thrive in laboratory and field environments, investigating the mechanisms of life at every scale. Your curiosity for biology and its applications makes Life Sciences a natural fit. Graduates work in biomedical research, pharmaceuticals, environmental science, education and biotechnology.",
    "Mathematics": "Based on your responses, you are someone who experiences the unique pleasure of a proof clicking into place. You thrive in abstract, rigorous intellectual environments where pure logic and mathematical beauty are the highest currency. Your love for abstraction, patterns and formal reasoning makes Mathematics a natural fit. Graduates work in research, finance, data science, cryptography, academia and technology.",
    "Pharmaceutical Science": "Based on your responses, you are someone who wants to understand how drugs are discovered, developed and delivered to patients. You thrive at the intersection of chemistry, biology and healthcare, working in labs and translational research settings. Graduates work in pharmaceutical companies, clinical research organisations, regulatory agencies and healthcare institutions.",
    "Physics": "Based on your responses, you are someone driven to understand the fundamental laws that govern the universe. You thrive in intellectually demanding environments combining mathematical rigour with experimental curiosity. Your passion for understanding reality at its deepest level makes Physics a natural fit. Graduates work in research, engineering, finance, data science, defence technology and academia.",
    "Quantitative Finance": "Based on your responses, you are someone who applies mathematical and statistical tools to understand and navigate financial markets. You thrive in analytically intense environments where models, algorithms and data drive investment decisions. Graduates work in quantitative trading, risk management, investment banking, hedge funds and financial technology.",
    "Statistics": "Based on your responses, you are someone who believes that uncertainty can be measured, modelled and managed. You thrive in analytical environments applying statistical methods to real-world problems across science, business and society. Graduates work in biostatistics, government analytics, market research, data science and actuarial science."
}

SCIENCES_DRILL_DOWN_QUESTIONS = [
    {
        "id": "SCI_Q1",
        "text": "Which science excites you the most?",
        "options": {
            "A": ("Mathematics — pure logic, proofs and abstract structures", {"Mathematics": 2, "Statistics": 1, "Quantitative Finance": 1}),
            "B": ("Physics — understanding the fundamental laws of the universe", {"Physics": 2}),
            "C": ("Chemistry — how substances interact and transform", {"Chemistry": 2, "Pharmaceutical Science": 1, "Food Science and Technology": 1}),
            "D": ("Biology — how living things work at every scale", {"Life Sciences": 2, "Pharmaceutical Science": 1, "Food Science and Technology": 1}),
            "E": ("Statistics and data — finding patterns and making predictions", {"Statistics": 2, "Data Science and Analytics": 2, "Quantitative Finance": 1})
        }
    },
    {
        "id": "SCI_Q2",
        "text": "What kind of research environment appeals most to you?",
        "options": {
            "A": ("A dry lab — working with computers, code and data", {"Data Science and Analytics": 2, "Statistics": 2, "Mathematics": 1}),
            "B": ("A wet lab — running experiments with chemicals, samples and equipment", {"Chemistry": 2, "Pharmaceutical Science": 2, "Life Sciences": 1, "Food Science and Technology": 1}),
            "C": ("A physics lab — lasers, particle detectors and precision instruments", {"Physics": 2}),
            "D": ("A financial modelling environment — data, markets and quantitative models", {"Quantitative Finance": 2, "Statistics": 1}),
            "E": ("A field or applied research setting connecting science to everyday life", {"Food Science and Technology": 2, "Life Sciences": 1})
        }
    },
    {
        "id": "SCI_Q3",
        "text": "Which problem would you most like to work on?",
        "options": {
            "A": ("Developing a new drug to treat a disease with no current cure", {"Pharmaceutical Science": 2, "Chemistry": 1, "Life Sciences": 1}),
            "B": ("Building a machine learning model to predict epidemic outbreaks", {"Data Science and Analytics": 2, "Statistics": 1}),
            "C": ("Proving a mathematical theorem that has stumped researchers for decades", {"Mathematics": 2}),
            "D": ("Understanding how a quantum phenomenon could revolutionise computing", {"Physics": 2}),
            "E": ("Designing safer and more nutritious food products at scale", {"Food Science and Technology": 2})
        }
    },
    {
        "id": "SCI_Q4",
        "text": "How important is it that your work has direct practical applications?",
        "options": {
            "A": ("Not important — I love pure science and theory for its own sake", {"Mathematics": 2, "Physics": 2}),
            "B": ("Somewhat important — I want theory grounded in real phenomena", {"Physics": 1, "Statistics": 1, "Chemistry": 1}),
            "C": ("Very important — I want my work to directly solve real-world problems", {"Food Science and Technology": 2, "Data Science and Analytics": 1, "Pharmaceutical Science": 1}),
            "D": ("Extremely important — I want direct impact on health, markets or society", {"Pharmaceutical Science": 2, "Quantitative Finance": 2, "Data Science and Analytics": 1})
        }
    },
    {
        "id": "SCI_Q5",
        "text": "Which career path appeals most to you?",
        "options": {
            "A": ("Quantitative analyst or risk manager at a bank or hedge fund", {"Quantitative Finance": 2, "Mathematics": 1, "Statistics": 1}),
            "B": ("Data scientist or machine learning engineer", {"Data Science and Analytics": 2, "Statistics": 1}),
            "C": ("Research scientist in academia or a biotech lab", {"Life Sciences": 2, "Chemistry": 2, "Physics": 1}),
            "D": ("Pharmacist, drug developer or clinical researcher", {"Pharmaceutical Science": 2}),
            "E": ("Food technologist, nutritionist or product developer", {"Food Science and Technology": 2})
        }
    },
    {
        "id": "SCI_Q6",
        "text": "How comfortable are you with heavy mathematics and abstract reasoning?",
        "options": {
            "A": ("Very comfortable — I genuinely enjoy abstract maths and proofs", {"Mathematics": 2, "Physics": 1, "Quantitative Finance": 1}),
            "B": ("Comfortable with applied maths — statistics, modelling and data", {"Statistics": 2, "Data Science and Analytics": 2, "Quantitative Finance": 1}),
            "C": ("I prefer maths as a tool rather than the focus itself", {"Chemistry": 1, "Life Sciences": 1, "Pharmaceutical Science": 1, "Food Science and Technology": 1}),
            "D": ("I prefer experimental and observational work over mathematical theory", {"Life Sciences": 2, "Food Science and Technology": 2})
        }
    },
    {
        "id": "SCI_Q7",
        "text": "Which application of science excites you most?",
        "options": {
            "A": ("Understanding the origins of the universe, black holes or quantum mechanics", {"Physics": 2}),
            "B": ("Developing medicines that save lives", {"Pharmaceutical Science": 2, "Chemistry": 1, "Life Sciences": 1}),
            "C": ("Using algorithms to predict stock prices or manage financial risk", {"Quantitative Finance": 2, "Statistics": 1}),
            "D": ("Building AI systems that learn from data to make predictions", {"Data Science and Analytics": 2}),
            "E": ("Improving the safety, nutrition and sustainability of our food supply", {"Food Science and Technology": 2})
        }
    },
    {
        "id": "SCI_Q8",
        "text": "Which best describes your scientific personality?",
        "options": {
            "A": ("The theorist — I love abstract ideas and mathematical elegance", {"Mathematics": 2, "Physics": 1}),
            "B": ("The experimentalist — I love designing and running experiments to test hypotheses", {"Chemistry": 2, "Life Sciences": 2, "Physics": 1}),
            "C": ("The data scientist — I love finding patterns in large, messy datasets", {"Data Science and Analytics": 2, "Statistics": 2}),
            "D": ("The applied scientist — I want science to solve practical problems quickly", {"Food Science and Technology": 2, "Pharmaceutical Science": 2}),
            "E": ("The financial scientist — I want to apply quantitative tools to markets", {"Quantitative Finance": 2})
        }
    },
    {
        "id": "SCI_Q9",
        "text": "How important is it to you that your degree leads to a clear, defined career?",
        "options": {
            "A": ("Not important — I want intellectual freedom to explore wherever my curiosity leads", {"Mathematics": 2, "Physics": 2}),
            "B": ("Somewhat important — I want options but also a rough direction", {"Chemistry": 1, "Life Sciences": 1, "Statistics": 1}),
            "C": ("Very important — I want to know what job I am training for", {"Pharmaceutical Science": 2, "Food Science and Technology": 2, "Quantitative Finance": 1}),
            "D": ("Extremely important — I want a degree with clear, high-demand career outcomes", {"Quantitative Finance": 2, "Data Science and Analytics": 2})
        }
    },
    {
        "id": "SCI_Q10",
        "text": "Which identity feels most like you?",
        "options": {
            "A": ("I am a pure scientist — I follow curiosity wherever it leads, regardless of application", {"Mathematics": 2, "Physics": 2}),
            "B": ("I am a life scientist — I want to understand living systems and improve health", {"Life Sciences": 2, "Pharmaceutical Science": 1}),
            "C": ("I am a data person — I turn numbers into knowledge and predictions", {"Data Science and Analytics": 2, "Statistics": 2, "Quantitative Finance": 1}),
            "D": ("I am a chemist — I find beauty in molecular transformations", {"Chemistry": 2, "Pharmaceutical Science": 1}),
            "E": ("I am an applied scientist — I want science to solve tangible problems in the world", {"Food Science and Technology": 2, "Pharmaceutical Science": 1})
        }
    }
]


# ============================================================
# MUSIC (YST) DRILL-DOWN DATA
# ============================================================

MUSIC_PROGRAMMES = [
    "Audio Arts & Sciences", "Brass", "Composition",
    "Music & Society/ Music, Collaboration & Production", "Percussion", "Piano",
    "String & Harp", "Voice", "Woodwinds"
]

MUSIC_IDENTITY_STATEMENTS = {
    "Audio Arts & Sciences": "Based on your responses, you are someone who is as passionate about the technology of sound as the art of it. You thrive at the intersection of music, acoustics and engineering — recording, mixing and shaping sonic experiences. Your love for the technical side of audio production makes Audio Arts & Sciences a natural fit. Graduates work in recording studios, film sound, live events and audio technology.",
    "Brass": "Based on your responses, you are someone with a commanding musical presence and a love for the power and brilliance of brass instruments. You thrive in ensemble and orchestral settings where precision, projection and teamwork unite. Your dedication to your instrument and performance craft makes the Brass pathway a natural fit. Graduates pursue orchestral, chamber, military and freelance performance careers.",
    "Composition": "Based on your responses, you are someone who hears music in your head before it exists in the world. You thrive when translating inner musical ideas into scores, digital productions and sonic experiences for others to perform. Your creative drive and musical imagination makes Composition a natural fit. Graduates work as composers for concert music, film, games, theatre and multimedia.",
    "Music & Society/ Music, Collaboration & Production": "Based on your responses, you are someone who sees music not just as art but as a social and cultural force. You thrive exploring how music shapes communities, identities and histories, and how it can be a tool for education and change. Graduates work in music education, arts management, cultural policy, research and community music.",
    "Percussion": "Based on your responses, you are someone drawn to rhythm, energy and the unique diversity of the percussion world. You thrive in the challenge of mastering an enormous range of instruments and styles across classical, contemporary and world music. Graduates pursue orchestral, chamber, contemporary and cross-genre performance careers.",
    "Piano": "Based on your responses, you are someone with deep connection to the piano as your primary musical voice. You thrive in the demanding, intimate world of solo and collaborative piano performance, combining technical mastery with interpretive depth. Graduates pursue solo performance, collaborative piano, teaching and chamber music careers.",
    "String & Harp": "Based on your responses, you are someone whose musical identity is inseparable from your instrument — whether violin, viola, cello, double bass or harp. You thrive in the rich traditions of orchestral and chamber music, bringing precision and expressivity to every note. Graduates pursue orchestral, chamber and solo performance careers worldwide.",
    "Voice": "Based on your responses, you are someone whose instrument is your own body — you communicate music most naturally through singing. You thrive in the interpretive world of vocal performance, drawing audiences into the emotional world of opera, art song and choral music. Graduates pursue opera, oratorio, concert singing and teaching careers.",
    "Woodwinds": "Based on your responses, you are someone with a special connection to the lyrical, expressive world of woodwind instruments. You thrive in the demanding technical and musical requirements of orchestral and chamber playing. Graduates pursue orchestral, chamber, solo and teaching careers across classical and contemporary music."
}

MUSIC_DRILL_DOWN_QUESTIONS = [
    {
        "id": "MUS_Q1",
        "text": "What is your primary instrument or musical focus?",
        "options": {
            "A": ("Piano", {"Piano": 3}),
            "B": ("A string instrument (violin, viola, cello, double bass) or harp", {"String & Harp": 3}),
            "C": ("A woodwind instrument (flute, oboe, clarinet, bassoon, saxophone)", {"Woodwinds": 3}),
            "D": ("A brass instrument (trumpet, trombone, French horn, tuba)", {"Brass": 3}),
            "E": ("Percussion or drumkit", {"Percussion": 3})
        }
    },
    {
        "id": "MUS_Q2",
        "text": "If your primary instrument is voice, or if you have a strong interest beyond performance, which appeals most?",
        "options": {
            "A": ("Singing — classical voice, opera or art song", {"Voice": 3}),
            "B": ("Composing — writing original music for others to perform", {"Composition": 3}),
            "C": ("Music technology — recording, mixing and producing sound", {"Audio Arts & Sciences": 3}),
            "D": ("Music in society — education, culture and community", {"Music & Society/ Music, Collaboration & Production": 3}),
            "E": ("My answer above covered it — I am a performer first", {"Piano": 1, "String & Harp": 1, "Woodwinds": 1, "Brass": 1, "Percussion": 1})
        }
    },
    {
        "id": "MUS_Q3",
        "text": "What kind of musical environment do you thrive in?",
        "options": {
            "A": ("Alone at my instrument, practising and perfecting my technique", {"Piano": 2, "Voice": 1}),
            "B": ("In a large orchestra or ensemble with 50+ musicians", {"String & Harp": 2, "Brass": 2, "Woodwinds": 2, "Percussion": 1}),
            "C": ("In a studio, recording and producing music using technology", {"Audio Arts & Sciences": 2, "Composition": 1}),
            "D": ("In a community or educational setting, sharing music with others", {"Music & Society/ Music, Collaboration & Production": 2}),
            "E": ("At my desk composing — writing scores and hearing them in my head", {"Composition": 2})
        }
    },
    {
        "id": "MUS_Q4",
        "text": "Which best describes your musical identity?",
        "options": {
            "A": ("I am a performer — my purpose is to interpret and communicate music to audiences", {"Piano": 2, "Voice": 2, "String & Harp": 2, "Brass": 1, "Woodwinds": 1, "Percussion": 1}),
            "B": ("I am a creator — I want to write music that didn't exist before", {"Composition": 2}),
            "C": ("I am a technologist — I am as interested in sound engineering as in music itself", {"Audio Arts & Sciences": 2}),
            "D": ("I am an educator and advocate — I want music to reach and transform communities", {"Music & Society/ Music, Collaboration & Production": 2})
        }
    },
    {
        "id": "MUS_Q5",
        "text": "Which career path excites you most?",
        "options": {
            "A": ("Orchestral musician or soloist performing on concert stages worldwide", {"String & Harp": 2, "Brass": 2, "Woodwinds": 2, "Piano": 1, "Percussion": 1}),
            "B": ("Opera singer or concert vocalist", {"Voice": 2}),
            "C": ("Film composer, game music composer or concert hall composer", {"Composition": 2}),
            "D": ("Sound engineer, music producer or audio technology specialist", {"Audio Arts & Sciences": 2}),
            "E": ("Music educator, arts administrator or cultural policy professional", {"Music & Society/ Music, Collaboration & Production": 2})
        }
    },
    {
        "id": "MUS_Q6",
        "text": "How important is music technology in your musical vision?",
        "options": {
            "A": ("Central — I am as excited by DAWs, microphones and acoustics as I am by instruments", {"Audio Arts & Sciences": 3}),
            "B": ("Very important — I use technology as a core tool in composition and production", {"Composition": 2, "Audio Arts & Sciences": 1}),
            "C": ("Somewhat important — I use technology to support my performance or teaching", {"Music & Society/ Music, Collaboration & Production": 1, "Piano": 1}),
            "D": ("Not particularly important — I am a traditional performance-focused musician", {"String & Harp": 1, "Brass": 1, "Woodwinds": 1, "Voice": 1, "Percussion": 1, "Piano": 1})
        }
    },
    {
        "id": "MUS_Q7",
        "text": "Which music do you feel most connected to performing or creating?",
        "options": {
            "A": ("Classical orchestral and chamber music", {"String & Harp": 2, "Woodwinds": 2, "Brass": 2, "Piano": 1}),
            "B": ("Opera and vocal music", {"Voice": 2}),
            "C": ("Contemporary and experimental music", {"Composition": 2, "Percussion": 2, "Audio Arts & Sciences": 1}),
            "D": ("Music that serves communities — educational, therapeutic or accessible", {"Music & Society/ Music, Collaboration & Production": 2}),
            "E": ("Cross-genre — I want to explore everything from classical to jazz to world music", {"Percussion": 2, "Audio Arts & Sciences": 1, "Composition": 1})
        }
    },
    {
        "id": "MUS_Q8",
        "text": "Which best describes your broader relationship with music?",
        "options": {
            "A": ("Music is my craft — I dedicate myself to mastering my instrument above all", {"Piano": 2, "Voice": 2, "String & Harp": 1, "Brass": 1, "Woodwinds": 1}),
            "B": ("Music is my creative outlet — I express myself most through composing", {"Composition": 2}),
            "C": ("Music is a technology — I am fascinated by how sound works and can be shaped", {"Audio Arts & Sciences": 2}),
            "D": ("Music is a social force — I care about its role in culture, education and community", {"Music & Society/ Music, Collaboration & Production": 2})
        }
    },
    {
        "id": "MUS_Q9",
        "text": "How do you imagine your daily life as a music professional?",
        "options": {
            "A": ("Practising for hours, performing concerts and travelling internationally", {"Piano": 2, "Voice": 2, "String & Harp": 1, "Brass": 1, "Woodwinds": 1}),
            "B": ("Writing music at a desk or keyboard and hearing it realised by performers", {"Composition": 2}),
            "C": ("In a studio working with artists to capture and shape their sound", {"Audio Arts & Sciences": 2}),
            "D": ("Teaching, running workshops or managing arts programmes for communities", {"Music & Society/ Music, Collaboration & Production": 2}),
            "E": ("Rehearsing with an ensemble and performing a wide variety of repertoire", {"Percussion": 2, "Brass": 1, "Woodwinds": 1, "String & Harp": 1})
        }
    },
    {
        "id": "MUS_Q10",
        "text": "Which statement feels most like you?",
        "options": {
            "A": ("I am a dedicated instrumentalist — my whole musical life revolves around my instrument", {"Piano": 2, "String & Harp": 2, "Brass": 2, "Woodwinds": 2, "Percussion": 2}),
            "B": ("I am a singer — my voice is my instrument and my most honest form of expression", {"Voice": 2}),
            "C": ("I am a composer — I hear music in my head that the world hasn't heard yet", {"Composition": 2}),
            "D": ("I am a sound architect — I shape sonic experiences through technology", {"Audio Arts & Sciences": 2}),
            "E": ("I am a music advocate — I want music to be accessible and meaningful to everyone", {"Music & Society/ Music, Collaboration & Production": 2})
        }
    }
]


# ============================================================
# CLUSTER CONFIGURATION
# ============================================================

CLUSTER_CONFIG = {
    "cde": {
        "name": "CDE",
        "full_name": "College of Design and Engineering",
        "programmes": CDE_PROGRAMMES,
        "questions": CDE_DRILL_DOWN_QUESTIONS,
        "identity_statements": CDE_IDENTITY_STATEMENTS,
        "session_index": "cde_question_index",
        "session_responses": "cde_responses",
        "session_result": "cde_result",
        "drilldown_page": "cde_drilldown",
        "result_page": "cde_result_page",
        "emoji": "⚙️"
    },
    "computing": {
        "name": "Computing",
        "full_name": "School of Computing",
        "programmes": COMPUTING_PROGRAMMES,
        "questions": COMPUTING_DRILL_DOWN_QUESTIONS,
        "identity_statements": COMPUTING_IDENTITY_STATEMENTS,
        "session_index": "comp_question_index",
        "session_responses": "comp_responses",
        "session_result": "comp_result",
        "drilldown_page": "comp_drilldown",
        "result_page": "comp_result_page",
        "emoji": "💻"
    },
    "business": {
        "name": "Business",
        "full_name": "NUS Business School",
        "programmes": BUSINESS_PROGRAMMES,
        "questions": BUSINESS_DRILL_DOWN_QUESTIONS,
        "identity_statements": BUSINESS_IDENTITY_STATEMENTS,
        "session_index": "biz_question_index",
        "session_responses": "biz_responses",
        "session_result": "biz_result",
        "drilldown_page": "biz_drilldown",
        "result_page": "biz_result_page",
        "emoji": "💼"
    },
    "humanities": {
        "name": "Humanities & Social Sciences",
        "full_name": "College of Humanities and Sciences",
        "programmes": HUMANITIES_PROGRAMMES,
        "questions": HUMANITIES_DRILL_DOWN_QUESTIONS,
        "identity_statements": HUMANITIES_IDENTITY_STATEMENTS,
        "session_index": "hum_question_index",
        "session_responses": "hum_responses",
        "session_result": "hum_result",
        "drilldown_page": "hum_drilldown",
        "result_page": "hum_result_page",
        "emoji": "📚"
    },
    "sciences": {
        "name": "Sciences",
        "full_name": "Faculty of Science",
        "programmes": SCIENCES_PROGRAMMES,
        "questions": SCIENCES_DRILL_DOWN_QUESTIONS,
        "identity_statements": SCIENCES_IDENTITY_STATEMENTS,
        "session_index": "sci_question_index",
        "session_responses": "sci_responses",
        "session_result": "sci_result",
        "drilldown_page": "sci_drilldown",
        "result_page": "sci_result_page",
        "emoji": "🔬"
    },
    "music": {
        "name": "Music",
        "full_name": "Yong Siew Toh Conservatory of Music",
        "programmes": MUSIC_PROGRAMMES,
        "questions": MUSIC_DRILL_DOWN_QUESTIONS,
        "identity_statements": MUSIC_IDENTITY_STATEMENTS,
        "session_index": "mus_question_index",
        "session_responses": "mus_responses",
        "session_result": "mus_result",
        "drilldown_page": "mus_drilldown",
        "result_page": "mus_result_page",
        "emoji": "🎵"
    }
}


# ============================================================
# FACULTY-TO-CLUSTER MAPPING (FIX for drill-down trigger bug)
# ============================================================
# This mapping uses the Faculty column from the Programmes Excel sheet
# to determine which cluster a programme belongs to. This is more
# reliable than matching programme names (which can have typos or
# appear in multiple clusters like "Computer Engineering").
#
# Each key is a lowercase substring that will be checked against the
# Faculty column value. The mapping is checked in order, so more
# specific keys should come first.

FACULTY_TO_CLUSTER = {
    "design and engineering": "cde",
    "cde": "cde",
    "computing": "computing",
    "school of computing": "computing",
    "business": "business",
    "yong siew toh": "music",
    "conservatory of music": "music",
    "music": "music",
    # CHS contains both humanities and sciences — handled specially below
}

# Programmes under CHS that belong to the "sciences" cluster
# (everything else in CHS maps to "humanities")
CHS_SCIENCES_SET = {s.lower() for s in SCIENCES_PROGRAMMES}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _normalise_name(s):
    """Normalise a programme name for comparison: lowercase, strip, fix known typos."""
    TYPO_MAP = {
        "chemistyry": "chemistry",
        "landscapre architecuture": "landscape architecture",
        "electrical englineering": "electrical engineering",
    }
    s = s.lower().replace('&', 'and').replace('  ', ' ').strip()
    return TYPO_MAP.get(s, s)


def get_cluster_for_programme(programme_name: str) -> str | None:
    """Return the cluster key for a given programme name — normalised exact match,
    with tolerance for known Excel typos (e.g. Chemistyry -> Chemistry).

    NOTE: This is the name-only fallback. Prefer get_cluster_for_result() which
    also uses the Faculty column for accurate detection."""
    pname_norm = _normalise_name(programme_name)

    for cluster_key, config in CLUSTER_CONFIG.items():
        for prog in config["programmes"]:
            if _normalise_name(prog) == pname_norm:
                return cluster_key
    return None


def get_cluster_for_result(programme_name: str, faculty: str) -> str | None:
    """Determine cluster using Faculty column first, programme name as fallback.

    This fixes the bug where programmes like 'Computer Engineering' (which exist
    in both CDE and Computing) were always mapped to CDE due to dict ordering.
    By using the Faculty column from the Excel data, we get the correct cluster."""
    faculty_lower = str(faculty).lower().strip()

    # 1) Check explicit faculty-to-cluster mappings
    for key, cluster in FACULTY_TO_CLUSTER.items():
        if key in faculty_lower:
            return cluster

    # 2) Handle CHS (Humanities and Sciences) — split into humanities vs sciences
    if "humanities" in faculty_lower or "sciences" in faculty_lower or "chs" in faculty_lower:
        pname_norm = _normalise_name(programme_name)
        if pname_norm in CHS_SCIENCES_SET:
            return "sciences"
        # Check if it's a known humanities programme
        for prog in HUMANITIES_PROGRAMMES:
            if _normalise_name(prog) == pname_norm:
                return "humanities"
        # Default CHS programmes to humanities
        return "humanities"

    # 3) Fallback to programme-name-only matching
    return get_cluster_for_programme(programme_name)


def check_cluster_trigger(matches_df: pd.DataFrame) -> list:
    """Return list of cluster keys where 2+ of top 8 results belong to that cluster.

    Uses Faculty column (via get_cluster_for_result) for accurate cluster detection.
    Threshold of 2 (out of 8 shown) ensures smaller clusters like Computing, Sciences
    and Music can trigger alongside larger ones like CDE."""
    top_results = matches_df.head(8)
    triggered = []
    cluster_counts = {key: 0 for key in CLUSTER_CONFIG}

    for _, row in top_results.iterrows():
        cluster = get_cluster_for_result(row['Programme_Name'], row['Faculty'])
        if cluster:
            cluster_counts[cluster] += 1

    for cluster_key, count in cluster_counts.items():
        if count >= 2:
            triggered.append(cluster_key)

    return triggered


def calculate_cluster_scores(responses: Dict[str, str], questions: list, programmes: list) -> str:
    """Calculate best-fit programme from drill-down responses"""
    programme_scores = {prog: 0 for prog in programmes}
    for q_id, chosen_option in responses.items():
        question = next((q for q in questions if q['id'] == q_id), None)
        if question and chosen_option in question['options']:
            _, score_dict = question['options'][chosen_option]
            for prog, points in score_dict.items():
                if prog in programme_scores:
                    programme_scores[prog] += points
    return max(programme_scores, key=programme_scores.get)


# ============================================================
# SESSION STATE
# ============================================================

def init_session_state():
    defaults = {
        'page': 'welcome',
        'responses': {},
        'current_question': 0,
        'results': None,
        # CDE
        'cde_responses': {}, 'cde_result': None, 'cde_question_index': 0,
        # Computing
        'comp_responses': {}, 'comp_result': None, 'comp_question_index': 0,
        # Business
        'biz_responses': {}, 'biz_result': None, 'biz_question_index': 0,
        # Humanities
        'hum_responses': {}, 'hum_result': None, 'hum_question_index': 0,
        # Sciences
        'sci_responses': {}, 'sci_result': None, 'sci_question_index': 0,
        # Music
        'mus_responses': {}, 'mus_result': None, 'mus_question_index': 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ============================================================
# SCORING ALGORITHM
# ============================================================

def calculate_riasec_scores(responses: Dict[str, int], questions_df: pd.DataFrame) -> Dict[str, float]:
    riasec_scores = {'R': 0, 'I': 0, 'A': 0, 'S': 0, 'E': 0, 'C': 0}
    for q_id, response in responses.items():
        if q_id.startswith('Q') and int(q_id[1:]) <= 24:
            question = questions_df[questions_df['Question_ID'] == q_id].iloc[0]
            riasec_type = question['RIASEC_Type']
            riasec_scores[riasec_type] += (response - 1)
    for code in riasec_scores:
        riasec_scores[code] = (riasec_scores[code] / 16) * 100
    return riasec_scores


def get_top_riasec(riasec_scores: Dict[str, float], n: int = 3) -> List[str]:
    sorted_codes = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)
    return [code for code, score in sorted_codes[:n]]


def get_top_values(responses: Dict[str, int], n: int = 3) -> List[str]:
    value_mapping = {
        'Q25': 'high-salary', 'Q26': 'helping-people',
        'Q27': 'creativity', 'Q28': 'technology', 'Q29': 'work-life-balance'
    }
    value_responses = {label: responses[q_id] for q_id, label in value_mapping.items() if q_id in responses}
    sorted_values = sorted(value_responses.items(), key=lambda x: x[1], reverse=True)
    return [value for value, score in sorted_values[:n]]


def match_programmes(riasec_scores: Dict[str, float], top_values: List[str],
                     programmes_df: pd.DataFrame, top_n: int = 8) -> pd.DataFrame:
    top_riasec = get_top_riasec(riasec_scores, n=3)
    scores = []

    for idx, row in programmes_df.iterrows():
        score = 0
        match_details = []
        prog_primary = row['Primary_RIASEC']
        prog_secondary = row['Secondary_RIASEC']
        prog_tertiary = row['Tertiary_RIASEC'] if pd.notna(row['Tertiary_RIASEC']) else None
        prog_codes = [c for c in [prog_primary, prog_secondary, prog_tertiary] if c]

        r1_weight = riasec_scores[top_riasec[0]] / 100
        if top_riasec[0] == prog_primary:
            pts = round(5 * r1_weight, 2)
            score += pts
            match_details.append(f"Your top interest ({RIASEC_NAMES[top_riasec[0]]}, {riasec_scores[top_riasec[0]]:.0f}%) matches the programme's primary focus (+{pts:.1f})")
        elif top_riasec[0] == prog_secondary:
            pts = round(3 * r1_weight, 2)
            score += pts
            match_details.append(f"Your top interest ({RIASEC_NAMES[top_riasec[0]]}) matches a key component (+{pts:.1f})")

        if len(top_riasec) > 1:
            r2_weight = riasec_scores[top_riasec[1]] / 100
            if top_riasec[1] == prog_primary:
                pts = round(3 * r2_weight, 2)
                score += pts
                match_details.append(f"Your 2nd interest ({RIASEC_NAMES[top_riasec[1]]}) matches the programme's primary focus (+{pts:.1f})")
            elif top_riasec[1] == prog_secondary:
                pts = round(2 * r2_weight, 2)
                score += pts
                match_details.append(f"Your 2nd interest ({RIASEC_NAMES[top_riasec[1]]}) matches a component (+{pts:.1f})")
            elif prog_tertiary and top_riasec[1] == prog_tertiary:
                pts = round(1 * r2_weight, 2)
                score += pts
                match_details.append(f"Your 2nd interest aligns with programme aspects (+{pts:.1f})")

        if len(top_riasec) > 2 and top_riasec[2] == prog_primary:
            score += 1
            match_details.append(f"Your 3rd interest ({RIASEC_NAMES[top_riasec[2]]}) matches the programme focus (+1.0)")

        prog_top2 = [prog_primary, prog_secondary]
        if len(top_riasec) >= 2 and top_riasec[0] in prog_top2 and top_riasec[1] in prog_top2:
            score += 2
            match_details.append("Strong alignment: Your top 2 interests match this programme's core profile (+2.0)")

        if top_riasec[0] not in prog_codes:
            score -= 1
            match_details.append(f"Your top interest ({RIASEC_NAMES[top_riasec[0]]}) is not a core focus of this programme (-1.0)")

        if pd.notna(row['Value_Tags']):
            prog_values = [v.strip() for v in str(row['Value_Tags']).split(',')]
            value_q_map = {'high-salary': 'Q25', 'helping-people': 'Q26',
                           'creativity': 'Q27', 'technology': 'Q28', 'work-life-balance': 'Q29'}
            value_matches = []
            for val in top_values:
                val_score = st.session_state.responses.get(value_q_map.get(val, ''), 0)
                if val in prog_values and val_score >= 4:
                    score += 2
                    value_matches.append(val)
            if value_matches:
                match_details.append(f"Strongly shares your values: {', '.join(value_matches)} (+2.0 each)")

        scores.append({
            'Programme_ID': row['Programme_ID'],
            'Programme_Name': row['Programme_Name'],
            'Faculty': row['Faculty'],
            'Primary_RIASEC': prog_primary,
            'Secondary_RIASEC': prog_secondary,
            'Tertiary_RIASEC': prog_tertiary,
            'Value_Tags': row['Value_Tags'],
            'Match_Score': round(score, 1),
            'Match_Details': match_details
        })

    results_df = pd.DataFrame(scores)
    results_df = results_df.sort_values('Match_Score', ascending=False).head(top_n)
    return results_df


# ============================================================
# PAGE: WELCOME
# ============================================================

def show_welcome_page():
    st.markdown('<div class="main-header">🎓 NUS Smart Advisor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Discover Your Best-Fit NUS Undergraduate Programme</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        ### Welcome! 👋

        This tool helps you discover NUS undergraduate programmes that match your:
        - **Interests** (what you enjoy doing)
        - **Work Style** (how you like to work)
        - **Values** (what matters to you in a career)

        #### How it works:
        1. **Answer 29 questions** (about 3 minutes)
        2. **Get your RIASEC profile** — your personal interest type
        3. **See your top 8 programme matches** with explanations
        4. **Explore deeper** — if your results cluster around a faculty, answer 10 more targeted questions for a single best-fit recommendation

        #### What is RIASEC?
        A research-backed framework identifying 6 interest types:
        - **R**ealistic · **I**nvestigative · **A**rtistic · **S**ocial · **E**nterprising · **C**onventional
        ---
        """)

        st.info("💡 **Tip:** Answer honestly based on what genuinely interests you, not what you think you *should* like.")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Start Questionnaire", type="primary", use_container_width=True):
            st.session_state.page = 'questionnaire'
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("🛠️ Developer Test Mode"):
            st.warning("⚠️ For testing only — skips all 29 questions with a preset profile.")
            selected_profile = st.selectbox("Select a test profile:", list(TEST_PROFILES.keys()))
            if st.button("⚡ Load Profile & Go to Results", use_container_width=True):
                st.session_state.responses = TEST_PROFILES[selected_profile].copy()
                st.session_state.current_question = len(TEST_PROFILES[selected_profile])
                st.session_state.page = 'results'
                st.rerun()

        with st.expander("📊 About This Tool"):
            st.markdown("""
            Developed as a Final Year Project by Jiajian (Mechanical Engineering, NUS CDE).

            Uses **Holland's RIASEC Theory**, **Person-Environment Fit** research
            and covers all **75 NUS undergraduate programmes**.
            """)


# ============================================================
# PAGE: QUESTIONNAIRE (with auto-advance)
# ============================================================

def show_questionnaire_page(questions_df):
    st.markdown('<div class="main-header">📝 Questionnaire</div>', unsafe_allow_html=True)

    total_questions = len(questions_df)
    current = st.session_state.current_question
    progress = current / total_questions

    st.progress(progress)
    st.markdown(f"**Question {current + 1} of {total_questions}**")

    question = questions_df.iloc[current]
    q_id = question['Question_ID']
    category = question['Category']
    text = question['Question_Text']

    st.markdown(f"### {category}")
    st.markdown(f"*{text}*")
    st.markdown("<br>", unsafe_allow_html=True)

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
        index=None,
        key=f"q_{q_id}_{current}",
        horizontal=False
    )

    # Auto-advance when an option is selected
    if response is not None:
        st.session_state.responses[q_id] = response
        time.sleep(0.4)
        if current < total_questions - 1:
            st.session_state.current_question += 1
        else:
            st.session_state.page = 'results'
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if current > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.page = 'welcome'
            st.session_state.responses = {}
            st.session_state.current_question = 0
            st.rerun()


# ============================================================
# PAGE: RESULTS
# ============================================================

def show_results_page(questions_df, programmes_df, riasec_desc_df):
    st.markdown('<div class="main-header">🎯 Your Results</div>', unsafe_allow_html=True)

    riasec_scores = calculate_riasec_scores(st.session_state.responses, questions_df)
    top_riasec = get_top_riasec(riasec_scores, n=3)
    top_values = get_top_values(st.session_state.responses, n=3)
    matches = match_programmes(riasec_scores, top_values, programmes_df, top_n=8)

    st.markdown("## 📊 Your RIASEC Profile")
    col1, col2 = st.columns([1, 1])

    with col1:
        categories = list(RIASEC_NAMES.values())
        scores_list = [riasec_scores[code] for code in RIASEC_NAMES.keys()]
        fig = go.Figure(data=go.Scatterpolar(
            r=scores_list, theta=categories, fill='toself',
            fillcolor='rgba(0, 61, 124, 0.2)',
            line=dict(color='#003D7C', width=2)
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False, height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Your Top Interests:")
        for i, code in enumerate(top_riasec, 1):
            score = riasec_scores[code]
            desc = riasec_desc_df[riasec_desc_df['Code'] == code].iloc[0]['Description']
            st.markdown(f"**{i}. {RIASEC_NAMES[code]} ({code}) — {score:.1f}%**  \n{desc}")
        st.markdown("### Your Top Values:")
        for i, value in enumerate(top_values, 1):
            st.markdown(f"{i}. {value.replace('-', ' ').title()}")

    st.markdown("---")
    st.markdown("## 🎓 Your Top Programme Matches")
    st.markdown("*These programmes best align with your interests and values*")

    for rank, (idx, row) in enumerate(matches.iterrows(), 1):
        tertiary_html = f'<span class="riasec-badge">{row["Tertiary_RIASEC"]} - {RIASEC_NAMES[row["Tertiary_RIASEC"]]}</span>' if pd.notna(row['Tertiary_RIASEC']) else ''
        st.markdown(f"""
        <div class="recommendation-card">
            <h3>{rank}. {row['Programme_Name']}
                <span class="score-badge">Match: {row['Match_Score']:.1f} pts</span>
            </h3>
            <p><strong>Faculty:</strong> {row['Faculty']}</p>
            <p>
                <strong>RIASEC Profile:</strong>
                <span class="riasec-badge">{row['Primary_RIASEC']} - {RIASEC_NAMES[row['Primary_RIASEC']]}</span>
                <span class="riasec-badge">{row['Secondary_RIASEC']} - {RIASEC_NAMES[row['Secondary_RIASEC']]}</span>
                {tertiary_html}
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📋 Why this match?"):
            for detail in row['Match_Details']:
                st.markdown(f"- {detail}")
            st.markdown(f"\n**Programme Values:** {row['Value_Tags']}")

    # Drill-down triggers
    triggered_clusters = check_cluster_trigger(matches)
    if triggered_clusters:
        st.markdown("---")
        st.markdown("### 🔍 Want to go deeper?")
        st.markdown("*2 or more of your top 8 matches belong to the same faculty — answer 10 more focused questions to find your single best-fit programme within that faculty.*")

        for cluster_key in triggered_clusters:
            config = CLUSTER_CONFIG[cluster_key]
            st.info(f"**{config['emoji']} {config['name']} programmes dominate your results!** Answer 10 more questions to find your best-fit {config['name']} programme.")
            if st.button(f"{config['emoji']} Explore {config['name']} Further", type="primary", use_container_width=True, key=f"btn_{cluster_key}"):
                st.session_state[config['session_responses']] = {}
                st.session_state[config['session_index']] = 0
                st.session_state.page = config['drilldown_page']
                st.rerun()

    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Retake Quiz", use_container_width=True):
            st.session_state.page = 'welcome'
            st.session_state.responses = {}
            st.session_state.current_question = 0
            st.rerun()

    with col2:
        results_text = f"""NUS SMART ADVISOR - YOUR RESULTS

YOUR RIASEC PROFILE:
1. {RIASEC_NAMES[top_riasec[0]]} ({riasec_scores[top_riasec[0]]:.1f}%)
2. {RIASEC_NAMES[top_riasec[1]]} ({riasec_scores[top_riasec[1]]:.1f}%)
3. {RIASEC_NAMES[top_riasec[2]]} ({riasec_scores[top_riasec[2]]:.1f}%)

YOUR TOP VALUES: {', '.join([v.replace('-', ' ').title() for v in top_values])}

YOUR TOP PROGRAMME MATCHES:
"""
        for rank, (idx, row) in enumerate(matches.iterrows(), 1):
            results_text += f"\n{rank}. {row['Programme_Name']} ({row['Faculty']}) - Score: {row['Match_Score']:.1f}\n"

        st.download_button("📥 Download Results", data=results_text,
                           file_name="nus_smart_advisor_results.txt",
                           mime="text/plain", use_container_width=True)

    with col3:
        if st.button("ℹ️ About Results", use_container_width=True):
            st.info("""
            **How matching works:**
            - Scores scale with how strongly you answered each RIASEC dimension
            - Primary matches score higher than secondary matches
            - Small penalty when your top interest is absent from a programme
            - Values boost score only if you rated them 4 or 5 (important to you)
            - Perfect top-2 alignment gives a bonus

            **Next steps:**
            - Research your top matches on the NUS website
            - Talk to current students in these programmes
            - Use the drill-down feature for a more specific recommendation!
            """)


# ============================================================
# GENERIC DRILL-DOWN PAGES
# ============================================================

def show_drilldown_page(cluster_key: str):
    config = CLUSTER_CONFIG[cluster_key]
    questions = config['questions']
    total = len(questions)
    current = st.session_state[config['session_index']]

    st.markdown(f'<div class="main-header">{config["emoji"]} {config["name"]} Explorer</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">Let\'s find your best-fit {config["name"]} programme</div>', unsafe_allow_html=True)

    st.progress(current / total)
    st.markdown(f"**Question {current + 1} of {total}**")

    question = questions[current]
    q_id = question['id']
    options = question['options']

    st.markdown(f"### {question['text']}")
    st.markdown("<br>", unsafe_allow_html=True)

    response = st.radio(
        "Choose the option that feels most like you:",
        options=list(options.keys()),
        format_func=lambda x: options[x][0],
        index=None,
        key=f"drill_{q_id}_{current}",
        horizontal=False
    )

    # Auto-advance
    if response is not None:
        st.session_state[config['session_responses']][q_id] = response
        time.sleep(0.4)
        if current < total - 1:
            st.session_state[config['session_index']] += 1
        else:
            st.session_state.page = config['result_page']
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        if current > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state[config['session_index']] -= 1
                st.rerun()
    with col2:
        if st.button("⬅️ Back to Results", use_container_width=True):
            st.session_state.page = 'results'
            st.rerun()


def show_drilldown_result_page(cluster_key: str):
    config = CLUSTER_CONFIG[cluster_key]

    best_fit = calculate_cluster_scores(
        st.session_state[config['session_responses']],
        config['questions'],
        config['programmes']
    )
    st.session_state[config['session_result']] = best_fit

    statement = config['identity_statements'].get(best_fit, "This programme is a strong fit based on your responses.")

    st.markdown(f'<div class="main-header">🎯 Your Best-Fit {config["name"]} Programme</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="recommendation-card">
        <h2>{config['emoji']} {best_fit}</h2>
        <p style="font-size: 1.1rem; line-height: 1.8;">{statement}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔗 What's Next?")
    st.markdown(f"""
    - 🌐 [Explore {best_fit} on NUS website](https://www.nus.edu.sg/admissions/undergraduate/programmes.html)
    - 💬 Talk to current {best_fit} students
    - 📋 Go back to Stage 1 results to see the full picture
    """)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to My Programme Matches", use_container_width=True):
            st.session_state.page = 'results'
            st.rerun()
    with col2:
        if st.button(f"🔄 Retake {config['name']} Explorer", use_container_width=True):
            st.session_state[config['session_responses']] = {}
            st.session_state[config['session_result']] = None
            st.session_state[config['session_index']] = 0
            st.session_state.page = config['drilldown_page']
            st.rerun()


# ============================================================
# MAIN
# ============================================================

def main():
    init_session_state()
    questions_df, programmes_df, values_df, riasec_desc_df = load_data()

    with st.sidebar:
        st.markdown("### 🎓 NUS Smart Advisor")
        st.markdown("---")
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'welcome'
            st.rerun()
        st.markdown("---")
        st.markdown("""
        **Smart Advisor Tool**
        Version 3.0

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

    page = st.session_state.page

    if page == 'welcome':
        show_welcome_page()
    elif page == 'questionnaire':
        show_questionnaire_page(questions_df)
    elif page == 'results':
        show_results_page(questions_df, programmes_df, riasec_desc_df)
    else:
        # Generic routing for all drill-down pages
        for cluster_key, config in CLUSTER_CONFIG.items():
            if page == config['drilldown_page']:
                show_drilldown_page(cluster_key)
                return
            elif page == config['result_page']:
                show_drilldown_result_page(cluster_key)
                return


if __name__ == "__main__":
    main()