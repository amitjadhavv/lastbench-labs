# LastBench Labs

LastBench Labs is a specialized recruitment and screening platform designed to identify and verify expert AI evaluators. It leverages a custom-built AI Screening Agent powered by **Gemini 2.5** to conduct rigorous technical interviews across various AI/ML domains.

## 🚀 Key Features

- **AI-Driven Screening**: An interactive, chat-based interview agent that evaluates candidates on specific skills like RLHF, Hallucination Detection, and Model Benchmarking.
- **Specialized Skill Sets**: Supports over 15+ specialized AI evaluation tasks.
- **Admin Dashboard**: A secure staff portal for reviewing candidate transcripts, AI scores, and professional profiles.
- **Serverless PostgreSQL**: Powered by Neon Tech for high-performance, scalable data storage.
- **Clean UI**: A modern, responsive interface built with Bootstrap 5.

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Django 5.x
- **Database**: PostgreSQL (Neon Tech)
- **AI Engine**: Google Gemini 2.5 (via `google-genai` SDK)
- **Frontend**: HTML5, Bootstrap 5, Vanilla JavaScript
- **Auth**: Django built-in authentication with separate portals for Evaluators and Staff.

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd lastbench-labs
```

### 2. Set up the Virtual Environment
```bash
# Windows
python -m venv myproj
.\myproj\Scripts\activate

# Install dependencies
pip install django psycopg2-binary dj-database-url google-genai
```

### 3. Configure Database & AI Key
In `lastbench_project/settings.py`, update the following:
- **Database**: Add your Neon connection string to the `DATABASES` section.
- **API Key**: Add your `GEMINI_API_KEY`.

### 4. Initialize the Project
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_skills
```

### 5. Create an Admin Account
```bash
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('Admin', 'admin@example.com', 'admin')"
```

### 6. Run the Server
```bash
python manage.py runserver
```

## 📂 Project Structure

- `core/`: Main application logic, including the AI agent and dashboard views.
- `lastbench_project/`: Project-wide settings and URL configuration.
- `templates/`: Global UI layouts and shared components.
- `static/`: Custom CSS and assets.

## 🛡️ License
Distributed under the MIT License. See `LICENSE` for more information.

---
Built with ❤️ by [Your Name/Company] using Antigravity AI.
