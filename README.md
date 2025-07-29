# Tasklytics

Tasklytics is a full-stack task management application built with **FastAPI** and **React (Vite + TypeScript)**. It allows users to register, log in, manage tasks, and receive email notifications for due tasks.

---

## 🚀 Tech Stack

### Backend (Python / FastAPI)

* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic v2
* FastAPI-Mail (Outlook SMTP)
* APScheduler (task reminders)
* JWT authentication

### Frontend (React / Vite / TypeScript)

* React 18
* Vite
* TypeScript
* CSS Modules

---

## ✨ Features

* User registration with email & password
* JWT login and secure token-based authentication
* Task CRUD (Create, Read, Update, Delete)
* Due date email notifications via Outlook
* Task scheduler with background jobs
* Responsive, modern UI
* Deployment ready for **Render.com**

---

## 🧪 Local Development

### Backend

```bash
# Set up and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 📦 Build for Production

```bash
cd frontend
npm run build
```

This will create a production-ready `/dist` folder.

---

## ☁️ Deploy to Render

### 1. Push to GitHub

Make sure `.env` is in your `.gitignore`, and only commit `.env.example`.

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/tasktracker.git
git push -u origin main
```

### 2. Create Web Service on [Render.com](https://render.com)

* Use **Render's Web Service** for FastAPI backend
* Set build command: `./start.sh`
* Set environment variables using `.env.example`

### 3. Create PostgreSQL instance

* Use Render's managed PostgreSQL
* Set `DATABASE_URL` in Render dashboard

---

## 🛠 Environment Variables

See `.env.example` for required environment variables:

```env
JWT_SECRET=your_secret_key
DATABASE_URL=postgresql://user:pass@host/dbname
SMTP_USER=you@example.com
SMTP_PASS=your_app_password
MAIL_USERNAME=you@example.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=you@example.com
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_STARTTLS=true
MAIL_SSL_TLS=false
```

---

## ✅ API Documentation

Visit `http://localhost:8000/docs` for Swagger UI.

---

## 📄 License

MIT License. Free to use and modify.

---

## 🙌 Author

Luis Colón
GitHub: [lcolon231](https://github.com/lcolon231)
LinkedIn: [Luis Colón](https://www.linkedin.com/in/luiscolon31)

---

## ⭐ Suggestions

Feel free to fork and improve this project. Pull requests welcome!
