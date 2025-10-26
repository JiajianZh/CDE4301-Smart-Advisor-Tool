import streamlit as st
import pandas as pd
import math
from collections import defaultdict

st.set_page_config(page_title="Identity-Based Major Advisor", page_icon="🎓", layout="centered")
st.title("Identity-Based Major Advisor")
st.write("Answer a few quick questions. We’ll infer your work-mode profile and suggest programs (incl. NUS).")

# -------- Cached data loader (faster reloads) --------
@st.cache_data(ttl=3600, show_spinner=False)  # cache CSV for 1 hour
def load_programs():
    return pd.read_csv("data/programs.csv")

# -------- Config --------
WORK_MODES = ["builder","analyst","people","creative","researcher","operator","systems"]

QUESTIONS = [
    ("You’d rather…", ["Fix a machine","Interview users"]),
    ("You enjoy…", ["Data deep dives","Visual design sprints"]),
    ("You value more…", ["Real-world impact now","Research depth"]),
    ("You prefer…", ["Structured checklists","Open-ended exploration"]),
    ("Club website scenario: you would…", ["Code backend","Run user tests","Project manage","Design UI","Analyze traffic"]),
    ("You like systems that are…", ["Physical & tangible","Digital & informational"]),
    ("Pick up to two interests", ["manufacturing","energy","health","software","finance","climate","transport","design","analytics","operations"]),
    ("Preferred study style", ["lab","studio","theory","project"])
]

# Each option adds weights to work modes
MODE_MAP = {
    "Fix a machine":{"builder":2,"systems":1},
    "Interview users":{"people":2,"creative":1},
    "Data deep dives":{"analyst":2,"systems":1},
    "Visual design sprints":{"creative":2,"people":1},
    "Real-world impact now":{"operator":2,"builder":1},
    "Research depth":{"researcher":2,"analyst":1},
    "Structured checklists":{"operator":2,"systems":1},
    "Open-ended exploration":{"creative":2,"researcher":1},
    "Code backend":{"analyst":2,"systems":1},
    "Run user tests":{"people":2,"analyst":1},
    "Project manage":{"operator":2,"people":1},
    "Design UI":{"creative":2,"people":1},
    "Analyze traffic":{"analyst":2,"systems":1},
    "Physical & tangible":{"builder":2,"systems":1},
    "Digital & informational":{"analyst":2,"researcher":1},
}

def cosine(a: dict, b: dict) -> float:
    # a and b are dicts with keys = WORK_MODES and values = floats
    dot = sum(a.get(k,0)*b.get(k,0) for k in WORK_MODES)
    na = math.sqrt(sum((a.get(k,0))**2 for k in WORK_MODES))
    nb = math.sqrt(sum((b.get(k,0))**2 for k in WORK_MODES))
    return 0.0 if na == 0 or nb == 0 else dot / (na * nb)

# -------- UI --------
with st.form("quiz"):
    ans = {}
    ans["q1"] = st.radio(*QUESTIONS[0], index=None)
    ans["q2"] = st.radio(*QUESTIONS[1], index=None)
    ans["q3"] = st.radio(*QUESTIONS[2], index=None)
    ans["q4"] = st.radio(*QUESTIONS[3], index=None)
    ans["q5"] = st.radio(*QUESTIONS[4], index=None)
    ans["q6"] = st.radio(*QUESTIONS[5], index=None)
    ans["interests"] = st.multiselect(QUESTIONS[6][0], QUESTIONS[6][1], max_selections=2)
    ans["style"] = st.radio(*QUESTIONS[7], index=None)
    go = st.form_submit_button("See my matches")

if go and None not in [ans["q1"],ans["q2"],ans["q3"],ans["q4"],ans["q5"],ans["q6"],ans["style"]] and len(ans["interests"])>0:
    # Build user vectors
    mode_vec = defaultdict(int)
    for key in ["q1","q2","q3","q4","q5","q6"]:
        for k,v in MODE_MAP.get(ans[key], {}).items():
            mode_vec[k] += v
    max_possible = 2*6  # 6 mode-questions × max 2 points each
    user_mode = {m: (mode_vec[m]/max_possible) for m in WORK_MODES}
    user_interests = {x.strip().lower() for x in ans["interests"]}
    user_style = ans["style"].strip().lower()

    # Load programs (cached)
    df = load_programs()

    def row_mode_vec(row):
        mv = defaultdict(int)
        for t in str(row.get("tags_work_modes","")).split(","):
            t=t.strip().lower()
            if t in WORK_MODES:
                mv[t] += 1
        total = sum(mv.values())
        return {m: (mv[m]/total if total else 0.0) for m in WORK_MODES}

    def interest_overlap(row):
        tags = {x.strip().lower() for x in str(row.get("tags_interests","")).split(",") if x.strip()}
        return len(user_interests & tags) / max(1, len(user_interests))

    def style_fit(row):
        styles = {x.strip().lower() for x in str(row.get("study_style","")).split(",") if x.strip()}
        return 1.0 if user_style in styles else 0.0

    # Score programs
    scored = []
    for _,r in df.iterrows():
        pmode = row_mode_vec(r)
        mode_fit = cosine(user_mode, pmode)         # 0..1
        i_fit = interest_overlap(r)                  # 0..1
        s_fit = style_fit(r)                         # 0 or 1
        final = 70*mode_fit + 20*i_fit + 10*s_fit   # 0..100
        scored.append((final, mode_fit, i_fit, s_fit, r))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:6]

    # Display
    top_modes = sorted(user_mode.items(), key=lambda x: x[1], reverse=True)[:3]
    st.subheader("Your identity snapshot")
    st.write("You lean towards: " + ", ".join([f"{m} {round(v*100)}%" for m,v in top_modes]) + ".")

    st.subheader("Suggested programs")
    for score, mfit, ifit, sfit, r in top:
        why = f"mode fit {round(mfit*100)}%, interests {round(ifit*100)}%, study style {'✓' if sfit==1 else '—'}"
        link = str(r.get("link",""))
        name = str(r.get("program_name","Program"))
        inst = str(r.get("institution",""))
        country = str(r.get("country",""))
        level = str(r.get("level",""))
        line = f"- {name} — {inst} ({country}) · {level}  \n  why: {why}"
        if link.startswith("http"):
            st.markdown(f"- [{name}]({link}) — {inst} ({country}) · {level}  \n  why: {why}")
        else:
            st.markdown(line)

    nus = [x for x in top if "nus" in str(x[4].get("institution","")).lower()]
    if nus:
        st.subheader("NUS matches")
        for score, mfit, ifit, sfit, r in nus:
            st.markdown(f"- {r.get('program_name','')} • modules: {r.get('example_modules','')} • roles: {r.get('example_roles','')}")

    # Downloadable mini report
    report = "Identity snapshot: " + ", ".join([f"{m} {round(v*100)}%" for m,v in top_modes]) + "\n\n"
    report += "Top suggestions:\n" + "\n".join([f"- {x[4].get('program_name','')} — {x[4].get('institution','')} ({x[4].get('country','')})" for x in top])
    st.download_button("Download my mini report", report, file_name="identity_major_report.txt")

    # Quick restart button
    if st.button("Start over"):
        st.rerun()
else:
    st.info("Answer all fields to see results.")
