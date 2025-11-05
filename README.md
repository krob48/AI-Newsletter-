# 🧠 AI-Powered Business & Tech Newsletter

This project automatically collects **recent business and technology news**, summarizes the content with **OpenAI**, formats it into a clean **HTML newsletter**, and optionally **emails it to subscribers** on a schedule.  
It was built for my *Business Applications Development* class to demonstrate API integration, automation, and real-world application of Python.

---

## 🚀 Features
- **Fetches news** from [The Guardian Open Platform](https://open-platform.theguardian.com/)
- **Summarizes** articles using OpenAI (or a fallback if no API key)
- **Renders** a timestamped HTML newsletter
- **Sends** the newsletter via email (using Gmail SMTP)
- **Automates** daily sending via macOS/Linux cron or Windows Task Scheduler
- Configurable topics, sections, recipients, and schedule

---

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Libraries:** `requests`, `python-dotenv`, `openai`
- **APIs:** Guardian Open Platform, OpenAI API
- **Email:** SMTP (Gmail App Passwords recommended)
- **Scheduler:** macOS `cron` / Windows Task Scheduler

---

## 📦 Setup Instructions

### 1️⃣ Clone or download the project
```bash
git clone https://github.com/yourusername/AI-Newsletter.git
cd AI-Newsletter
```

### 2️⃣ Create and activate a virtual environment
**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Create a file named **`.env`** in the project root with your API keys and email settings:

```bash
# Guardian API (get free key from https://open-platform.theguardian.com/)
GUARDIAN_API_KEY=your_guardian_api_key_here

# OpenAI API (https://platform.openai.com/)
OPENAI_API_KEY=your_openai_api_key_here

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password   # App Password, not your regular password
FROM_NAME=AI Newsletter
FROM_EMAIL=your_email@gmail.com
```

---

## ⚙️ How to Run

###  Dry-run (no email, opens in browser)
```bash
python main.py --topics "business,technology" --max_articles 5 --dry_run
```

### 📧 Send as email
```bash
python main.py --topics "business,technology" --max_articles 5 --to your_email@gmail.com
```

### 🖥️ Skip browser opening (for cron/task scheduler)
```bash
python main.py --topics "business,technology" --max_articles 5 --to your_email@gmail.com --no_open
```

Each run generates a file under:
```
out/newsletter_YYYY-MM-DD_HH-MM-SS.html
```

---

## 🗓️ Automate with a Scheduler

### macOS / Linux (Cron)
1. Open your crontab:
   ```bash
   crontab -e
   ```
2. Add this line (runs every day at 8:05 AM):
   ```bash
   PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
   5 8 * * * /Users/admin/Desktop/AI-Newsletter-/.venv/bin/python /Users/admin/Desktop/AI-Newsletter-/main.py --topics "business,technology" --max_articles 6 --to your_email@gmail.com --no_open >> /Users/admin/Desktop/AI-Newsletter-/out/cron.log 2>&1
   ```

### Windows (Task Scheduler)
- **Action:** `Start a Program`
- **Program/script:** `C:\path\to\AI-Newsletter-\.venv\Scripts\python.exe`
- **Arguments:** `C:\path\to\AI-Newsletter-\main.py --topics "business,technology" --max_articles 6 --to your_email@gmail.com --no_open`
- **Start in:** `C:\path\to\AI-Newsletter-`

---

##  Project Structure
```
AI-Newsletter-/
├── main.py                # Orchestrates the workflow
├── config.py              # Loads .env and global variables
├── fetch.py               # Queries Guardian API for articles
├── summarize.py           # Summarizes content (AI or fallback)
├── render.py              # Builds the HTML newsletter
├── emailer.py             # Sends email via SMTP
├── requirements.txt       # Project dependencies
├── .env                   # API and SMTP configuration
└── out/                   # Generated newsletters + cron logs
```

---

##  Example Output
Each section includes:
- **Headline**
- **Article link**
- **AI-generated summary bullets**

---

## 🧠 Lessons Demonstrated
- REST API integration (Guardian, OpenAI)
- Secure credential management with `.env`
- Automation & scheduling (cron)
- HTML generation and templating
- Email automation with SMTP
- Code modularization and reusability

---

## ✨ Future Improvements
- Add multiple news sources (NewsAPI, GNews)
- Include keyword filtering and deduplication
- Integrate with Mailchimp or SendGrid
- Add a front-end interface for topic selection
- Store sent newsletters in a database

---

## 🧑‍💻 Author
**Keyla Roberts**  
Business Applications Development | Tennessee Tech University  
📧 [sebastiankeyla.ks@gmail.com](mailto:sebastiankeyla.ks@gmail.com)

---

## 📜 License
This project is for **educational and demonstration purposes**.  
You may reuse or adapt this code for non-commercial, academic use.
