# /verify — Post-Change Verification

Verify recent changes (new features or optimizations) are correct and safe before shipping.

## Usage

```
/verify              — auto-detect changes from git diff
/verify <file>       — verify a specific file
```

## Execution Protocol

### Step 1: Identify What Changed

Run `git diff HEAD~1 --name-only` to find changed files. If a specific file is provided via argument, focus on that file only.

Categorize changes:
- **HTML files** (`.html`) — frontend UI / calculator logic
- **Python files** (`.py`) — Flask backend logic
- **Template files** (`templates/*.html`) — Jinja2 templates
- **Config/other** — static assets, settings

### Step 2: Code Review Checklist

For each changed file, read the file and verify:

#### General
- [ ] No syntax errors (missing brackets, unclosed tags)
- [ ] No hardcoded secrets or sensitive data
- [ ] Variable names are consistent (no typos, no stale references)
- [ ] Removed code has no remaining references elsewhere

#### JavaScript (in `.html` files)
- [ ] All `document.getElementById()` targets exist in the HTML
- [ ] All functions called in `onclick`/event handlers are defined
- [ ] Math formulas are correct — manually compute one sample case and verify
- [ ] `parseFloat` / `parseInt` have fallback for NaN
- [ ] No XSS risk (user input is not injected into innerHTML without sanitization)
- [ ] Edge cases handled: zero, negative, empty input

#### Python / Flask (`app.py`)
- [ ] All `request.form` keys match the HTML form `name` attributes
- [ ] All `render_template()` variables are passed and used in the template
- [ ] Template variables in `.html` match what `render_template()` sends
- [ ] No division by zero risk
- [ ] Error handling for invalid inputs

#### Templates (`templates/*.html`)
- [ ] All `{{ variable }}` references match what the route passes
- [ ] Jinja2 syntax is valid (matching `{% %}` blocks)
- [ ] No broken HTML structure

### Step 3: Calculation Verification

If the change involves BMR/TDEE/macros or any numeric formula:

1. Pick a concrete test case (e.g., male, 30y, 181cm, 80kg, very active, 新手增肌)
2. Manually compute each step:
   - BMR (Mifflin-St Jeor): `10 * weight + 6.25 * height - 5 * age + 5`
   - BMR (Katch-McArdle if body fat given): `370 + 21.6 * lean_mass`
   - TDEE: `BMR * activity_factor`
   - Total calories: `TDEE * multiplier`
   - Protein: `g/kg * weight`
   - Fat: `g/kg * weight`
   - Carbs: `(total - protein*4 - fat*9) / 4`
3. Compare with what the code would produce
4. Flag any mismatch

### Step 4: Cross-File Consistency

If both `app.py` and `bmr.html` were changed (or should have been):
- Verify formulas are identical between frontend JS and backend Python
- Verify form field names match between `templates/index.html` and `app.py`
- Verify result variable names match between `app.py` and `templates/result_manual.html`

### Step 5: Quick Smoke Test (if Flask app)

Run:
```bash
cd /Users/zhankaiwei/Documents/training-plans
python3 -c "from app import *; print(calculate_bmr('male', 181, 80, 30))"
```

Test key functions with known inputs and verify outputs.

### Step 6: Report

Output a summary table:

```
## Verification Report

| Check                  | Status | Notes           |
|------------------------|--------|-----------------|
| HTML syntax            | PASS   |                 |
| JS element references  | PASS   |                 |
| Formula correctness    | PASS   | Verified: ...   |
| Flask ↔ Template sync  | PASS   |                 |
| XSS / Security         | PASS   |                 |
| Edge cases             | WARN   | [detail]        |
| Smoke test             | PASS   |                 |

**Test case:** Male, 30y, 181cm, 80kg, very active, 新手增肌
- BMR: 1786.3 kcal (Mifflin-St Jeor)
- TDEE: 3081 kcal
- Target: 3543 kcal (+15%)
- Protein: 144g (1.8 g/kg), Fat: 80g (1.0 g/kg), Carbs: 533g
```

If any check **FAILS**, clearly state what is wrong, which file and line, and suggest a fix.
