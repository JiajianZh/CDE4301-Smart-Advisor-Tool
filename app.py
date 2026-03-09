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
    """Load the Excel data file"""
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

# Test profiles for developer mode
TEST_PROFILES = {
    "Engineering (R+I)": {
        'Q1': 5, 'Q2': 5, 'Q3': 5, 'Q4': 5,   # R
        'Q5': 5, 'Q6': 5, 'Q7': 5, 'Q8': 5,   # I
        'Q9': 2, 'Q10': 2, 'Q11': 2, 'Q12': 2, # A
        'Q13': 2, 'Q14': 2, 'Q15': 2, 'Q16': 2, # S
        'Q17': 3, 'Q18': 3, 'Q19': 3, 'Q20': 3, # E
        'Q21': 3, 'Q22': 3, 'Q23': 3, 'Q24': 3, # C
        'Q25': 4, 'Q26': 2, 'Q27': 3, 'Q28': 5, 'Q29': 3
    },
    "Business (E+C)": {
        'Q1': 2, 'Q2': 2, 'Q3': 2, 'Q4': 2,
        'Q5': 3, 'Q6': 3, 'Q7': 3, 'Q8': 3,
        'Q9': 2, 'Q10': 2, 'Q11': 2, 'Q12': 2,
        'Q13': 3, 'Q14': 3, 'Q15': 3, 'Q16': 3,
        'Q17': 5, 'Q18': 5, 'Q19': 5, 'Q20': 5,
        'Q21': 5, 'Q22': 5, 'Q23': 5, 'Q24': 5,
        'Q25': 5, 'Q26': 2, 'Q27': 3, 'Q28': 3, 'Q29': 3
    },
    "Arts/Social (A+S)": {
        'Q1': 2, 'Q2': 2, 'Q3': 2, 'Q4': 2,
        'Q5': 3, 'Q6': 3, 'Q7': 3, 'Q8': 3,
        'Q9': 5, 'Q10': 5, 'Q11': 5, 'Q12': 5,
        'Q13': 5, 'Q14': 5, 'Q15': 5, 'Q16': 5,
        'Q17': 2, 'Q18': 2, 'Q19': 2, 'Q20': 2,
        'Q21': 2, 'Q22': 2, 'Q23': 2, 'Q24': 2,
        'Q25': 2, 'Q26': 5, 'Q27': 5, 'Q28': 2, 'Q29': 4
    },
    "Computing (I+R)": {
        'Q1': 4, 'Q2': 4, 'Q3': 4, 'Q4': 4,
        'Q5': 5, 'Q6': 5, 'Q7': 5, 'Q8': 5,
        'Q9': 2, 'Q10': 2, 'Q11': 2, 'Q12': 2,
        'Q13': 2, 'Q14': 2, 'Q15': 2, 'Q16': 2,
        'Q17': 3, 'Q18': 3, 'Q19': 3, 'Q20': 3,
        'Q21': 3, 'Q22': 3, 'Q23': 3, 'Q24': 3,
        'Q25': 4, 'Q26': 2, 'Q27': 3, 'Q28': 5, 'Q29': 3
    }
}


# ============================================================
# CDE DRILL-DOWN DATA
# ============================================================

CDE_PROGRAMMES = [
    "Architecture",
    "Biomedical Engineering",
    "Chemical Engineering",
    "Civil Engineering",
    "Computer Engineering",
    "Electrical Engineering",
    "Engineering Science",
    "Environmental and Sustainability Engineering",
    "Industrial Design",
    "Industrial and Systems Engineering",
    "Infrastructure and Project Management",
    "Landscape Architecture",
    "Materials Science and Engineering",
    "Mechanical Engineering",
    "Robotics and Machine Intelligence"
]

CDE_IDENTITY_STATEMENTS = {
    "Architecture": "Based on your responses, you are someone who sees the world through space, form and human experience. You thrive when you can blend creative vision with technical precision, turning ideas into physical environments that people live and work in. Your love for design, visual thinking and spatial reasoning makes Architecture a natural fit. Graduates often go on to become licensed architects, urban designers, or design consultants shaping Singapore's and the world's built environment.",
    "Biomedical Engineering": "Based on your responses, you are someone who sits at the intersection of science and humanity — you want technology to heal. You thrive in lab environments where biology meets engineering, solving problems that directly improve patient lives. Your interest in biology, chemistry and medical applications, combined with an engineering mindset, makes Biomedical Engineering your natural home. Graduates often work in medical device companies, hospitals, research institutes or pursue medicine.",
    "Chemical Engineering": "Based on your responses, you are someone who thinks at the molecular level — fascinated by how materials and substances transform and interact. You thrive in lab and process environments, designing systems that turn raw materials into useful products at scale. Your strength in chemistry and mathematics, combined with a love for systematic problem-solving, makes Chemical Engineering a strong fit. Graduates work in pharmaceuticals, petrochemicals, food technology and sustainability sectors.",
    "Civil Engineering": "Based on your responses, you are someone who thinks big — you want to build things that last generations. You thrive when working on large-scale physical challenges, from bridges and tunnels to water systems and transport networks. Your preference for tangible, real-world problems and your interest in mathematics and physics makes Civil Engineering a natural fit. Graduates shape the infrastructure of cities and countries, working with government bodies, construction firms and consultancies.",
    "Computer Engineering": "Based on your responses, you are someone who lives at the boundary of hardware and software — you love understanding how machines think and communicate. You thrive when coding, designing circuits or building systems that bridge the physical and digital worlds. Your passion for computing, electronics and logical problem-solving makes Computer Engineering your natural home. Graduates work in tech companies, semiconductor firms, cybersecurity and embedded systems across the globe.",
    "Electrical Engineering": "Based on your responses, you are someone energised by the invisible forces that power the modern world. You thrive when designing and analysing electrical systems, from power grids to microchips to wireless communications. Your strength in physics and mathematics, combined with a fascination for electronics and energy, makes Electrical Engineering a strong fit. Graduates work in energy, telecommunications, semiconductor and smart systems industries.",
    "Engineering Science": "Based on your responses, you are someone who loves engineering at its most fundamental — you want to understand the deep principles behind how things work before building them. You thrive in intellectually challenging environments that blend mathematics, physics and computational thinking. Your curiosity-driven, analytical mindset makes Engineering Science a natural fit. Graduates are highly versatile, going into research, finance, data science, defence technology and advanced engineering roles.",
    "Environmental and Sustainability Engineering": "Based on your responses, you are someone driven by purpose — you want engineering to protect and restore the planet. You thrive when working on challenges that sit at the intersection of technical solutions and environmental impact, from clean water systems to carbon reduction. Your interest in environmental science, chemistry and sustainability makes this programme a natural fit. Graduates work in environmental consultancies, government agencies, green energy firms and international organisations.",
    "Industrial Design": "Based on your responses, you are someone who believes great design improves everyday life. You thrive in creative studio environments, sketching, prototyping and refining products that are both beautiful and functional. Your blend of artistic sensibility, human empathy and technical curiosity makes Industrial Design a natural fit. Graduates work as product designers, UX designers and innovation consultants in consumer electronics, furniture, healthcare and lifestyle industries.",
    "Industrial and Systems Engineering": "Based on your responses, you are someone who sees inefficiency as a problem worth solving. You thrive when optimising complex systems — whether it's a supply chain, a hospital workflow or a manufacturing process. Your analytical mindset, love for data and ability to see the big picture makes Industrial and Systems Engineering a natural fit. Graduates work in operations, logistics, consulting, data analytics and management roles across virtually every industry.",
    "Infrastructure and Project Management": "Based on your responses, you are someone who makes things happen at scale. You thrive when coordinating large teams, managing timelines and budgets, and delivering complex projects from vision to reality. Your strength in planning, systems thinking and leadership makes Infrastructure and Project Management a natural fit. Graduates become project managers, quantity surveyors and construction consultants, delivering major infrastructure projects across Singapore and beyond.",
    "Landscape Architecture": "Based on your responses, you are someone who sees nature and human spaces as inseparable. You thrive when designing outdoor environments — parks, waterfronts, green corridors — that balance ecological health with human wellbeing. Your love for spatial design, environmental sensitivity and creative thinking makes Landscape Architecture a natural fit. Graduates work with urban planning agencies, landscape consultancies and environmental design firms shaping liveable cities.",
    "Materials Science and Engineering": "Based on your responses, you are someone fascinated by what things are made of and why they behave the way they do. You thrive in lab environments, experimenting with metals, polymers, ceramics and composites to unlock new material properties. Your interest in chemistry, physics and hands-on experimentation makes Materials Science and Engineering a natural fit. Graduates work in semiconductor, aerospace, biomedical and advanced manufacturing industries.",
    "Mechanical Engineering": "Based on your responses, you are someone who sees the world as a system of forces, motion and energy waiting to be harnessed. You thrive when designing, building and testing physical things — from engines and robots to medical devices and renewable energy systems. Your love for physics, mathematics and hands-on making makes Mechanical Engineering a natural fit. Graduates are among the most versatile engineers, working across aerospace, automotive, robotics, energy and manufacturing industries.",
    "Robotics and Machine Intelligence": "Based on your responses, you are someone captivated by the idea of machines that can sense, think and act. You thrive at the cutting edge — combining mechanical engineering, electronics and artificial intelligence to build systems that were once science fiction. Your passion for coding, intelligent systems and pushing boundaries makes Robotics and Machine Intelligence a natural fit. Graduates are at the forefront of automation, AI research, autonomous vehicles and smart manufacturing."
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
    "Computer Science",
    "Artificial Intelligence",
    "Information Security",
    "Computer Engineering",
    "Business Analytics",
    "Business Artificial Intelligence Systems"
]

COMPUTING_IDENTITY_STATEMENTS = {
    "Computer Science": "Based on your responses, you are someone who is energised by abstract thinking and elegant problem-solving. You gravitate toward logic, algorithms and building software systems from the ground up. You are happiest when given a hard problem, a blank screen and the freedom to engineer a solution. Your love for computational theory and software development makes Computer Science a natural fit. Graduates work as software engineers, researchers and tech leads at top technology companies and research institutions worldwide.",
    "Artificial Intelligence": "Based on your responses, you are someone captivated by the idea of machines that can learn, reason and make decisions. You are drawn to the cutting edge — where mathematics, data and computing collide to create intelligent systems. Your passion for algorithms, pattern recognition and the future of technology makes Artificial Intelligence a natural fit. Graduates work in AI research labs, tech giants, autonomous systems and healthcare technology, shaping how machines understand our world.",
    "Information Security": "Based on your responses, you are someone who thinks like both a builder and a protector — you want to understand systems deeply enough to defend them. You are drawn to the challenge of outsmarting attackers, securing data and building trustworthy digital infrastructure. Your analytical mindset, attention to detail and interest in the cat-and-mouse world of cybersecurity makes Information Security a natural fit. Graduates work in cybersecurity firms, government agencies, banking and critical infrastructure protection.",
    "Computer Engineering": "Based on your responses, you are someone who lives at the boundary of hardware and software — you love understanding how machines think at the deepest level. You thrive when building systems that bridge the physical and digital worlds, from chips and circuits to embedded software. Your passion for both electronics and computing makes Computer Engineering a natural fit. Graduates work in semiconductor companies, tech hardware firms, robotics and IoT industries.",
    "Business Analytics": "Based on your responses, you are someone who sees data as a lens for better decisions. You are drawn to the intersection of technology and business — turning messy real-world data into clear insights that drive strategy. Your blend of analytical thinking, interest in statistics and ability to communicate findings makes Business Analytics a natural fit. Graduates work as data analysts, business intelligence specialists and strategy consultants across finance, retail, healthcare and tech industries.",
    "Business Artificial Intelligence Systems": "Based on your responses, you are someone who wants AI to solve real business problems, not just theoretical ones. You are excited by how machine learning and intelligent systems can transform how companies operate, compete and serve customers. Your combination of business acumen, interest in AI applications and systems thinking makes Business AI Systems a natural fit. Graduates work at the frontier of AI adoption in enterprises, consulting firms, fintech companies and digital transformation roles."
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
        "text": "Which school subject combination appeals to you most?",
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
            "C": ("Train a machine learning model to predict customer behaviour", {"Artificial Intelligence": 1, "Business Analytics": 2, "Business Artificial Intelligence Systems": 1}),
            "D": ("Find and fix vulnerabilities in a company's entire digital infrastructure", {"Information Security": 2}),
            "E": ("Build an AI system that automates a real business process", {"Artificial Intelligence": 1, "Business Artificial Intelligence Systems": 2})
        }
    },
    {
        "id": "COMP_Q4",
        "text": "How do you feel about the business side of technology?",
        "options": {
            "A": ("Not very interested — I prefer pure technical depth over business applications", {"Computer Science": 2, "Computer Engineering": 1, "Information Security": 1}),
            "B": ("Somewhat interested — I like tech but also want to understand its real-world impact", {"Artificial Intelligence": 1, "Computer Science": 1}),
            "C": ("Very interested — I want to use technology to directly drive business outcomes", {"Business Analytics": 2, "Business Artificial Intelligence Systems": 2}),
            "D": ("I want to bridge both worlds equally", {"Business Artificial Intelligence Systems": 2, "Business Analytics": 1})
        }
    },
    {
        "id": "COMP_Q5",
        "text": "Which career environment sounds most exciting to you?",
        "options": {
            "A": ("A top tech company (Google, Meta, ByteDance) as a software engineer", {"Computer Science": 2, "Artificial Intelligence": 1}),
            "B": ("A semiconductor or hardware company designing next-generation chips", {"Computer Engineering": 2}),
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
        "text": "How important is it to you that your work has a direct business or commercial impact?",
        "options": {
            "A": ("Not important — I care about technical excellence and innovation above all", {"Computer Science": 2, "Computer Engineering": 1}),
            "B": ("Somewhat important — I want my work to matter but I'm drawn to deep technical problems", {"Artificial Intelligence": 2, "Information Security": 1}),
            "C": ("Very important — I want to see clear, measurable business results from my work", {"Business Analytics": 2, "Business Artificial Intelligence Systems": 2}),
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
# HELPER FUNCTIONS
# ============================================================

def check_cde_trigger(matches_df: pd.DataFrame) -> bool:
    """Check if 3+ of top 5 results are CDE programmes"""
    top_5 = matches_df.head(5)
    cde_count = sum(
        1 for _, row in top_5.iterrows()
        if any(prog.lower() in row['Programme_Name'].lower() for prog in CDE_PROGRAMMES)
    )
    return cde_count >= 3


def check_computing_trigger(matches_df: pd.DataFrame) -> bool:
    """Check if 3+ of top 5 results are Computing programmes"""
    top_5 = matches_df.head(5)
    comp_count = sum(
        1 for _, row in top_5.iterrows()
        if any(prog.lower() in row['Programme_Name'].lower() for prog in COMPUTING_PROGRAMMES)
    )
    return comp_count >= 3


def calculate_cluster_scores(responses: Dict[str, str], questions: list, programmes: list) -> str:
    """Generic function to calculate best-fit programme from drill-down responses"""
    programme_scores = {prog: 0 for prog in programmes}

    for q_id, chosen_option in responses.items():
        question = next((q for q in questions if q['id'] == q_id), None)
        if question and chosen_option in question['options']:
            _, score_dict = question['options'][chosen_option]
            for prog, points in score_dict.items():
                if prog in programme_scores:
                    programme_scores[prog] += points

    best_fit = max(programme_scores, key=programme_scores.get)
    return best_fit


# ============================================================
# SESSION STATE
# ============================================================

def init_session_state():
    """Initialize session state variables"""
    defaults = {
        'page': 'welcome',
        'responses': {},
        'current_question': 0,
        'results': None,
        # CDE drill-down
        'cde_responses': {},
        'cde_result': None,
        'cde_question_index': 0,
        # Computing drill-down
        'comp_responses': {},
        'comp_result': None,
        'comp_question_index': 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ============================================================
# SCORING ALGORITHM
# ============================================================

def calculate_riasec_scores(responses: Dict[str, int], questions_df: pd.DataFrame) -> Dict[str, float]:
    """Calculate RIASEC scores from questionnaire responses"""
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
    """Get top N RIASEC codes sorted by score"""
    sorted_codes = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)
    return [code for code, score in sorted_codes[:n]]


def get_top_values(responses: Dict[str, int], n: int = 3) -> List[str]:
    """Extract top values from questions Q25-Q29"""
    value_mapping = {
        'Q25': 'high-salary',
        'Q26': 'helping-people',
        'Q27': 'creativity',
        'Q28': 'technology',
        'Q29': 'work-life-balance'
    }
    value_responses = {}
    for q_id, label in value_mapping.items():
        if q_id in responses:
            value_responses[label] = responses[q_id]

    sorted_values = sorted(value_responses.items(), key=lambda x: x[1], reverse=True)
    return [value for value, score in sorted_values[:n]]


def match_programmes(riasec_scores: Dict[str, float], top_values: List[str],
                     programmes_df: pd.DataFrame, top_n: int = 8) -> pd.DataFrame:
    """
    IMPROVED matching algorithm using score magnitude for better differentiation.

    Scoring:
    - 1st RIASEC × (score/100) matches Primary:   up to 5 pts
    - 1st RIASEC × (score/100) matches Secondary: up to 3 pts
    - 2nd RIASEC × (score/100) matches Primary:   up to 3 pts
    - 2nd RIASEC × (score/100) matches Secondary: up to 2 pts
    - 3rd RIASEC matches Primary:                 up to 1 pt
    - Perfect top-2 alignment bonus:              +2 pts
    - Values match (only if rated 4-5):           +2 pts per match
    - Mismatch penalty (top type absent from programme): -1 pt
    """
    top_riasec = get_top_riasec(riasec_scores, n=3)

    scores = []
    for idx, row in programmes_df.iterrows():
        score = 0
        match_details = []

        prog_primary = row['Primary_RIASEC']
        prog_secondary = row['Secondary_RIASEC']
        prog_tertiary = row['Tertiary_RIASEC'] if pd.notna(row['Tertiary_RIASEC']) else None
        prog_codes = [c for c in [prog_primary, prog_secondary, prog_tertiary] if c]

        # --- RIASEC matching weighted by actual score magnitude ---
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

        if len(top_riasec) > 2:
            if top_riasec[2] == prog_primary:
                score += 1
                match_details.append(f"Your 3rd interest ({RIASEC_NAMES[top_riasec[2]]}) matches the programme focus (+1.0)")

        # --- Perfect top-2 bonus ---
        prog_top2 = [prog_primary, prog_secondary]
        if len(top_riasec) >= 2 and top_riasec[0] in prog_top2 and top_riasec[1] in prog_top2:
            score += 2
            match_details.append("Strong alignment: Your top 2 interests match this programme's core profile (+2.0)")

        # --- Mismatch penalty ---
        if top_riasec[0] not in prog_codes:
            score -= 1
            match_details.append(f"Your top interest ({RIASEC_NAMES[top_riasec[0]]}) is not a focus of this programme (-1.0)")

        # --- Values matching (only high ratings count) ---
        if pd.notna(row['Value_Tags']):
            prog_values = [v.strip() for v in str(row['Value_Tags']).split(',')]
            value_matches = []
            for val in top_values:
                val_score = st.session_state.responses.get(
                    [k for k, v in {'Q25': 'high-salary', 'Q26': 'helping-people',
                                    'Q27': 'creativity', 'Q28': 'technology',
                                    'Q29': 'work-life-balance'}.items() if v == val][0], 0
                )
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

        # Developer test mode
        with st.expander("🛠️ Developer Test Mode"):
            st.warning("⚠️ For testing only — skips the 29 questions with preset answers.")
            selected_profile = st.selectbox("Select a test profile:", list(TEST_PROFILES.keys()))
            if st.button("⚡ Load Test Profile & See Results", use_container_width=True):
                st.session_state.responses = TEST_PROFILES[selected_profile].copy()
                st.session_state.current_question = len(TEST_PROFILES[selected_profile])
                st.session_state.page = 'results'
                st.rerun()

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


# ============================================================
# PAGE: QUESTIONNAIRE
# ============================================================

def show_questionnaire_page(questions_df):
    """Display questionnaire page"""
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

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

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


# ============================================================
# PAGE: RESULTS
# ============================================================

def show_results_page(questions_df, programmes_df, riasec_desc_df):
    """Display results page"""
    st.markdown('<div class="main-header">🎯 Your Results</div>', unsafe_allow_html=True)

    riasec_scores = calculate_riasec_scores(st.session_state.responses, questions_df)
    top_riasec = get_top_riasec(riasec_scores, n=3)
    top_values = get_top_values(st.session_state.responses, n=3)
    matches = match_programmes(riasec_scores, top_values, programmes_df, top_n=8)

    st.markdown("## 📊 Your RIASEC Profile")
    col1, col2 = st.columns([1, 1])

    with col1:
        categories = list(RIASEC_NAMES.values())
        scores = [riasec_scores[code] for code in RIASEC_NAMES.keys()]
        fig = go.Figure(data=go.Scatterpolar(
            r=scores, theta=categories, fill='toself',
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
            name = RIASEC_NAMES[code]
            score = riasec_scores[code]
            desc = riasec_desc_df[riasec_desc_df['Code'] == code].iloc[0]['Description']
            st.markdown(f"**{i}. {name} ({code}) - {score:.1f}%**  \n{desc}")

        st.markdown("### Your Top Values:")
        for i, value in enumerate(top_values, 1):
            st.markdown(f"{i}. {value.replace('-', ' ').title()}")

    st.markdown("---")
    st.markdown("## 🎓 Your Top Programme Matches")
    st.markdown("*These programmes best align with your interests and values*")

    for rank, (idx, row) in enumerate(matches.iterrows(), 1):
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
                {f'<span class="riasec-badge">{row["Tertiary_RIASEC"]} - {RIASEC_NAMES[row["Tertiary_RIASEC"]]}</span>' if pd.notna(row['Tertiary_RIASEC']) else ''}
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📋 Why this match?"):
            for detail in row['Match_Details']:
                st.markdown(f"- {detail}")
            st.markdown(f"\n**Programme Values:** {row['Value_Tags']}")

    st.markdown("---")

    # --- CDE drill-down trigger ---
    cde_triggered = check_cde_trigger(matches)
    comp_triggered = check_computing_trigger(matches)

    if cde_triggered or comp_triggered:
        st.markdown("### 🔍 Want to go deeper?")

    if cde_triggered:
        st.info("**3 or more of your top matches are CDE programmes!** Answer 10 more questions to find your single best-fit CDE programme.")
        if st.button("🔍 Explore CDE Programmes Further", type="primary", use_container_width=True):
            st.session_state.cde_responses = {}
            st.session_state.cde_question_index = 0
            st.session_state.page = 'cde_drilldown'
            st.rerun()

    if comp_triggered:
        st.info("**3 or more of your top matches are Computing programmes!** Answer 10 more questions to find your single best-fit Computing programme.")
        if st.button("💻 Explore Computing Programmes Further", type="primary", use_container_width=True):
            st.session_state.comp_responses = {}
            st.session_state.comp_question_index = 0
            st.session_state.page = 'comp_drilldown'
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

YOUR TOP VALUES:
{', '.join([v.replace('-', ' ').title() for v in top_values])}

YOUR TOP PROGRAMME MATCHES:
"""
        for rank, (idx, row) in enumerate(matches.iterrows(), 1):
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
            - RIASEC scores are weighted by how strongly you scored in each type
            - Primary matches score higher than secondary matches
            - A small penalty applies when your top interest is absent from a programme
            - Values only boost score if you rated them 4 or 5 (important to you)
            - Perfect top-2 alignment gives a bonus

            **Next steps:**
            - Research your top matches on the NUS website
            - Talk to current students in these programmes
            - Consider your academic strengths and interests
            - Apply to programmes that excite you!
            """)


# ============================================================
# PAGE: CDE DRILL-DOWN
# ============================================================

def show_drilldown_page(cluster_name, questions, session_index_key, session_responses_key, result_page_key):
    """Generic drill-down questionnaire page for any cluster"""
    st.markdown(f'<div class="main-header">🔍 {cluster_name} Explorer</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">Let\'s find your best-fit {cluster_name} programme</div>', unsafe_allow_html=True)

    total = len(questions)
    current = st.session_state[session_index_key]
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

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        if current > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state[session_index_key] -= 1
                st.rerun()

    with col2:
        if current < total - 1:
            if st.button("Next ➡️", type="primary", use_container_width=True, disabled=(response is None)):
                if response is not None:
                    st.session_state[session_responses_key][q_id] = response
                    st.session_state[session_index_key] += 1
                    st.rerun()
        else:
            if st.button("✅ See My Best-Fit Programme", type="primary", use_container_width=True, disabled=(response is None)):
                if response is not None:
                    st.session_state[session_responses_key][q_id] = response
                    st.session_state.page = result_page_key
                    st.rerun()


def show_drilldown_result_page(cluster_name, result_key, identity_statements, questions, programmes, responses_key, index_key, drilldown_page_key):
    """Generic drill-down result page for any cluster"""
    st.markdown(f'<div class="main-header">🎯 Your Best-Fit {cluster_name} Programme</div>', unsafe_allow_html=True)

    best_fit = calculate_cluster_scores(st.session_state[responses_key], questions, programmes)
    st.session_state[result_key] = best_fit

    statement = identity_statements.get(best_fit, "This programme is a strong fit based on your responses.")

    st.markdown(f"""
    <div class="recommendation-card">
        <h2>🏆 {best_fit}</h2>
        <p style="font-size: 1.1rem; line-height: 1.8;">{statement}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔗 What's Next?")
    st.markdown(f"""
    - 🌐 [Explore {best_fit} on NUS website](https://www.nus.edu.sg/admissions/undergraduate/programmes.html)
    - 💬 Talk to current {best_fit} students
    - 📋 Review your Stage 1 results to see the bigger picture
    """)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back to My Programme Matches", use_container_width=True):
            st.session_state.page = 'results'
            st.rerun()

    with col2:
        if st.button(f"🔄 Retake {cluster_name} Explorer", use_container_width=True):
            st.session_state[responses_key] = {}
            st.session_state[result_key] = None
            st.session_state[index_key] = 0
            st.session_state.page = drilldown_page_key
            st.rerun()


# ============================================================
# MAIN
# ============================================================

def main():
    """Main application logic"""
    init_session_state()
    questions_df, programmes_df, values_df, riasec_desc_df = load_data()

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
        Version 2.0

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

    # Page routing
    if st.session_state.page == 'welcome':
        show_welcome_page()

    elif st.session_state.page == 'questionnaire':
        show_questionnaire_page(questions_df)

    elif st.session_state.page == 'results':
        show_results_page(questions_df, programmes_df, riasec_desc_df)

    elif st.session_state.page == 'cde_drilldown':
        show_drilldown_page(
            cluster_name="CDE",
            questions=CDE_DRILL_DOWN_QUESTIONS,
            session_index_key='cde_question_index',
            session_responses_key='cde_responses',
            result_page_key='cde_result'
        )

    elif st.session_state.page == 'cde_result':
        show_drilldown_result_page(
            cluster_name="CDE",
            result_key='cde_result',
            identity_statements=CDE_IDENTITY_STATEMENTS,
            questions=CDE_DRILL_DOWN_QUESTIONS,
            programmes=CDE_PROGRAMMES,
            responses_key='cde_responses',
            index_key='cde_question_index',
            drilldown_page_key='cde_drilldown'
        )

    elif st.session_state.page == 'comp_drilldown':
        show_drilldown_page(
            cluster_name="Computing",
            questions=COMPUTING_DRILL_DOWN_QUESTIONS,
            session_index_key='comp_question_index',
            session_responses_key='comp_responses',
            result_page_key='comp_result'
        )

    elif st.session_state.page == 'comp_result':
        show_drilldown_result_page(
            cluster_name="Computing",
            result_key='comp_result',
            identity_statements=COMPUTING_IDENTITY_STATEMENTS,
            questions=COMPUTING_DRILL_DOWN_QUESTIONS,
            programmes=COMPUTING_PROGRAMMES,
            responses_key='comp_responses',
            index_key='comp_question_index',
            drilldown_page_key='comp_drilldown'
        )


if __name__ == "__main__":
    main()