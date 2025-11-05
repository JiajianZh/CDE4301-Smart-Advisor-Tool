import os
import math
from collections import defaultdict

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Identity-Based Major Advisor", page_icon="🎓", layout="centered")
st.title("Identity-Based Major Advisor")
st.write("Answer a few quick questions. We’ll infer your work-mode profile and suggest NUS programmes.")

# ---- Data loader (expects: id, program_name, institution, tags_work_modes) ----
@st.cache_data(ttl=3600, show_spinner=False)
def load_programs():
    return pd.read_csv("data/programs.csv")

# ---- Config ----
WORK_MODES = ["builder","analyst","people","creative","researcher","operator","systems"]

QUESTIONS = [
    # Q1: weekend build-a-thon roles
    ("Your team signs up for a weekend build-a-thon. Which roles do you actually want to take on?",
     ["Prototype hardware", "Design screens/UX", "Interview potential users", "Build the data pipeline", "Coordinate tasks & timeline", "None of these"]),
    # Q2: club website scenario
    ("Club website scenario: hands on deck—what would you pick up first?",
     ["Code backend", "Run user tests", "Project manage", "Design UI", "Analyze traffic", "None of these"]),
    # Q3: capstone project style
    ("For your capstone, which project style sounds most you?",
     ["Lab experiments with equipment", "Fieldwork with stakeholders", "Theoretical modelling & proofs", "Business case with ops plan", "System integration across tools", "None of these"]),
    # Q4: how you organise work
    ("When you organise work, which approach feels natural?",
     ["Checklists & SOPs", "Explore ideas then refine", "Analyse datasets for insight", "Design the overall architecture", "None of these"]),
    # Q5: what energises you
    ("In a long project, what consistently energises you?",
     ["Hands-on building and testing", "Making things clearer for people", "Finding patterns in messy data", "Crafting visuals & interactions", "None of these"]),
    # Q6: when things break
    ("When something breaks, which troubleshooting path do you instinctively start with?",
     ["Debug circuitry/mechanics", "Trace code/data flows", "Talk to users to understand context", "Re-organise process/workflow", "None of these"]),
]


MODE_MAP = {
    # Q1 build-a-thon
    "Prototype hardware": {"builder": 2, "systems": 1},
    "Design screens/UX": {"creative": 2, "people": 1},
    "Interview potential users": {"people": 2, "analyst": 1},
    "Build the data pipeline": {"analyst": 2, "systems": 1},
    "Coordinate tasks & timeline": {"operator": 2, "people": 1},
    # Q2 club website
    "Code backend": {"analyst": 2, "systems": 1},
    "Run user tests": {"people": 2, "analyst": 1},
    "Project manage": {"operator": 2, "people": 1},
    "Design UI": {"creative": 2, "people": 1},
    "Analyze traffic": {"analyst": 2, "systems": 1},
    # Q3 capstone style
    "Lab experiments with equipment": {"builder": 2, "researcher": 1},
    "Fieldwork with stakeholders": {"people": 2, "operator": 1},
    "Theoretical modelling & proofs": {"researcher": 2, "analyst": 1},
    "Business case with ops plan": {"operator": 2, "analyst": 1},
    "System integration across tools": {"systems": 2, "builder": 1},
    # Q4 organise work
    "Checklists & SOPs": {"operator": 2, "systems": 1},
    "Explore ideas then refine": {"creative": 2, "researcher": 1},
    "Analyse datasets for insight": {"analyst": 2, "systems": 1},
    "Design the overall architecture": {"systems": 2, "analyst": 1},
    # Q5 energisers
    "Hands-on building and testing": {"builder": 2, "systems": 1},
    "Making things clearer for people": {"people": 2, "operator": 1},
    "Finding patterns in messy data": {"analyst": 2, "researcher": 1},
    "Crafting visuals & interactions": {"creative": 2, "people": 1},
    # Q6 when things break
    "Debug circuitry/mechanics": {"builder": 2, "systems": 1},
    "Trace code/data flows": {"analyst": 2, "systems": 1},
    "Talk to users to understand context": {"people": 2, "analyst": 1},
    "Re-organise process/workflow": {"operator": 2, "systems": 1},
}
IGNORES = {"None of these"}  # selected options that add no weight


# Lightweight keyword mapping for the open-ended box (no API needed)
TEXT_KEYWORDS = {
    "builder": ["prototype","hardware","tooling","fabrication","manufactur","mech","hands-on","lab","robot","cad","solidworks","autocad","arduino"],
    "analyst": ["data","model","analysis","statistics","analytics","excel","sql","python"," r ","matlab","forecast","optimi","quant"],
    "people": ["interview","users","stakeholder","team","client","community","lead","mentor","volunteer","club"],
    "creative": ["design","ui","ux","sketch","figma","aesthet","visual","brand","story","media"],
    "researcher": ["paper","research","experiment","hypothesis","literature","study","theory","journal","simulation"],
    "operator": ["process","ops","operations","sop","checklist","maintenance","logistics","supply","safety","compliance"],
    "systems": ["system","architecture","workflow","pipeline","integration","platform","network","infrastructure"],
}

def extract_modes_from_text(text: str) -> dict:
    vec = defaultdict(int)
    t = (text or "").lower()
    for mode, kws in TEXT_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                vec[mode] += 1
    hits = sum(vec.values())
    if hits == 0:
        return {m: 0 for m in WORK_MODES}
    scale = 6  # about one MCQ worth of influence
    return {m: (vec[m] / hits) * scale for m in WORK_MODES}

def cosine(a: dict, b: dict) -> float:
    dot = sum(a.get(k,0)*b.get(k,0) for k in WORK_MODES)
    na = math.sqrt(sum((a.get(k,0))**2 for k in WORK_MODES))
    nb = math.sqrt(sum((b.get(k,0))**2 for k in WORK_MODES))
    return 0.0 if na == 0 or nb == 0 else dot / (na * nb)

# Optional AI explanation (only if key is present; matching does NOT use LLM)
def llm_explain(identity_text: str, top_rows: list[dict]) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        bullets = "\n".join([f"- {r['program_name']} — {r['institution']} (modes: {r['tags_work_modes']})" for r in top_rows])
        system = "You are an academic advising assistant. Be concise, plain-English, and use only provided facts."
        user = f"""
Identity snapshot:
{identity_text}

Programmes:
{bullets}

Write 3–5 sentences summarising why these fit, referencing the modes shown.
"""
        resp = client.chat.completions.create(
            model="gpt-4o-mini", temperature=0.2,
            messages=[{"role":"system","content":system},{"role":"user","content":user}],
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        st.caption(f"(AI explanation unavailable: {e})")
        return None

# ---- UI ----
with st.form("quiz"):
    ans = {}
    # multiselect (max 2) for each scenario question
    for i, (prompt, choices) in enumerate(QUESTIONS, start=1):
        ans[f"q{i}"] = st.multiselect(prompt, choices, max_selections=2, key=f"q{i}")
    about = st.text_area(
        "Optional: tell us about yourself (projects/modules you liked, CCAs, goals)",
        placeholder="e.g., built a robot arm; enjoy Python data work; led a design club"
    )
    go = st.form_submit_button("See my matches")

if go:
    # ensure each question has at least one selection (or 'None of these')
    if any(len(ans[f"q{i}"]) == 0 for i in range(1, len(QUESTIONS)+1)):
        st.info("Make a selection for each question (you can choose up to two, or 'None of these').")
    else:
        mode_vec = defaultdict(int)

        # accumulate weights from all selected options
        for i in range(1, len(QUESTIONS)+1):
            for choice in ans[f"q{i}"]:
                if choice in IGNORES:
                    continue
                for k, v in MODE_MAP.get(choice, {}).items():
                    mode_vec[k] += v

        # add open-text influence (same function as before)
        text_vec = extract_modes_from_text(about)
        for m in WORK_MODES:
            mode_vec[m] += text_vec.get(m, 0)

        # normalise: each question can contribute up to 2 options (each roughly weight ~2)
        # 6 questions * 2 options * 2 points = 24, plus text scale (~6)
        max_possible = 24 + 6
        user_mode = {m: (mode_vec[m]/max_possible) for m in WORK_MODES}

        # ... keep the rest of your scoring/display code unchanged ...


    # Load programmes and score
    df = load_programs()

    def row_mode_vec(row):
        mv = defaultdict(int)
        for t in str(row.get("tags_work_modes","")).split(","):
            t=t.strip().lower()
            if t in WORK_MODES:
                mv[t] += 1
        total = sum(mv.values())
        return {m: (mv[m]/total if total else 0.0) for m in WORK_MODES}

    scored = []
    for _, r in df.iterrows():
        pmode = row_mode_vec(r)
        mode_fit = cosine(user_mode, pmode)   # 0..1
        scored.append((100*mode_fit, mode_fit, r))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:6]

    # Identity snapshot
    top_modes = sorted(user_mode.items(), key=lambda x: x[1], reverse=True)[:3]
    st.subheader("Your identity snapshot")
    st.write("You lean towards: " + ", ".join([f"{m} {round(v*100)}%" for m,v in top_modes]) + ".")

    # Suggestions
    st.subheader("Suggested programmes")
    for score, mfit, r in top:
        prog_modes = [t.strip() for t in str(r.get("tags_work_modes","")).split(",") if t.strip()]
        why = f"mode match {round(mfit*100)}% • programme modes: {', '.join(prog_modes[:3])}"
        st.markdown(f"- {r.get('program_name','Program')} — {r.get('institution','')}  \n  why: {why}")

    # Optional AI blurb
    identity_text = "Top modes: " + ", ".join([f"{m} {round(v*100)}%" for m,v in top_modes]) + ". " + (about or "")
    top_dicts = [{"program_name": str(r.get("program_name","")), "institution": str(r.get("institution","")), "tags_work_modes": str(r.get("tags_work_modes",""))} for _,_,r in top]
    llm_text = llm_explain(identity_text, top_dicts)
    if llm_text:
        st.subheader("Why these fit (AI)")
        st.write(llm_text)

    if st.button("Start over"):
        st.rerun()
else:
    st.info("Answer all MCQs to see results (the text box is optional).")
