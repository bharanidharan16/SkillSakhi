import os
import re
import sqlite3
import urllib.parse
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "skillsakhi-sih-sdg5-secret-key-2026")

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skillsakhi.db")

# Demo internship catalog aligned with SDG 5 (Gender Equality & Inclusive Tech Careers)
INITIAL_INTERNSHIPS = [
    {
        "id": 1,
        "title": "Python Development Intern",
        "company": "NovaTech (Demo)",
        "domain": "Software",
        "mode": "Hybrid",
        "location": "Chennai",
        "skills": "Python, Flask, Git",
        "duration": "8 weeks",
        "stipend": "Demo: ₹8,000/month",
        "inclusive": 1,
        "inclusion_perks": "Women in Tech Mentorship • Flexible Hours",
        "description": "Build small web features, write unit tests, and learn collaborative agile software development."
    },
    {
        "id": 2,
        "title": "Data Analytics Intern",
        "company": "InsightWorks (Demo)",
        "domain": "Data",
        "mode": "Remote",
        "location": "Remote",
        "skills": "Python, SQL, Excel",
        "duration": "10 weeks",
        "stipend": "Demo: ₹10,000/month",
        "inclusive": 1,
        "inclusion_perks": "Equal Pay Certified • 1-on-1 Career Coaching",
        "description": "Explore datasets, create business reports, and communicate data-driven insights effectively."
    },
    {
        "id": 3,
        "title": "Machine Learning Intern",
        "company": "ModelSpring (Demo)",
        "domain": "AI/ML",
        "mode": "Remote",
        "location": "Remote",
        "skills": "Python, Machine Learning, Pandas",
        "duration": "12 weeks",
        "stipend": "Demo: ₹12,000/month",
        "inclusive": 1,
        "inclusion_perks": "Female Tech Leadership • Supportive Onboarding",
        "description": "Prepare training data, clean datasets, and experiment with beginner-friendly machine learning models."
    },
    {
        "id": 4,
        "title": "UI/UX Design Intern",
        "company": "PixelBridge (Demo)",
        "domain": "Design",
        "mode": "Hybrid",
        "location": "Bengaluru",
        "skills": "Figma, Wireframing, Communication",
        "duration": "6 weeks",
        "stipend": "Demo: ₹7,000/month",
        "inclusive": 0,
        "inclusion_perks": "Creative Studio Setting • Design Reviews",
        "description": "Create wireframes, conduct user research, and improve intuitive user flows for a sample web application."
    },
    {
        "id": 5,
        "title": "Cybersecurity Intern",
        "company": "SafeStack (Demo)",
        "domain": "Security",
        "mode": "On-site",
        "location": "Chennai",
        "skills": "Networking, Linux, Security Basics",
        "duration": "8 weeks",
        "stipend": "Demo: ₹8,500/month",
        "inclusive": 1,
        "inclusion_perks": "Safe Workplace Certified • Supervised Lab Training",
        "description": "Learn network vulnerability analysis and practical security fundamentals in a supervised environment."
    },
    {
        "id": 6,
        "title": "Frontend Web Development Intern",
        "company": "EmpowerCode (Demo)",
        "domain": "Web",
        "mode": "Remote",
        "location": "Remote",
        "skills": "HTML, CSS, JavaScript, React",
        "duration": "8 weeks",
        "stipend": "Demo: ₹9,000/month",
        "inclusive": 1,
        "inclusion_perks": "Women Coding Community • Peer Study Circles",
        "description": "Build accessible, mobile-first responsive web pages and reusable interactive frontend UI components."
    },
    {
        "id": 7,
        "title": "Cloud & DevOps Intern",
        "company": "SkyScale Systems (Demo)",
        "domain": "Cloud",
        "mode": "Hybrid",
        "location": "Hyderabad",
        "skills": "Linux, Git, Docker, Cloud Basics",
        "duration": "10 weeks",
        "stipend": "Demo: ₹11,000/month",
        "inclusive": 1,
        "inclusion_perks": "Diversity Hiring Partner • Cloud Certification Support",
        "description": "Assist with containerization, continuous integration workflows, and modern cloud deployment pipelines."
    },
    {
        "id": 8,
        "title": "AI Ethics & Fairness Intern",
        "company": "EquiTech Labs (Demo)",
        "domain": "AI/ML",
        "mode": "Remote",
        "location": "Remote",
        "skills": "Python, Research, Communication",
        "duration": "6 weeks",
        "stipend": "Demo: ₹10,000/month",
        "inclusive": 1,
        "inclusion_perks": "UN SDG 5 Aligned • Bias Mitigation Research",
        "description": "Analyze algorithmic bias and curate gender-fair benchmark datasets for responsible artificial intelligence."
    }
]


# -------------------------------------------------------------
# Database Helper Functions (SQLite with standard library)
# -------------------------------------------------------------

def get_db():
    """Connect to SQLite database and return connection with row factory."""
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Safely close database connection after request ends."""
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    """Create tables and seed initial demo data if empty."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                education TEXT DEFAULT '',
                skills TEXT DEFAULT '',
                interests TEXT DEFAULT '',
                preferred_mode TEXT DEFAULT 'Any',
                bio TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Internships table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS internships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                domain TEXT NOT NULL,
                mode TEXT NOT NULL,
                location TEXT NOT NULL,
                skills TEXT NOT NULL,
                duration TEXT NOT NULL,
                stipend TEXT NOT NULL,
                inclusive INTEGER DEFAULT 1,
                inclusion_perks TEXT DEFAULT '',
                description TEXT NOT NULL
            )
        """)

        # Applications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                internship_id INTEGER NOT NULL,
                status TEXT DEFAULT 'Submitted',
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(internship_id) REFERENCES internships(id)
            )
        """)

        # Saved internships table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_internships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                internship_id INTEGER NOT NULL,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(internship_id) REFERENCES internships(id),
                UNIQUE(user_id, internship_id)
            )
        """)

        # Seed internships if table is empty
        cursor.execute("SELECT COUNT(*) FROM internships")
        if cursor.fetchone()[0] == 0:
            for item in INITIAL_INTERNSHIPS:
                cursor.execute("""
                    INSERT INTO internships (
                        id, title, company, domain, mode, location,
                        skills, duration, stipend, inclusive, inclusion_perks, description
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item["id"], item["title"], item["company"], item["domain"],
                    item["mode"], item["location"], item["skills"], item["duration"],
                    item["stipend"], item["inclusive"], item["inclusion_perks"], item["description"]
                ))

        # Seed demo student account if empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            demo_password = generate_password_hash("student123")
            cursor.execute("""
                INSERT INTO users (
                    name, email, password_hash, education, skills, interests, preferred_mode, bio
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "Priya Sharma",
                "priya@example.com",
                demo_password,
                "B.Tech Computer Science (3rd Year), Anna University",
                "Python, Git, SQL, Flask",
                "Software, Data, AI/ML",
                "Remote",
                "Aspiring software engineer passionate about building inclusive technology and web applications."
            ))

        conn.commit()


# Initialize database upon module import
init_db()


# -------------------------------------------------------------
# Helper Utilities
# -------------------------------------------------------------

def get_current_user():
    """Return currently logged-in user record or None."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


def parse_skills(skills_input):
    """Normalize comma-separated skill string or list into clean list."""
    if isinstance(skills_input, list):
        items = skills_input
    elif isinstance(skills_input, str):
        items = skills_input.split(",")
    else:
        items = []
    return [skill.strip() for skill in items if skill and skill.strip()]


def score_match(student_skills, internship_skills_str):
    """Calculate match percentage, matched skills, and missing skills."""
    student_set = {s.strip().lower() for s in student_skills if s.strip()}
    req_list = parse_skills(internship_skills_str)
    req_set = {s.strip().lower() for s in req_list if s.strip()}

    if not req_set:
        return {"score": 0, "matched": [], "missing": []}

    matched = [s for s in req_list if s.strip().lower() in student_set]
    missing = [s for s in req_list if s.strip().lower() not in student_set]
    score = round(100 * len(matched) / len(req_set))

    return {
        "score": score,
        "matched": matched,
        "missing": missing
    }


def get_all_skills():
    """Retrieve unique list of all skills across opportunities."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT skills FROM internships")
    all_skills = set()
    for row in cursor.fetchall():
        for s in parse_skills(row["skills"]):
            all_skills.add(s)
    return sorted(all_skills)


def get_learning_info(title, skills_input="", domain=""):
    """
    Automatically identify relevant learning topics from each internship title
    and required skills, and dynamically generate a properly URL-encoded YouTube search URL.
    Exact format: https://www.youtube.com/results?search_query=Python+programming+tutorial
    """
    if not title:
        title = ""
    skills_list = parse_skills(skills_input) if callable(parse_skills) else []
    title_lower = title.lower()
    domain_lower = domain.lower() if domain else ""
    skills_lower = [s.lower() for s in skills_list]

    # 1. Data Analytics / Data Analyst
    if any(k in title_lower for k in ["data analyst", "data analytic", "analytics"]) or domain_lower == "data":
        topic = "Python, SQL, Excel and data analysis tutorials"
        search_query = "Python SQL Excel and data analysis tutorial"

    # 2. AI / ML
    elif any(k in title_lower for k in ["machine learning", "ai/ml", "ai / ml"]) or ("ai" in title_lower.split() and "ethics" not in title_lower) or domain_lower == "ai/ml":
        topic = "Artificial Intelligence and Machine Learning tutorials"
        search_query = "Artificial Intelligence and Machine Learning tutorial"

    # 3. Web Development / Frontend
    elif any(k in title_lower for k in ["web dev", "frontend", "front-end", "web development"]) or any(s in ["html", "css", "javascript"] for s in skills_lower):
        topic = "HTML, CSS and JavaScript tutorials"
        search_query = "HTML CSS and JavaScript tutorial"

    # 4. UI/UX Design
    elif any(k in title_lower for k in ["ui/ux", "ui ux", "design", "figma"]) or domain_lower == "design":
        topic = "UI/UX design tutorials"
        search_query = "UI UX design tutorial"

    # 5. Cybersecurity / Security
    elif any(k in title_lower for k in ["cybersecurity", "cyber security", "security"]) or domain_lower == "security":
        topic = "Cybersecurity fundamentals"
        search_query = "Cybersecurity fundamentals tutorial"

    # 6. Cloud & DevOps
    elif any(k in title_lower for k in ["cloud", "devops", "docker", "kubernetes"]) or domain_lower == "cloud":
        topic = "Cloud and DevOps fundamentals"
        search_query = "Cloud and DevOps tutorial"

    # 7. AI Ethics & Fairness
    elif any(k in title_lower for k in ["ethics", "fairness"]):
        topic = "AI ethics and responsible AI tutorials"
        search_query = "AI ethics and responsible AI tutorial"

    # 8. Python Developer / Python Programming
    elif "python" in title_lower or "python" in skills_lower:
        topic = "Python programming tutorials"
        search_query = "Python programming tutorial"

    # 9. Dynamic fallback using cleaned title and skills
    else:
        clean_title = re.sub(r'[\(\)\[\]/,&#-]', ' ', title).replace("Demo", "").replace("Intern", "").strip()
        clean_skills = [re.sub(r'[\(\)\[\]/,&#-]', ' ', s).strip() for s in skills_list[:3]]
        clean_words = [w for w in (clean_title.split() + clean_skills) if w]
        topic = f"{clean_title} tutorials" if clean_title else "Technology tutorials"
        search_query = f"{' '.join(clean_words)} tutorial".strip()

    # Clean query of extra punctuation, ensuring space-separated words for quote_plus
    clean_query_words = " ".join(re.sub(r'[,/&#\(\)]', ' ', search_query).split())
    encoded_query = urllib.parse.quote_plus(clean_query_words)
    youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"

    return {
        "topic": topic,
        "search_query": clean_query_words,
        "youtube_url": youtube_url
    }


@app.template_filter("learning_info")
def learning_info_filter(item):
    """Jinja filter to access learning info safely in templates."""
    if isinstance(item, dict) and "learning" in item and item["learning"]:
        return item["learning"]
    title = item.get("title", "") if isinstance(item, dict) else getattr(item, "title", "")
    skills = item.get("skills", "") if isinstance(item, dict) else getattr(item, "skills", "")
    domain = item.get("domain", "") if isinstance(item, dict) else getattr(item, "domain", "")
    return get_learning_info(title, skills, domain)


@app.context_processor
def inject_learning_utilities():
    """Make get_learning_info globally accessible to all Jinja templates."""
    return {
        "get_learning_info": get_learning_info
    }


# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------

@app.route("/")
@app.route("/dashboard")
def home():
    """Main dashboard: displays personalized recommendations and stats."""
    current_user = get_current_user()
    db = get_db()

    # Determine student info: prioritize logged-in profile, fallback to query parameters
    if current_user:
        student_name = current_user["name"]
        raw_skills = current_user["skills"] or "Python, Git"
        education = current_user["education"]
        interests = current_user["interests"]
    else:
        student_name = request.args.get("name", "Student").strip() or "Student"
        raw_skills = request.args.get("skills", "Python, Git")
        education = "Student Explorer"
        interests = "Software, Data, AI/ML"

    student_skills = parse_skills(raw_skills)

    # Fetch all opportunities from database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM internships")
    rows = cursor.fetchall()

    scored = []
    missing_frequency = {}

    for row in rows:
        item = dict(row)
        match_info = score_match(student_skills, item["skills"])
        item["score"] = match_info["score"]
        item["matched"] = match_info["matched"]
        item["missing"] = match_info["missing"]
        item["skills_list"] = parse_skills(item["skills"])
        learning = get_learning_info(item["title"], item["skills"], item.get("domain", ""))
        item["learning"] = learning
        item["youtube_url"] = learning["youtube_url"]
        item["learning_topic"] = learning["topic"]
        item["search_query"] = learning["search_query"]

        for miss in match_info["missing"]:
            missing_frequency[miss] = missing_frequency.get(miss, 0) + 1

        scored.append(item)

    # Sort descending by match score
    scored.sort(key=lambda x: x["score"], reverse=True)

    # Identify applied and saved internship IDs for logged-in user
    applied_ids = set()
    saved_ids = set()
    if current_user:
        cursor.execute("SELECT internship_id FROM applications WHERE user_id = ?", (current_user["id"],))
        applied_ids = {r["internship_id"] for r in cursor.fetchall()}

        cursor.execute("SELECT internship_id FROM saved_internships WHERE user_id = ?", (current_user["id"],))
        saved_ids = {r["internship_id"] for r in cursor.fetchall()}

    # Most in-demand missing skills to recommend learning
    top_missing_skills = sorted(missing_frequency.items(), key=lambda x: x[1], reverse=True)[:4]

    return render_template(
        "index.html",
        internships=scored,
        student_name=student_name,
        raw_skills=raw_skills,
        student_skills=student_skills,
        education=education,
        interests=interests,
        skill_options=get_all_skills(),
        current_user=current_user,
        applied_ids=applied_ids,
        saved_ids=saved_ids,
        top_missing_skills=[skill for skill, count in top_missing_skills]
    )


@app.route("/internships")
def internships():
    """Explore internships with keyword search, domain, work mode & SDG 5 filters."""
    current_user = get_current_user()
    db = get_db()

    query = request.args.get("q", "").strip().lower()
    domain = request.args.get("domain", "All")
    mode = request.args.get("mode", "All")
    inclusive_only = request.args.get("inclusive", "0") == "1"

    # Student skills for match score display
    if current_user:
        student_skills = parse_skills(current_user["skills"] or "Python, Git")
    else:
        student_skills = parse_skills(request.args.get("skills", "Python, Git"))

    cursor = db.cursor()
    cursor.execute("SELECT * FROM internships")
    rows = cursor.fetchall()

    results = []
    domains_set = set()

    for row in rows:
        item = dict(row)
        domains_set.add(item["domain"])
        item["skills_list"] = parse_skills(item["skills"])
        match_info = score_match(student_skills, item["skills"])
        item["score"] = match_info["score"]
        item["matched"] = match_info["matched"]
        item["missing"] = match_info["missing"]
        learning = get_learning_info(item["title"], item["skills"], item.get("domain", ""))
        item["learning"] = learning
        item["youtube_url"] = learning["youtube_url"]
        item["learning_topic"] = learning["topic"]
        item["search_query"] = learning["search_query"]

        # Search filter
        searchable = " ".join([
            item["title"], item["company"], item["domain"],
            item["description"], item["skills"], item["location"],
            item.get("inclusion_perks", "")
        ]).lower()

        if query and query not in searchable:
            continue
        if domain != "All" and item["domain"] != domain:
            continue
        if mode != "All" and item["mode"] != mode:
            continue
        if inclusive_only and not item["inclusive"]:
            continue

        results.append(item)

    # Sort by match score if skills present
    results.sort(key=lambda x: x["score"], reverse=True)

    applied_ids = set()
    saved_ids = set()
    if current_user:
        cursor.execute("SELECT internship_id FROM applications WHERE user_id = ?", (current_user["id"],))
        applied_ids = {r["internship_id"] for r in cursor.fetchall()}

        cursor.execute("SELECT internship_id FROM saved_internships WHERE user_id = ?", (current_user["id"],))
        saved_ids = {r["internship_id"] for r in cursor.fetchall()}

    return render_template(
        "internships.html",
        internships=results,
        domains=sorted(domains_set),
        q=request.args.get("q", ""),
        selected_domain=domain,
        selected_mode=mode,
        inclusive_only=inclusive_only,
        current_user=current_user,
        applied_ids=applied_ids,
        saved_ids=saved_ids
    )


# -------------------------------------------------------------
# Authentication Routes (Register, Login, Logout)
# -------------------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new student account."""
    if get_current_user():
        return redirect(url_for("home"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        education = request.form.get("education", "").strip()
        skills = request.form.get("skills", "").strip()
        interests = request.form.get("interests", "").strip()
        preferred_mode = request.form.get("preferred_mode", "Any")
        bio = request.form.get("bio", "").strip()

        if not name or not email or not password:
            flash("Please fill in your name, email, and password.", "error")
            return render_template("register.html", name=name, email=email, education=education, skills=skills)

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            flash("An account with this email already exists. Please log in.", "error")
            return redirect(url_for("login"))

        password_hash = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, education, skills, interests, preferred_mode, bio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, email, password_hash, education, skills, interests, preferred_mode, bio))
        db.commit()

        new_user_id = cursor.lastrowid
        session["user_id"] = new_user_id
        session["user_name"] = name

        flash(f"Welcome to SkillSakhi, {name}! Your profile is ready.", "success")
        return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in an existing student."""
    if get_current_user():
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash(f"Welcome back, {user['name']}! Here are your latest matches.", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password. You can use the one-click demo login below.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log out current user."""
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for("home"))


# -------------------------------------------------------------
# Student Profile Route
# -------------------------------------------------------------

@app.route("/profile", methods=["GET", "POST"])
def profile():
    """View and update student profile: skills, education, and interests."""
    current_user = get_current_user()
    if not current_user:
        flash("Please log in or register to view and update your profile.", "info")
        return redirect(url_for("login"))

    db = get_db()
    cursor = db.cursor()

    if request.method == "POST":
        name = request.form.get("name", "").strip() or current_user["name"]
        education = request.form.get("education", "").strip()
        skills = request.form.get("skills", "").strip()
        interests = request.form.get("interests", "").strip()
        preferred_mode = request.form.get("preferred_mode", "Any")
        bio = request.form.get("bio", "").strip()

        cursor.execute("""
            UPDATE users
            SET name = ?, education = ?, skills = ?, interests = ?, preferred_mode = ?, bio = ?
            WHERE id = ?
        """, (name, education, skills, interests, preferred_mode, bio, current_user["id"]))
        db.commit()
        session["user_name"] = name
        flash("Your profile has been updated successfully!", "success")
        return redirect(url_for("profile"))

    # Fetch student's applied internships
    cursor.execute("""
        SELECT i.*, a.applied_at, a.status
        FROM applications a
        JOIN internships i ON a.internship_id = i.id
        WHERE a.user_id = ?
        ORDER BY a.applied_at DESC
    """, (current_user["id"],))
    applied_internships = [dict(r) for r in cursor.fetchall()]

    # Fetch student's saved internships
    cursor.execute("""
        SELECT i.*, s.saved_at
        FROM saved_internships s
        JOIN internships i ON s.internship_id = i.id
        WHERE s.user_id = ?
        ORDER BY s.saved_at DESC
    """, (current_user["id"],))
    saved_internships = [dict(r) for r in cursor.fetchall()]

    # Calculate profile completeness score
    fields = [current_user["name"], current_user["education"], current_user["skills"],
              current_user["interests"], current_user["bio"]]
    completeness = round(100 * sum(1 for f in fields if f and f.strip()) / len(fields))

    return render_template(
        "profile.html",
        current_user=current_user,
        applied_internships=applied_internships,
        saved_internships=saved_internships,
        completeness=completeness,
        all_skills=get_all_skills()
    )


# -------------------------------------------------------------
# Internship Actions (Apply & Save)
# -------------------------------------------------------------

@app.route("/apply/<int:internship_id>", methods=["POST"])
def apply_internship(internship_id):
    """Submit a sample application for an internship."""
    current_user = get_current_user()
    if not current_user:
        flash("Please log in to apply for demo internships.", "info")
        return redirect(url_for("login"))

    db = get_db()
    cursor = db.cursor()

    # Check if already applied
    cursor.execute("""
        SELECT id FROM applications WHERE user_id = ? AND internship_id = ?
    """, (current_user["id"], internship_id))
    existing = cursor.fetchone()

    cursor.execute("SELECT title, company FROM internships WHERE id = ?", (internship_id,))
    internship = cursor.fetchone()

    if not existing and internship:
        cursor.execute("""
            INSERT INTO applications (user_id, internship_id, status)
            VALUES (?, ?, 'Submitted')
        """, (current_user["id"], internship_id))
        db.commit()
        flash(f"🎉 Application submitted for {internship['title']} at {internship['company']}! (Demo listing)", "success")
    elif existing:
        flash("You have already applied for this opportunity.", "info")

    return redirect(request.referrer or url_for("home"))


@app.route("/save/<int:internship_id>", methods=["POST"])
def save_internship(internship_id):
    """Bookmark or toggle save an internship."""
    current_user = get_current_user()
    if not current_user:
        flash("Please log in to save internships to your profile.", "info")
        return redirect(url_for("login"))

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT id FROM saved_internships WHERE user_id = ? AND internship_id = ?
    """, (current_user["id"], internship_id))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            DELETE FROM saved_internships WHERE user_id = ? AND internship_id = ?
        """, (current_user["id"], internship_id))
        db.commit()
        flash("Removed from saved bookmarks.", "info")
    else:
        cursor.execute("""
            INSERT INTO saved_internships (user_id, internship_id)
            VALUES (?, ?)
        """, (current_user["id"], internship_id))
        db.commit()
        flash("Internship saved to your bookmarks!", "success")

    return redirect(request.referrer or url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
