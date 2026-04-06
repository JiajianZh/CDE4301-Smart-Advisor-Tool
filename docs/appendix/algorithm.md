# Appendix C: Matching Algorithm

[← Back to Main Report](../index.md)

---

## Stage 1: Global Ranking Algorithm

### Input Data

**Student Profile:**
- RIASEC scores (6 values, 0-100 scale for each type)
- Top 2 RIASEC types (highest scores)
- Values ratings (5 items, 1-5 scale)
- Important values (only items rated 4 or 5)

**Programme Data:**
- Primary RIASEC code (1 letter)
- Secondary RIASEC code (1 letter)
- Tertiary RIASEC code (optional, 1 letter)
- Value tags (3-5 keywords)

---

### Scoring Formula

For each programme, calculate total score:

```
Total Score = RIASEC Score + Values Score + Perfect Match Bonus
```

#### Component 1: RIASEC Score

```python
riasec_score = 0

# Student's 1st interest matches programme's codes
if student_interest_1 == programme_primary:
    riasec_score += 5.0
if student_interest_1 == programme_secondary:
    riasec_score += 3.0
if student_interest_1 == programme_tertiary:
    riasec_score += 1.5

# Student's 2nd interest matches programme's codes
if student_interest_2 == programme_primary:
    riasec_score += 3.0
if student_interest_2 == programme_secondary:
    riasec_score += 2.0
if student_interest_2 == programme_tertiary:
    riasec_score += 1.0
```

**Weight rationale:**
- Primary code gets most weight (5.0, 3.0) because it represents the dominant programme activity
- Secondary code gets moderate weight (3.0, 2.0) because it's still significant (20-40% of activities)
- Student's 1st interest gets more weight than 2nd interest
- These weights are design choices based on testing, not scientifically validated

#### Component 2: Values Score

```python
values_score = 0

for each value the student rated 4 or 5:
    if that value keyword appears in programme's value tags:
        values_score += 1.0
```

**Design note:** Only ratings of 4-5 count as "important" to the student. Neutral ratings (3) don't contribute. Each matching value adds 1.0 point maximum (prevents double-counting).

#### Component 3: Perfect Match Bonus

```python
perfect_match_bonus = 0

if (student_interest_1 == programme_primary AND 
    student_interest_2 == programme_secondary):
    perfect_match_bonus += 2.0
```

**Rationale:** Reward programmes where the student's top 2 interests exactly match the programme's primary and secondary codes in the same order. This identifies programmes that are a complete fit.

---

### Example Calculation

**Student Profile:**
- Top 2 RIASEC: R (100%), I (75%)
- Important values: "technology", "innovation"

**Programme: Mechanical Engineering**
- Primary: R
- Secondary: I
- Value tags: "technology", "innovation", "problem-solving"

**Calculation:**

```
RIASEC Score:
- Student R matches Programme R (primary): +5.0
- Student I matches Programme I (secondary): +2.0
= 7.0 points

Values Score:
- "technology" matches: +1.0
- "innovation" matches: +1.0
= 2.0 points

Perfect Match Bonus:
- Student R-I matches Programme R-I exactly: +2.0
= 2.0 points

Total Score: 7.0 + 2.0 + 2.0 = 11.0 points
```

---

### Ranking Output

After calculating scores for all 75 programmes:

1. Sort programmes by total score (highest first)
2. Return top 8 programmes
3. For each programme, provide:
   - Programme name
   - Total score
   - Match explanation (which components contributed)
   - RIASEC codes
   - Value tags that matched

---

## Stage 2: Drill-Down Algorithm

### Trigger Logic

After Stage 1 ranking, check if drill-down should trigger:

```python
# Count how many of the top 8 results belong to each faculty
faculty_counts = {}
for each programme in top_8_results:
    faculty = programme.faculty
    faculty_counts[faculty] += 1

# Trigger if any faculty has 2+ programmes in top 8
for faculty, count in faculty_counts:
    if count >= 2:
        trigger_drill_down(faculty)
```

**Threshold rationale:** 2+ programmes (out of 8) means 25%+ of top results cluster in one faculty. This suggests the student needs faculty-specific differentiation.

---

### Drill-Down Scoring

Each faculty drill-down has 10 multiple-choice questions. Each answer option maps to specific programmes with point values.

**Example: CDE Drill-Down Question 3**

```
Q3: "Where would you feel most at home learning?"

A) Workshop or fabrication lab → Mechanical Eng +2, Civil Eng +1
B) Design studio → Architecture +2, Industrial Design +2
C) Computer lab → Computer Eng +2, Info Systems +1
D) Science lab → Biomedical Eng +2, Chemical Eng +2, Materials Sci +1
E) Field/construction site → Civil Eng +2, Architecture +1
```

**Scoring process:**

```python
drill_down_scores = {programme: 0 for programme in cde_programmes}

for each of 10 questions:
    selected_option = student's answer
    for programme, points in option_mappings[selected_option]:
        drill_down_scores[programme] += points

# Find programme with highest total
best_fit = programme with max(drill_down_scores)
```

**Output:** Single best-fit programme with personalized identity statement.

---

## Algorithm Validation

### Score Range Analysis

Across all test profiles:
- **Excellent matches:** 9.0-12.5 points
- **Good matches:** 6.0-9.0 points
- **Poor matches:** 3.0-6.0 points
- **Very poor matches:** 0-3.0 points

Only programmes scoring 5.0+ are shown to users. This filters out matches with almost no alignment.

### Component Contribution Analysis

For strong RIASEC profiles (one dominant type):
- RIASEC score contributes 70-80% of total
- Values contribute 15-20%
- Perfect match bonus contributes 5-10%

For balanced profiles (all types similar):
- RIASEC score contributes 50-60%
- Values contribute 30-40%
- Perfect match bonus rarely triggers

This confirms the design goal: RIASEC drives matching, values provide personalization.

---

## Implementation Notes

**Language:** Python 3.9+

**Key functions:**
- `calculate_riasec_profile()`: Converts 24 question responses to 6-type scores
- `calculate_match_scores()`: Implements Stage 1 scoring formula
- `check_drill_down_trigger()`: Detects faculty clustering
- `run_drill_down()`: Implements Stage 2 faculty-specific scoring

**Performance:** On Streamlit Cloud (shared hosting), full matching for 75 programmes completes in under 0.5 seconds.

**Data structure:** All programme data loaded from Excel into Pandas DataFrame at app startup. Scoring operates on in-memory data (no database queries).

---

[← Back to Main Report](../index.md)
