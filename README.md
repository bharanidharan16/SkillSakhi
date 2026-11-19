# SkillSakhi — SIH Inclusive Internship & Skill Matching Portal

SkillSakhi is an Academia–Industry Skill & Internship Portal prototype aligned with **UN Sustainable Development Goal 5: Gender Equality**. It empowers female students and early-career learners through transparent, skills-based opportunity matching, bias-free recommendations, and supportive tech mentorship.

---

## ✨ Features Implemented

1. **Modern, Responsive, Mobile-Friendly UI**
   - Lavender & mint pastel theme with accessible contrast and clean typography.
   - Interactive mobile navigation menu drawer that works smoothly on phones, tablets, and desktops.
   - Real-time flash notification banners for user feedback.

2. **Student Registration & Login Interface**
   - Secure student registration with password hashing (`werkzeug.security`).
   - Session-based authentication with persistent SQLite database (`skillsakhi.db`).
   - One-click demo login option (`priya@example.com` / `student123`) for rapid evaluation.

3. **Comprehensive Student Profile**
   - Editable profile with Education/University, listed Skills, Career Interests, Preferred Work Mode, and Bio.
   - Interactive skill tags cloud allowing students to add in-demand skills with one click.
   - Profile strength meter calculating readiness percentage.
   - History of submitted demo applications and bookmarked internships.

4. **Internship Listings with Advanced Search & Filters**
   - Full-text keyword search across titles, companies, domains, descriptions, skills, and locations.
   - Filters for **Domain** (Software, Data, AI/ML, Design, Security, Web, Cloud) and **Work Mode** (Remote, Hybrid, On-site).
   - Dedicated **🌸 SDG 5 Women-Inclusive Only** toggle.
   - Reset filter button for quick clearing.

5. **Transparent Skill-Based Matching Engine**
   - Normalizes and compares student skills against required opportunity skills.
   - Computes real-time match percentage (0–100%) and visual progress bar.
   - Highlights **✓ Matched Skills** and **+ Skills to Learn Next**.
   - Identifies candidate's top skill gap to accelerate upskilling.

6. **Inclusive Design Supporting Women in Tech (SDG 5)**
   - Flags organizations with verified inclusive practices (Female Tech Leadership, Mentorship Circles, Equal Pay Transparency, Safe Workplace certification).
   - SDG 5 commitment panels and bias-mitigation resources.

7. **Personalized Recommendations Dashboard**
   - KPI metrics: Total Opportunities, Listed Skills, and Top Match Percentage.
   - Recommended opportunities sorted by skill compatibility.
   - "🏆 Top Recommendation" badge for the best-fit role.
   - "Bridge Your Skill Gap" roadmap spotlighting the most requested missing skills.

8. **Demo Application & Bookmark System**
   - Click "Apply (Demo)" to record an application and track its status.
   - Bookmark opportunities with "☆ Save" / "★ Saved" toggle.

9. **"Learn Before You Apply" — Video Tutorial Integration**
   - Automatically maps each internship title and required skills to relevant YouTube learning tutorials.
   - Displays a dedicated **Recommended Learning** box on every internship card.
   - **"Watch Learning Videos ↗"** button dynamically opens safe, properly URL-encoded YouTube search results in a new tab (`target="_blank" rel="noopener noreferrer"`).
   - Topic examples:
     - *Python Developer Intern* → Python programming tutorials
     - *Web Development Intern* → HTML, CSS and JavaScript tutorials
     - *AI/ML Intern* → Artificial Intelligence and Machine Learning tutorials
     - *Data Analyst Intern* → Python, SQL, Excel and data analysis tutorials
     - *UI/UX Design Intern* → UI/UX design tutorials
     - *Cybersecurity Intern* → Cybersecurity fundamentals

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10 or newer
- VS Code or your preferred code editor / terminal

### Step-by-Step Setup

1. **Navigate to the project folder:**
   ```powershell
   cd "SkillSakhi_SIH_Starter_Project/skillsakhi_sih_project"
   ```

2. **Create a Python Virtual Environment:**
   - **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
     *(If script execution is disabled in PowerShell, open Command Prompt or run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

   - **Windows (Command Prompt):**
     ```bat
     python -m venv .venv
     .venv\Scripts\activate.bat
     ```

   - **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
   *(Only standard Flask is required; SQLite and Werkzeug come bundled with Python and Flask).*

4. **Start the Flask Application:**
   ```powershell
   python app.py
   ```

5. **Open in Your Browser:**
   Navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 🔑 Pre-Configured Demo Credentials

For quick testing without creating a new account:
- **Email:** `priya@example.com`
- **Password:** `student123`
*(On the `/login` page, you can also simply click the **"⚡ Use Demo Student (Priya)"** button to autofill credentials instantly).*

---

## 🧪 Testing Guide

1. **Test Registration & Login:**
   - Click **Login** in the top navigation bar. Click the demo button to sign in, or click **Register** to create a new student account.
2. **Test Profile Management:**
   - Go to **My Profile** in the top menu.
   - Click on any skill chip in the suggestions list (e.g. `+ React` or `+ Docker`) to instantly add it to your profile.
   - Update your education or bio and click **Save Profile Changes**.
3. **Test Skill-Based Matching:**
   - Go to the **Dashboard**. Note how the match score updates based on your profile's skills.
   - Check the **Matched Skills (✓)** and **Skills to Learn Next (+)** tags.
4. **Test Internship Search & Filters:**
   - Click **Explore Internships**.
   - Search for `Python` or `Remote`.
   - Check the **🌸 SDG 5 Women-Inclusive Only** checkbox to view companies offering female mentorship and equal-pay transparency.
5. **Test Demo Applications & Bookmarks:**
   - Click **Apply (Demo)** on any opportunity card. Notice the instant status badge update to **✓ Applied**.
   - Go to **My Profile** to view your application history.
6. **Test Mobile Responsiveness:**
   - Resize your browser window or switch to mobile device emulation in Chrome/Edge DevTools (F12) to test the hamburger menu and flexible card layout.
7. **Test "Learn Before You Apply" Feature:**
   - On either the **Dashboard** or **Explore Internships** page, look for the **Recommended Learning** section on any internship card.
   - Click the **Watch Learning Videos ↗** button.
   - Verify that a new browser tab opens directly to YouTube search results with the dynamically identified topic tutorials (e.g. *Python programming tutorials*, *HTML, CSS and JavaScript tutorials*, *Cybersecurity fundamentals*).

---

## 📁 Project Architecture

```
skillsakhi_sih_project/
├── app.py                 # Flask server, SQLite models, match engine, routes
├── requirements.txt       # Flask dependency specification
├── README.md              # Documentation and running instructions
├── skillsakhi.db          # SQLite database (auto-generated on first run)
├── static/
│   └── style.css          # Modern, responsive CSS theme (Lavender/Mint/SDG 5)
└── templates/
    ├── base.html          # Global layout, mobile navbar, flash messages, footer
    ├── index.html         # Student dashboard & recommended internships
    ├── internships.html   # Search, filter, and discovery catalog
    ├── login.html         # Student authentication interface with demo helper
    ├── register.html      # Account creation with skills and education inputs
    └── profile.html       # Profile management, applications, and saved roles
```

---

## 🤝 SDG 5 Alignment

All organizations, vacancies, and stipend figures in this prototype are fictional demo data created for the Smart India Hackathon (SIH). Match scores are transparent calculations based on listed technical skills.
