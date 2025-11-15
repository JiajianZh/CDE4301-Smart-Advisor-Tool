---
title: Interim Report
layout: default
---
Table of Contents
1.	Project Overview
 1.1 Project Title and Team
 1.2 Project Summary
 1.3 Value Proposition and Novelty
2.	Problem Definition and Context
 2.1 Problem Statement
3.	Objectives and Scope
 3.1 Project Objectives
 3.2 Project Scope and Boundaries
4.	Design Requirements
5.	Concept Development and Methodology
6.	Prototype Implementation
7.	Testing and Initial Results
8.	Challenges and Shortcomings
9.	Project Plan Forward
10.	References
________________________________________
1. Project Overview
1.1 Project Title and Team
Smart Advisor Tool
Student: Zhuang Jiajian, Mechanical Engineering, College of Design and Engineering
Supervisor: A/Prof Mark De Lessio
1.2 Project Summary
This project develops an online smart advisory tool targeted at high school and pre-university students who are uncertain about what to study next. The tool uses a short questionnaire to identify the student’s work preferences and learning style. A minimum viable product (MVP) has been implemented as a web application. The prototype includes a predefined dataset and a basic algorithm that ranks programmes based on user input.
1.3 Value Proposition and Novelty
This project addresses a common challenge faced by pre-university students: choosing what to study when they are still unsure about their interests and strengths. Many students feel overwhelmed by the number of university programmes and lack simple tools to help them reflect on what suits them best.
Existing platforms like NUS Career+, developed by the NUS Centre for Future-ready Graduates (CFG), support students who already have a career direction in mind. Designed for current NUS students, Career+ retrieves academic records to generate a personalised skills profile and recommends relevant upskilling courses. However, it assumes users already know what they want to do after graduation.
This project targets students at an earlier decision stage. It is intended for those still exploring their options. Rather than relying on academic data or declared goals, the tool helps users reflect on their identity and preferences, then matches them to relevant NUS undergraduate programmes. This identity-based approach supports exploration rather than career optimisation, filling a gap not addressed by current tools.
This matching approach also offers a more inclusive and relatable entry point for students who may not yet have access to strong career guidance. While career-first tools are useful for students with well-defined goals, many pre-university students come from diverse academic backgrounds and may lack exposure to structured advising or role models in professional fields. Asking students to first reflect on how they work, rather than what job they want, can help level the playing field and reduce decision anxiety. By focusing on preferences and learning style, the tool allows students to explore pathways that may align with their strengths, even if they are unfamiliar with specific programme names or job titles. This helps them discover meaningful options they might not otherwise consider, encouraging broader exploration at an early stage.
2. Problem Definition and Context
2.1 Problem Statement
Choosing what to study after high school is a challenge for many students. While some have clear goals, many are unsure about their interests or which study paths best fit them. This uncertainty is common both in Singapore and globally.
The Organisation for Economic Co-operation and Development (OECD, 2025) reported that around 40% of students are uncertain about future careers—twice as many as a decade ago. Gallup (2025) found that only 40% of Gen Z high school students had given serious thought to career plans, and fewer than 30% felt prepared to choose a post-secondary path.
In Singapore, the National Institute of Education (2023) found that about 25% of junior college and polytechnic students regretted their education pathway. The Institute of Policy Studies (2024) reported that 50% of youths aged 21 to 34 were uncertain about their future in the workforce.
When students enter a programme that does not suit their interests or working style, the consequences can be significant. Many students who realise they are in the wrong programme may disengage from learning, struggle academically, or even consider switching majors. Switching often leads to delayed graduation, additional tuition costs, or the need to repeat modules. It can also affect students’ confidence and well-being. For universities, frequent programme switching contributes to higher advising loads and lower programme retention rates. A tool that supports better decision-making at the outset can help reduce these outcomes by increasing alignment between student identity and programme choice.
These studies show that students often make major decisions without strong self-awareness or support. This can lead to dissatisfaction, disengagement, or the need to switch courses later.
3. Objectives and Scope
The objective of this project is to design and develop a smart advisory tool that helps pre-university students identify NUS programmes that fit their preferred working and learning styles. Through a short questionnaire, the system generates an identity statement and ranks suitable programmes based on match scores. The aim is to make early-stage programme exploration more guided, reflective, and user-friendly.
The project is scoped specifically for pre-university students in Singapore. It currently focuses only on undergraduate programmes at NUS. Other pathways such as polytechnic diplomas or overseas institutions are not included. The tool does not assess academic eligibility or predict outcomes. Instead, it focuses on identity-based alignment. The tool is designed to be used in a single browser session, requiring no login or data storage.
This narrow focus allows for a realistic prototype within the project timeline. It also lays the groundwork for future expansion or integration with more advanced systems.
4. Design Requirements
Design requirements translate the project vision into practical guidelines for implementation. They ensure the tool functions as intended for pre-university students making early decisions.
Functionally, the tool must allow users to complete a brief questionnaire, generate an identity summary, and receive a ranked list of NUS programmes with match scores. Streamlit was selected because it allows for quick development of interactive web applications using Python, which is the primary language used in this project. By using CSV files to store programme data, the tool avoids the complexity of database integration, making it easier to update and maintain. The choice to avoid back-end storage or login functionality was intentional. Since the target audience includes students accessing the tool on shared or school devices, removing authentication requirements ensures wider accessibility. This also makes the tool suitable for public settings such as school outreach events, career workshops, or university open houses. The goal is for the tool to be usable with minimal setup, allowing any student to receive instant, personalised guidance in a private and frictionless way. 
The algorithm should be explainable, consistent, and interpretable. The system must also provide short explanations for identity statements.
Non-functionally, the tool must run on modern browsers, require no login, and complete in under ten minutes. Language must be student-friendly, and the layout should focus on key outputs without unnecessary detail. The entire system is local-session based, built in Python with Streamlit, and uses CSV data.
Key success criteria include clarity, usability, and perceived relevance of suggestions. These design requirements will guide development and refinement in future phases.
5. Concept Development and Methodology
The system models student identity using a simplified framework inspired by RIASEC (Realistic, Investigative, Artistic, Social, Enterprising, and Conventional), adapted into work modes like builder, analyst, creative, people-oriented, and planner.
Users complete multiple-choice questions that map to these traits. Their responses are aggregated into a numerical profile vector. Each NUS programme in the dataset is manually tagged with identity traits. The system calculates similarity between the user's profile and each programme using cosine similarity, producing a match score.
The design of the questionnaire focused on making the items relevant, accessible, and easy to interpret. Questions were phrased using real-world scenarios, such as whether a student prefers hands-on tasks, data analysis, or helping others. Each option was carefully mapped to one or more identity traits in a way that avoids technical jargon or cultural bias. This ensures that students from different backgrounds can engage meaningfully with the tool without needing prior experience in self-assessment tests.
Cosine similarity was chosen as the core matching method because it is computationally simple and interpretable. It measures how similar two vectors are based on direction rather than magnitude, which fits the purpose of comparing user preferences with programme traits. This method is fast enough to run in-browser and allows for intuitive match scores on a 0–100% scale. The simplicity of the approach also makes it easier to explain to users and validate through manual review during testing.
The tool then displays a short identity summary and the top-matching programmes. Identity statements are generated using templates based on the strongest traits.
The system is built in Python using Streamlit and uses a structured CSV dataset. It does not store user data and runs fully in-browser. Though not a validated test, it is sufficient for lightweight guidance.
6. Prototype Implementation
A working MVP has been developed and deployed using Streamlit. The tool allows users to answer questions, view an identity statement, and see programme matches—all in-browser, with no login or data storage.
The initial version was designed to run locally as a Python script or static HTML, but this was limited in accessibility. The system was then shifted to a Streamlit web app hosted via GitHub, enabling instant public access.
The architecture is lightweight and self-contained. Questionnaire input, identity scoring, and programme matching are handled directly in the app. A CSV file contains manually tagged NUS programmes, and cosine similarity calculates match scores in real time.
While currently limited to 35 programmes and a basic question set, the tool demonstrates a complete, functioning end-to-end system suitable for guided programme exploration.
7. Testing and Initial Results
Informal internal testing was conducted to assess the system’s core functionality and usability. The developer tested the tool extensively using a variety of input combinations to confirm that it could produce meaningful identity statements and generate consistent match scores.
The results indicated that the tool performed reliably across a range of user profiles based on the 35 manually tagged NUS programmes. Identity summaries and programme rankings responded appropriately to different answer sets. Usability refinements were introduced during this process, including clearer question wording and a more streamlined layout.
To evaluate output consistency, structured test scenarios were created to simulate diverse user types. These included profiles with strong trait preferences (e.g., builder-heavy or people-oriented), as well as balanced or ambiguous response patterns. The tool was also tested with contradictory inputs to verify that it could still generate coherent outputs. Across all cases, match scores and identity summaries adapted logically and remained interpretable.
Some limitations were observed during testing. For example, programmes with similar tag combinations sometimes dominated the top results, suggesting a need for greater tag variety. In other cases, identity statements repeated certain phrases when one trait clearly outweighed the rest. These insights led to updates in question weighting, refinement of identity tags, and improved phrasing in the summary templates.
The tool was also tested across multiple browsers and mobile devices to confirm accessibility and layout stability. While no external testing has been completed yet, formal user evaluation is planned for the next phase of the project.
8. Challenges and Shortcomings
The tool currently uses a small dataset of 35 programmes, limiting diversity in recommendations. Tags are manually assigned based on public descriptions, which may not fully capture the nature of each programme.
All testing has been internal, with no input from external users. Without real feedback, it is unclear how students interpret the identity results or whether they find the suggestions useful.
The current questionnaire is concise but may not capture enough nuance. Identity statements may feel generic, especially for students with similar traits. The lack of data storage also limits deeper user features.
Despite these issues, the system functions as intended and serves as a viable proof of concept.
9. Project Plan Forward
In Semester 2, the project will expand the dataset, improve tag accuracy, and carry out structured user testing.
Surveys and interviews will be conducted with two key groups: (1) pre-university students to understand their expectations, and (2) NUS undergraduates to evaluate regret, satisfaction, and whether tools like this could have helped them choose more effectively.
The question set and identity summaries will be revised based on user input. Tags will be reviewed and possibly co-developed with advisors or subject matter experts.
The roadmap includes:
•	Jan–Feb: Conduct user research and interviews
•	Feb–Mar: Expand dataset, revise questionnaire
•	Mar–Apr: Run structured user tests
•	Apr–May: Final refinements and documentation
These efforts will turn the MVP into a validated, user-driven advisory tool for programme exploration.
Looking ahead, the tool could also support broader applications beyond its initial scope. For example, it could be integrated into school-level advisory sessions or career exploration workshops, particularly in secondary schools or junior colleges. It may also be useful for outreach teams during university open days, allowing prospective students to explore NUS programme fit in a personalised way. With further development, the tool could be adapted to support polytechnic pathways or mid-career learners who are considering a return to higher education.
10. References 
Gallup. (2025). Gen Z, parents lack knowledge of post–high school options. https://news.gallup.com/poll/545334/gen-z-parents-lack-knowledge-posthigh-school-options.aspx
Institute of Policy Studies. (2024). Singapore perspectives: Youth and the future of work survey. https://www.ips.org.sg
National Institute of Education. (2023). Pathways, regrets, and realignment: A study of post-secondary choices among Singapore students. Singapore: NIE Research Office.
Organisation for Economic Co-operation and Development. (2025). Dream jobs? Teenagers’ career aspirations and the future of work. Paris: OECD Publishing.


