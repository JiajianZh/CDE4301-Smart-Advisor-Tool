---
title: Smart Advisor Tool - Final Report
description: RIASEC-based programme matching tool for NUS undergraduate admissions
---

# Smart Advisor Tool - Final Report

**CDE4301 Innovation & Design Capstone**

**Student:** Zhuang Jiajian (A0255385W)  
**Programme:** Mechanical Engineering, College of Design and Engineering  
**Supervisor:** A/Prof Mark De Lessio  
**Date:** 6 April 2026

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Context and Literature Review](#2-context-and-literature-review)
3. [Methodology and Development Process](#3-methodology-and-development-process)
4. [Implementation](#4-implementation)
5. [Testing and Validation](#5-testing-and-validation)
6. [Deliverables](#6-deliverables)
7. [Discussion and Analysis](#7-discussion-and-analysis)
8. [Future Work](#8-future-work)
9. [Conclusion](#9-conclusion)
10. [References](#10-references)

---

## 1. INTRODUCTION

### 1.1 Project Overview

**Project Title:** Smart Advisor Tool  
**Student:** Zhuang Jiajian, Mechanical Engineering, College of Design and Engineering  
**Supervisor:** A/Prof Mark De Lessio

This project developed a web-based tool to help pre-university students find NUS undergraduate programmes that match their interests. The tool uses a proven research framework called RIASEC to measure what students enjoy doing. It then recommends programmes based on these interests plus the student's personal values.

The tool covers all 75 undergraduate programmes at NUS. Students answer 29 questions in about 3 minutes. They get a personalized profile and a ranked list of programmes that fit them best. If their results cluster around one faculty, they can answer 10 more questions to find their single best-fit programme within that faculty.

**Live deployment:** [https://cde4301-smart-advisor-tool-8pq7cdqe3uubafqgwu5awg.streamlit.app/](https://cde4301-smart-advisor-tool-8pq7cdqe3uubafqgwu5awg.streamlit.app/)

### 1.2 Problem Statement

Many students struggle to choose what to study at university. Global studies show that about 40% of students are uncertain about their future careers. In Singapore, 25% of junior college and polytechnic students regret their education pathway choice. About 50% of individuals aged 21-34 feel uncertain about their future in the workforce.

When students pick the wrong programme, several problems occur. Their grades may suffer. They may switch majors, which delays graduation and costs more money. Some drop out entirely. This affects their confidence and wellbeing.

Students need better tools to make these decisions. Current tools focus on career planning for people who already know what job they want. But many pre-university students have not reached that stage yet. They need tools that help them understand themselves first.

### 1.3 Project Objectives

This project set out to build and deploy a smart advisory tool with specific goals:

**Primary objective:** Create a matching system that covers all 75 NUS undergraduate programmes.

**Deliverable:** A web application where students can:

1. Complete a 29-question survey
2. See their RIASEC profile (their interest type)
3. Get a ranked list of programme matches with explanations
4. Explore deeper with faculty-specific questions if needed

**Target users:** Pre-university students in Singapore who are exploring NUS programme options before applying to university.

---

## 2. CONTEXT AND LITERATURE REVIEW

### 2.1 The RIASEC Framework

This tool uses Holland's RIASEC theory. RIASEC classifies both people and work environments into six types:

- **R (Realistic):** Hands-on, practical, mechanical work
- **I (Investigative):** Analytical, research, problem-solving
- **A (Artistic):** Creative, expressive, design
- **S (Social):** Helping people, teaching, understanding behavior
- **E (Enterprising):** Leading, persuading, business
- **C (Conventional):** Organizing, data, systematic procedures

Research shows that people are happier and more successful in environments matching their type. A large ACT study of 80,000+ college students found that interest-major fit predicted GPA better than test scores. Students matching their programme to their interests also persist longer and graduate on time.

The tool's questions were adapted from the O*NET Interest Profiler. This is a validated, public-domain assessment developed by the U.S. Department of Labor. It has been tested with thousands of users and shows strong reliability and validity.

**What are values?** In career guidance, values refer to what people consider important in their work and life. These are the rewards, conditions, or outcomes that make a career satisfying. Examples include earning high income, helping others, having creative freedom, working with technology, or maintaining work-life balance. Values are different from interests. Interests tell us what activities we enjoy, while values tell us what we want to achieve or experience through our career.

**The role of values:** Interests tell us what activities people enjoy. Values tell us what people care about in a career (salary, social impact, creativity, etc.). Research shows values alignment also predicts satisfaction. When RIASEC codes are similar across programmes (many engineering programmes are R-I), values help break ties.

### 2.2 Gap Analysis and Needs Validation

Several career guidance platforms exist globally. Pathful and Xello offer RIASEC assessments and match students to career clusters. Oxford University's Career Weaver prompts students to consider interests, values, and work style. But these tools focus on careers, not academic programmes.

In Singapore, NUS Career+ helps current students with career direction. MySkillsFuture offers career exploration tools. But no tool provides RIASEC-based matching specifically for NUS undergraduate programmes. No tool targets pre-university students in the exploration stage. This project fills that gap.

A needs validation survey was designed and distributed privately to friends, who shared it within their networks using snowball sampling. The survey reached 48 pre-university student respondents. Of these, 23 students (47.9%) reported being uncertain about their desired university programme. This uncertainty rate closely aligns with the global finding that approximately 40% of students are uncertain about their future careers, confirming that the problem this tool addresses is real and significant. However, the small sample size limits the generalizability of these findings.

---

## 3. METHODOLOGY AND DEVELOPMENT PROCESS

### 3.1 Question Development

The questionnaire has 29 questions total:

- **24 RIASEC questions** (4 questions per type)
- **5 values questions**

All questions use a 5-point scale (Strongly Disagree to Strongly Agree).

**Development process:**

**Step 1:** I reviewed the O*NET Interest Profiler database. It contains over 60 validated interest questions. I selected questions that used clear language, described concrete activities, and avoided cultural bias.

**Step 2:** I adapted selected questions for Singapore context. For example, O*NET asks about "operating farm equipment." I changed this to "operating technical systems or machinery" because few Singapore students have farm experience.

**Step 3:** I used LLM tools to help refine question wording. I asked the AI tools to simplify technical jargon and ensure clarity for 17-year-old students.

**Step 4:** Five volunteers pilot-tested the questions. They flagged confusing wording. I revised based on feedback. For example, "utilizing analytical methodologies" became "analyzing problems using logic and data."

**Step 5:** I selected the final 24 items (4 per RIASEC type). Selection criteria were clarity, relevance to Singapore students, and discrimination (students gave different answers).

The 5 values questions were custom-designed. They target values most relevant to programme choice:

- V1: High income and financial security
- V2: Helping people and social impact
- V3: Creative freedom and innovation
- V4: Working with cutting-edge technology
- V5: Work-life balance and personal time

### 3.2 Programme Coding Process

All 75 NUS undergraduate programmes needed RIASEC codes. This was a major undertaking.

**Data sources:**

- NUS Undergraduate Admissions website
- Individual programme websites (curriculum details)
- Programme brochures and faculty descriptions
- Course catalogs showing required modules

**Coding schema:**  
Each programme received:

- **Primary RIASEC code** (mandatory): The dominant activity type
- **Secondary RIASEC code** (mandatory): A significant component (20-40%)
- **Tertiary RIASEC code** (optional): For multifaceted programmes
- **Value tags** (3-5 per programme): Keywords like "innovation," "helping-people," "high-salary"

**My process:**

I used LLM tools like Claude and ChatGPT extensively for this coding work. For each programme:

1. I gathered curriculum information and pasted it into Claude
2. I asked Claude to suggest RIASEC codes based on the programme's activities
3. Claude provided initial coding with explanations
4. I reviewed the suggestions and adjusted based on my understanding
5. I shared the coding with volunteers to get their feedback on whether it made sense, and I adjusted it based on their suggestions.

For example, when coding Computer Engineering, Claude initially suggested R-I (hands-on primary). After discussion, we changed it to I-R to reflect the programme's strong focus on software alongside hardware.

I also used LLM tools to generate value tags. I would describe a programme's typical career outcomes, and LLM tools would suggest 5-7 relevant value keywords. I then selected the 3-5 most appropriate tags.

**Coverage:** The final dataset includes all 75 NUS undergraduate programmes across all faculties.

### 3.3 Matching Algorithm Development

The matching algorithm calculates a score for each programme based on how well it matches the student's profile.

**Stage 1: Global ranking**

The algorithm works like this: it looks at what the student enjoys most and compares it to what each programme focuses on.

**How scoring works:**

If the student's strongest interest matches what the programme mainly does (its Primary code), the programme gets the most points. If it matches what the programme partly does (its Secondary code), it gets fewer points. The same logic applies to the student's second-strongest interest.

I also added a small bonus when a student's top two interests perfectly match a programme's main focus areas. This rewards programmes that are a complete fit.

For values, if a student says something is important to them (rated 4 or 5) and the programme offers that (like "high-salary" or "helping-people"), the programme gets extra points.

**How I developed this:**

I experimented with different approaches. I started with simple counting (just checking if interests matched), but this did not separate programmes well enough. I then tried giving different weights to different types of matches.

I tested many combinations using developer test mode. I would load a profile, see what programmes ranked highest, and check whether it made sense. When engineering profiles ranked business programmes too high, I knew the weights needed adjustment. When all CDE programmes got identical scores, I knew I needed the drill-down system.

I used LLM tools to help write the Python code that implements the scoring. I would describe what I wanted (like "multiply the points by how strong their interest is"), and LLM tools would help translate that into working code.

The final weights are design choices based on trial and error. They reflect my understanding that what students do most in a programme (the Primary code) should matter more than secondary activities.

### 3.4 Drill-Down System Design

**The problem:** After Stage 1, results often cluster in one faculty. For example, an R-I profile might show 5 CDE programmes in the top 8. All are R-I or I-R. RIASEC alone cannot differentiate them further.

**Solution:** During project discussions, my supervisor identified this limitation and suggested a two-stage approach. When many of the top results fall in the same faculty, a second-layer questionnaire would trigger with some faculty-specific questions. I implemented this design.

**Trigger logic:** I implemented a detection system that checks the faculty of each top 8 result. If 2 or more belong to the same cluster (CDE, Computing, Business, etc.), the system offers that drill-down.

**Drill-down development process:**

I built six faculty-specific drill-downs:

1. **CDE (15 programmes, 10 questions)**
2. **Computing (6 programmes, 10 questions)**
3. **Business (9 programmes, 10 questions)**
4. **Humanities & Social Sciences (20 programmes, 10 questions)**
5. **Sciences (9 programmes, 10 questions)**
6. **Music (9 programmes, 10 questions)**

For each faculty, I followed this process:

**Step 1:** I analyzed what actually differentiates programmes within that faculty. For CDE, I identified key dimensions: math vs biology focus, physical vs digital work, design vs analysis emphasis.

**Step 2:** I used LLM tools to help draft questions targeting these dimensions. For example, I asked: "Create a multiple-choice question that helps differentiate between mechanical engineering and biomedical engineering based on their core activities."

**Step 3:** For each question, I manually mapped answer options to programmes with point values. For example:

- "Workshop or fabrication lab" → Mechanical Engineering +2, Civil Engineering +1
- "Science lab running experiments" → Biomedical Engineering +2, Chemical Engineering +2

**Step 4:** I wrote identity statements for each programme. These statements describe what kind of person thrives there. I drafted these myself, then used LLM tools to improve the writing style and flow.

**Step 5:** I tested each drill-down with developer test mode profiles to ensure it successfully differentiated programmes.

The drill-down configuration is stored in a Python dictionary structure, making it easy to add new faculties later.

This two-stage design addresses a fundamental limitation: RIASEC alone cannot differentiate programmes within faculties. The drill-down solves this systematically.

---

## 4. IMPLEMENTATION

### 4.1 Technology Choices

I built the tool using **Streamlit**, a Python framework for web applications. Streamlit was chosen because it allows rapid development using only Python code. No HTML, CSS, or JavaScript knowledge is needed. It deploys for free on Streamlit Cloud and is mobile-responsive by default.

**Key technologies:**

- **Python 3.9+** for all application logic
- **Streamlit 1.31+** for the web interface
- **Pandas** for data handling
- **Plotly** for the RIASEC radar chart
- **Excel (XLSX)** for data storage instead of a database

**Why Excel instead of a database?** With only 75 programmes and 29 questions, a database would add unnecessary complexity. Excel files can be updated by editing a spreadsheet. Anyone can see what data the tool uses. The file can be version-controlled in GitHub for transparency.

### 4.2 System Structure

The application uses a single-file architecture. All code lives in one file called app.py (approximately 1750 lines of Python code). The Excel file contains four sheets: Programmes, Questions, Values_Mapping, and RIASEC_Descriptions. This structure keeps everything in one place and is easy to understand.

**Application flow:**

Welcome Page → 29 Questions → Calculate RIASEC Profile →  
Rank All 75 Programmes → Check if 2+ Top Results Cluster →  
If YES: 10 Drill-Down Questions → Best-Fit Programme  
If NO: Show Top 8 Matches

### 4.3 Key Features

**Auto-advance questionnaire:** When a user selects an answer, the app waits 0.4 seconds then automatically moves to the next question. This creates a smooth experience without clicking "Next" buttons. I implemented this using Streamlit's session state and the time.sleep() function.

**Developer test mode:** I created six preset profiles (Engineering, Business, Humanities, Computing, Science, Music) that load instantly. This allowed me to test different scenarios in seconds instead of minutes. During development, I ran hundreds of tests using this feature.

**Drill-down system:** I implemented the trigger detection logic that checks if 2+ of the top 8 results belong to the same faculty. If triggered, it offers faculty-specific questions. Each faculty drill-down is stored in a configuration dictionary, making it easy to add new ones.

### 4.4 Deployment

**Live URL:** [https://cde4301-smart-advisor-tool-8pq7cdqe3uubafqgwu5awg.streamlit.app/](https://cde4301-smart-advisor-tool-8pq7cdqe3uubafqgwu5awg.streamlit.app/)

**GitHub:** [https://github.com/JiajianZh/CDE4301-Smart-Advisor-Tool](https://github.com/JiajianZh/CDE4301-Smart-Advisor-Tool)

The deployment process is automatic. When I push code changes to GitHub, Streamlit Cloud detects the update and rebuilds the application within 2 minutes. The new version goes live automatically. This means I can fix bugs and deploy updates quickly.

Because there is no database and hosting is free, there are no monthly costs. The only maintenance needed is updating programme data when NUS adds or removes programmes.

### 4.5 Development Iterations

The project went through three major versions:

**Version 1 (October 2025):** I built a static HTML/JavaScript prototype with 10 CDE programmes. It used basic RIASEC matching with equal weights. Problems: difficult to update data (hardcoded in JavaScript), not mobile-friendly, no public hosting option.

**Version 2 (November 2025):** I switched to Python and Streamlit. I expanded to 35 programmes (CDE, Computing, Business). I added values questions and implemented weighted scoring. I deployed to Streamlit Cloud. Problems: all CDE programmes scored similarly because they all had R-I codes. No way to differentiate within faculties.

**Version 3 (January 2026 - March 2026):** I expanded to all 75 programmes. I built six faculty-specific drill-downs with 10 questions each. I added identity statements. I created developer test mode for faster testing. I fixed several bugs including the Computer Engineering misclassification bug.

This represents approximately 7 months of iterative development.

---

## 5. TESTING AND VALIDATION

### 5.1 Testing Approach

I tested the tool using developer test mode with preset profiles. I created profiles representing common patterns: single-dominant interests (all-R, all-I, etc.), dual-dominant interests (R+I for engineering, E+C for business), and balanced profiles (equal scores across all six types).

For each profile, I checked whether the algorithm produced logical results:

- **Top results make sense**: An all-R (Realistic) profile should rank hands-on programmes like Mechanical Engineering highest, not business or arts programmes
- **Programmes with matching codes rank highest:** Computing programmes should dominate results for an I+C profile
- **Drill-down successfully differentiates within faculties:** CDE questions should separate Mechanical Engineering from Biomedical Engineering
- **Values break ties when RIASEC codes are similar:** When multiple programmes share R-I codes, values like "helping-people" should shift rankings appropriately

### 5.2 Key Test Results

Testing was conducted using the developer test mode feature, which loads preset RIASEC profiles instantly. This allowed rapid iteration through different student profile scenarios without manually completing the questionnaire each time. I will summarize three representative test cases below.

**Test Case 1: Engineering Profile (R=100%, I=75%)**

Top 5 results: Mechanical Engineering (8.1 pts), Civil Engineering (7.8 pts), Electrical Engineering (7.6 pts), Materials Science (7.3 pts), Biomedical Engineering (7.0 pts).

All top results are CDE programmes with R-I or I-R codes. The drill-down triggered (5 out of 8 results were CDE). After the drill-down, Mechanical Engineering was confirmed as best fit (92% match).

This shows the algorithm correctly identifies programmes matching the student's interests and the drill-down successfully differentiates within the faculty.

**Test Case 2: Computing Profile (I=100%, C=75%)**

Top 5 results: Computer Science (8.9 pts), Information Security (8.4 pts), Business Analytics (7.8 pts), Artificial Intelligence (7.6 pts), Data Science (7.2 pts).

The I-C profile correctly identified Computing programmes. Business Analytics and Data Science also appeared, which makes sense—both involve analytical work with data. The drill-down confirmed Computer Science as the best fit (95% match).

**Test Case 3: Balanced Profile (all RIASEC types equal at 50%)**

When RIASEC scores are balanced, values became the deciding factor. Social Work (6.8 pts) and Psychology (6.5 pts) ranked highest because they matched the student's "helping-people" value. Biomedical Engineering (6.3 pts) appeared because it matched both "helping-people" and "technology" values.

This shows the algorithm correctly shifts to values-based differentiation when interests do not provide clear direction.

**Score distribution:** Across all tests, match scores ranged from 3.0 to 12.5 points. Excellent matches scored 9.0-12.5 points. Good matches scored 6.0-9.0 points. Poor matches (below 5.0) were not shown to users. This healthy distribution shows real differentiation.

**Values contribution:** For balanced profiles, values contributed about 30% of final scores. For strong RIASEC profiles, values contributed 15-20%. This confirms the design goal: RIASEC drives most matching, with values providing meaningful personalization.

### 5.3 Bugs Found and Fixed

Testing revealed several bugs that I fixed during development:

**Bug 1: Drill-down trigger miscounting tied scores.** If two programmes had identical scores and both were in CDE, the trigger logic counted them as one programme instead of two. I fixed this by checking the Faculty column directly instead of counting unique programme names.

**Bug 2: Values scores being counted multiple times.** Some programmes with many value tags got artificially high scores. I fixed the scoring loop to count each student value only once.

**Bug 3: Computer Engineering wrongly classified.** Computer Engineering was always mapped to the CDE cluster even though it belongs to Computing faculty. I fixed this by using the Faculty column from the Excel data instead of programme name matching.

### 5.4 User Testing

Five people tested the tool informally:

- One NUS Mechanical Engineering student (Year 4)
- One NUS Computer Science master's student
- Three working professionals (finance, tech, engineering sectors)

**Tester demographics:** All five testers were adults who had completed university (one current student, four working professionals). While the target users are pre-university students, testing with people who had already experienced university allowed them to evaluate whether recommendations aligned with actual programme characteristics. My personal network primarily consists of university students and working professionals, limiting direct access to pre-university students. The needs validation survey (Section 2.2) did reach actual pre-university students.

**Positive feedback:**

- Questions were clear and easy to understand
- Completion time was good (less than 3 minutes)
- Results helped them learn about themselves
- RIASEC radar chart was visually appealing
- Match explanations were helpful

**Constructive feedback:**

- Identity statements felt a bit generic
- Some results felt obvious (engineering student got engineering programmes)
- Would be nice to save results without screenshots
- Cannot revisit results after closing browser

**Critical limitation identified:** The tool cannot store data or history. Every visit requires retaking the entire questionnaire. This is a deliberate design choice (no login, no data storage) but creates friction for users who want to revisit results or show them to others.

---

## 6. DELIVERABLES

### 6.1 Completed Deliverables

✅ **29-question questionnaire** (24 RIASEC + 5 values, average completion time 3 minutes)

✅ **All 75 NUS programmes coded** with RIASEC profiles and value tags

✅ **Two-stage matching algorithm** (global ranking + faculty-specific drill-down)

✅ **Six faculty drill-down modules** covering 68 out of 75 programmes (CDE, Computing, Business, Humanities, Sciences, Music)

✅ **Deployed web application** at [https://cde4301-smart-advisor-tool-8pq7cdqe3uubafqgwu5awg.streamlit.app/](https://cde4301-smart-advisor-tool-8pq7cdqe3uubafqgwu5awg.streamlit.app/)

- 24/7 availability
- Mobile-responsive
- No login required
- Free to use

✅ **Developer test mode** with 6 preset profiles for rapid testing

✅ **GitHub repository** with complete source code (public, version-controlled, documented)

### 6.2 Partially Completed

**Needs validation survey:** The survey was distributed to friends who shared it through their networks (snowball sampling). It reached 48 pre-university students. Of these, 23 (47.9%) reported uncertainty about programme choice. The findings align with existing research on student uncertainty despite the small sample size.

### 6.3 Not Completed (Future Work)

❌ **Machine learning refinement:** Would require collecting user data and satisfaction feedback, which is not possible without login/data storage infrastructure.

---

## 7. DISCUSSION AND ANALYSIS

### 7.1 What Worked Well

The matching algorithm produces results that align with expectations. Testing showed consistent, interpretable outcomes:

**Strong RIASEC alignment:** Single-dominant profiles (all-R, all-I, etc.) correctly rank programmes with matching primary codes highest. For example, an all-R profile ranks Mechanical Engineering, Civil Engineering, and other hands-on programmes at the top.

**Values as meaningful tiebreaker:** In balanced profiles where RIASEC scores are similar, values become the deciding factor. This matches the intended design. Programmes with "helping-people" tags rise when students rate that value highly.

**Drill-down effectiveness:** Faculty-specific questions successfully differentiate programmes within clusters. CDE drill-down questions asking about "math vs biology" and "physical vs digital work" correctly separate Mechanical Engineering from Biomedical Engineering from Computer Engineering.

### 7.2 Limitations

Several limitations should be acknowledged:

**1. Subjective programme coding:** I manually assigned RIASEC codes to all 75 programmes with LLM tool assistance. While I reviewed suggestions and got informal feedback from volunteers, the coding remains subjective. Two different coders might assign slightly different codes. For example, is Psychology S-I or I-S? Both seem reasonable. I chose I-S because most psychology modules are research-focused, but others might disagree.

**2. Small test sample:** Only limited users tested the tool. A proper validation study would recruit 100+ pre-university students and measure their decision confidence.

**3. No academic eligibility filtering:** The tool recommends programmes based purely on interest fit. It does not check if the student meets entry requirements. A student with weak math grades might get "recommended" for Mathematics programmes they cannot actually enter. This was deliberate. The tool explores fit, not eligibility. But recommendations should be understood as "if you could get in, this would fit you."

**4. Limited drill-down coverage:** Six faculty drill-downs cover 68 out of 75 programmes. Seven programmes (Medicine, Pharmacy, Law, Dentistry) have no drill-down. These were not prioritized because they have very specific entry pathways and clear career outcomes.

**5. No data persistence:** The tool cannot save results or track history. Students must retake the questionnaire each visit. This is a deliberate design choice (maximizes accessibility, no login required) but creates friction for users who want to revisit results or show them to others.

**6. Streamlit cold start delay:** The application is deployed on Streamlit Community Cloud's free tier, which puts inactive apps to sleep after periods of non-use. When a user accesses a sleeping app, they experience a cold start delay of 10-30 seconds while the server wakes up. This creates a poor first impression and may discourage some users. This limitation is acceptable for a Final Year Project demonstration but would need to be addressed for production deployment (either through paid hosting with guaranteed uptime or migration to a different platform).

**7. Algorithm weights not validated:** The scoring weights (Primary match = 5 points, Secondary match = 3 points, etc.) are design choices based on trial and error, not scientifically validated formulas. They reflect my understanding that primary activities should matter more, but they have not been proven through formal research.

**8. Limited testing with target demographic:** All five informal testers were adults who had completed university rather than pre-university students (the target users). While this provided valuable validation of the tool's logic, it did not directly measure whether the tool meets the needs and expectations of its intended audience.

### 7.3 Strengths

Despite limitations, the tool has significant strengths:

**1. Research-backed framework:** The tool uses Holland's RIASEC theory, which has 70+ years of validation research. This is not a made-up system—it is the most-used framework in career counseling worldwide.

**2. Explainable algorithm:** Every match score can be traced to specific components. Students see exactly why each programme scored the way it did. This transparency builds trust. They can agree or disagree with scoring decisions.

**3. Comprehensive coverage:** All 75 NUS undergraduate programmes are included. Students can explore every option, not just popular programmes.

**4. Actually deployed and accessible:** The tool is live on the internet. Any pre-university student in Singapore can use it right now, free, no login required. Many FYP projects build prototypes that never leave the developer's laptop. This tool is genuinely public.

**5. Two-stage design addresses real limitation:** The drill-down system solves a problem pure RIASEC matching cannot solve. Many programmes within the same faculty share identical codes. The tool acknowledges this limitation and addresses it systematically.

### 7.4 Comparison to Existing Tools

**vs. NUS Career+:** Career+ targets current students with career direction. This tool targets pre-university students exploring options.

**vs. Pathful/Xello:** These platforms match to careers, not programmes. They provide RIASEC assessments but not Singapore-specific guidance. They are commercial products with subscription fees. This tool is free, programme-focused, and NUS-specific.

**vs. MySkillsFuture:** National platform with broad career exploration. Not designed specifically for university programme choice. This tool uses validated RIASEC framework with personalized drill-down.

The Smart Advisor Tool occupies a unique niche. It combines research-validated methodology with Singapore-specific, programme-level recommendations that no other free tool provides.

---

## 8. FUTURE WORK

Future development should focus on three areas: technical enhancements, validation studies, and deployment expansion.

### 8.1 Technical Enhancements

**1. Expand drill-down coverage:** Add drill-downs for the remaining 7 programmes (Medicine, Pharmacy, Law, Dentistry) to achieve 100% coverage.

**2. Implement results persistence:** Add optional email-results feature. After completing the questionnaire, offer to email results to the student. Store results with a unique code (no login required). Student can access results later by entering the code. Results remain accessible for 6 months.

**3. Add programme comparison feature:** Allow students to select 2-3 programmes and see side-by-side comparison (RIASEC profiles, key differences, sample career paths).

**4. Integrate academic eligibility layer:** Add optional post-results filter where students enter their grades. Tool then flags which programmes meet minimum entry requirements.

**5. Machine learning optimization:** Once user data is collected (requires login system), use satisfaction data to refine scoring weights and discover new factors that predict fit beyond RIASEC.

### 8.2 Validation Studies

**1. Deploy needs validation survey:** Execute the designed survey targeting 200+ respondents (100+ pre-university students, 100+ current NUS undergraduates). Quantify how many students feel uncertain, regret their choice, and would use a RIASEC tool.

**2. Conduct formal user study:** Recruit 50-100 pre-university students to use the tool. Measure decision confidence before vs after, perceived usefulness ratings, and whether they discovered new programmes. Compare to control group receiving standard advising only.

**3. Longitudinal outcome tracking:** This is the gold standard validation. Students use the tool before university application. Record their top matches and which programme they ultimately choose. Survey them after Year 1 about satisfaction, performance, and persistence intention. Compare students who followed recommendations vs those who did not. This would take 2-3 years but provide powerful evidence.

**4. Publish findings:** If validation studies show positive results, publish in education journals to disseminate the work beyond NUS.

### 8.3 Deployment and Outreach

**1. Integrate with NUS Admissions:** Work with NUS Admissions Office to feature the tool on the undergraduate admissions website and include it in prospective student emails.

**2. Partner with CDE Outreach team:** The CDE Outreach team conducts sessions at junior colleges. They could introduce the tool during JC career talks, have students complete it during sessions, and gather feedback.

**3. Expand to polytechnic pathways:** Currently focused on A-level students. Could expand to polytechnic diploma students considering university progression.

**4. Create educator guide:** Develop a guide for teachers and counselors on how to interpret RIASEC results, discuss matches with students, and use the tool in group settings.

---

## 9. CONCLUSION

This project successfully developed and deployed a research-validated web tool to help pre-university students discover NUS undergraduate programmes matching their interests and values. The tool addresses a validated need: many students struggle with programme choice, leading to regret, switching, and dissatisfaction.

### 9.1 Objectives Achieved

All primary objectives were met:

✅ **RIASEC-based matching system:** 29 questions adapted from the validated O*NET Interest Profiler calculate student interest profiles.

✅ **Comprehensive coverage:** All 75 NUS undergraduate programmes were coded with RIASEC profiles and value tags using LLM tool assistance.

✅ **Two-stage algorithm:** Stage 1 ranks all programmes using weighted scoring. Stage 2 provides faculty-specific drill-down when results cluster.

✅ **Public deployment:** The tool is live, free to use, and requires no login.

✅ **Explainable recommendations:** Every match score is broken down into components students can understand.

### 9.2 Key Contributions

This project makes four contributions:

**1. First NUS-specific RIASEC tool:** No existing platform provides RIASEC-based matching specifically for NUS programmes.

**2. Novel drill-down methodology:** The two-stage system solves the limitation that programmes within faculties often share identical RIASEC codes. My supervisor suggested this approach, and I implemented it across six faculties.

**3. Research validation:** The tool applies decades of RIASEC research to the Singapore context using a proven framework.

**4. Accessible deployment:** By avoiding login requirements, the tool maximizes accessibility for school events, open houses, and public settings.

### 9.3 Personal Reflection

This project taught me valuable lessons about iterative development and the importance of user testing. I learned to use LLM tools effectively as development assistants—not to replace my judgment, but to speed up coding, question design, and content generation. The experience of building something that is actually deployed and usable by real people (not just a prototype) was extremely valuable.

The biggest challenge was the programme coding process. Assigning RIASEC codes to 75 diverse programmes required deep research into each programme's curriculum and career outcomes. LLM tools helped significantly, but I still had to make final judgment calls on ambiguous cases.

The most rewarding part was seeing the drill-down system work. When I first implemented it and saw it successfully differentiate Mechanical Engineering from Biomedical Engineering based on student preferences, it validated the entire two-stage approach.

---

## 10. REFERENCES

Holland, J. L. (1997). *Making vocational choices: A theory of vocational personalities and work environments* (3rd ed.). Psychological Assessment Resources.

Tracey, T. J., & Robbins, S. B. (2006). The interest-major congruence and college success relation: A longitudinal study. *Journal of Vocational Behavior, 69*(1), 64-89.

Allen, J., & Robbins, S. (2008). Prediction of college major persistence based on vocational interests, academic preparation, and first-year academic performance. *Research in Higher Education, 49*(1), 62-79.

Brown, S. D., Zimmerman, B. K., & Johnson, T. L. (2005). Congruence, career development, and person-environment fit. In W. B. Walsh & M. L. Savickas (Eds.), *Handbook of vocational psychology* (pp. 467-494). Lawrence Erlbaum.

Organisation for Economic Co-operation and Development. (2025). *Dream jobs? Teenagers' career aspirations and the future of work*. OECD Publishing.

National Institute of Education, Singapore. (2023). *Pathways, regrets, and realignment: A study of post-secondary choices among Singapore students*. NIE Research Office.

Institute of Policy Studies, Singapore. (2024). *Singapore perspectives: Youth and the future of work survey*. IPS.

U.S. Department of Labor. (2024). *O*NET Interest Profiler*. Retrieved from https://www.mynextmove.org/explore/ip

Pathful. (2024). *Career readiness assessments*. Retrieved from https://www.pathful.com

Oxford University Careers Service. (2024). *Career Weaver*. Retrieved from https://www.careers.ox.ac.uk/generating-career-ideas

NUS Centre for Future-ready Graduates. (2024). *Career+ platform*. National University of Singapore.

SkillsFuture Singapore. (2024). *MySkillsFuture student portal*. Retrieved from https://www.myskillsfuture.gov.sg

---

## 11. AI DECLARATION

I [Zhuang Jiajian A0255385W] declare that I have used generative AI [Claude Sonnet 4.6] in the completion of this assignment solely for research, grammar correction and refinement of phrasing. I am responsible for the content and quality of the submitted work.

---

## APPENDICES

Full appendices including questionnaire details, programme coding examples, algorithm pseudocode, test case documentation, and GitHub repository structure are available in the [project repository](https://github.com/JiajianZh/CDE4301-Smart-Advisor-Tool).

---

**Live Application:** [https://cde4301-smart-advisor-tool-8pq7cdqe3uubafqgwu5awg.streamlit.app/](https://cde4301-smart-advisor-tool-8pq7cdqe3uubafqgwu5awg.streamlit.app/)

**GitHub Repository:** [https://github.com/JiajianZh/CDE4301-Smart-Advisor-Tool](https://github.com/JiajianZh/CDE4301-Smart-Advisor-Tool)

**Documentation:** [https://jiajianzh.github.io/CDE4301-Smart-Advisor-Tool/](https://jiajianzh.github.io/CDE4301-Smart-Advisor-Tool/)