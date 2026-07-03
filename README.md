# 🚀 EchoStream - AI Powered Content Repurposing SaaS

EchoStream is an AI-powered Micro SaaS application that transforms long content into platform-specific content in seconds.

Users can generate:

- 🐦 Twitter Threads
- 💼 LinkedIn Posts
- 📝 Summaries
- 📧 Emails
- 📸 Instagram Captions

Built using React + Flask + OpenRouter API.

---

## 🌐 Live Demo

Frontend:

micro-saas-repurposing.vercel.app

Backend API:

https://echostream-backend-4jvf.onrender.com

---

## 📸 Screenshots

<img width="1721" height="871" alt="image" src="https://github.com/user-attachments/assets/0a3fea54-6569-44d7-97d4-9d8c7763071f" />


---

## ✨ Features

### Content Generation
- Generate AI-powered content instantly
- Multiple output formats
- Multiple writing tones

### Supported Formats

- Social Media
    - Twitter thread
    - LinkedIn post
    - Summary

- Email
    - Subject
    - Email body

- Instagram
    - Caption
    - Hashtags

### User Features

- Character counter
- Content history
- Copy content button
- Download generated content
- Viral enhancement button
- Free usage limit system
- Responsive UI

---

## 🛠 Tech Stack

### Frontend

- React
- Vite
- CSS

### Backend

- Python
- Flask
- Flask-CORS

### AI

- OpenRouter API
- Meta Llama 3 (8B Instruct)

### Deployment

Frontend:
- Vercel

Backend:
- Render

---

## 📂 Project Structure

```bash
Micro-Saas-Repurposing/
│
├── Backend/
│   ├── services/
│   │   └── ai_service.py
│   │
│   ├── app.py
│   ├── database.py
│   ├── config.py
│   ├── requirements.txt
│   └── .env
│
├── Frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## ⚙️ Installation

Clone repository:

```bash
git clone https://github.com/Harsh-Vardhan17Singh/Micro-Saas-Repurposing.git
```

Move into project:

```bash
cd Micro-Saas-Repurposing
```

---

# Backend Setup

Move into backend:

```bash
cd Backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`

```env
OPENROUTER_API_KEY=your_api_key_here
```

Run backend:

```bash
python app.py
```

Backend runs at:

```bash
http://127.0.0.1:5000
```

---

# Frontend Setup

Move into frontend:

```bash
cd Frontend
```

Install dependencies:

```bash
npm install
```

Create `.env`

```env
VITE_API_URL=http://127.0.0.1:5000
```

Run frontend:

```bash
npm run dev
```

Frontend runs at:

```bash
http://localhost:5173
```

---

## 🔌 API Endpoint

### Generate Content

**POST**

```bash
/generate
```

Request:

```json
{
    "text":"AI is transforming startups.",
    "tone":"professional",
    "format":"social",
    "userId":"test123"
}
```

Response:

```json
{
   "twitter":[
      "Tweet 1",
      "Tweet 2",
      "Tweet 3",
      "Tweet 4",
      "Tweet 5"
   ],
   "linkedin":"LinkedIn post...",
   "summary":"Summary...",
   "usage":1
}
```

---

## 🔒 Environment Variables

Backend:

```env
OPENROUTER_API_KEY=your_api_key
```

Frontend:

```env
VITE_API_URL=backend_url
```

---

## 🚀 Deployment

### Backend (Render)

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn app:app
```

Environment variables:

```env
OPENROUTER_API_KEY=your_api_key
```

---

### Frontend (Vercel)

Root Directory:

```bash
Frontend
```

Build Command:

```bash
npm run build
```

Output Directory:

```bash
dist
```

Environment variable:

```env
VITE_API_URL=https://your-render-backend-url.onrender.com
```

---

## 🔮 Future Improvements

- User authentication
- Subscription model
- Stripe payments
- Saved content dashboard
- Content templates
- Analytics
- More social platforms
- AI model selection

---

## 👨‍💻 Author

Harsh Vardhan Singh

GitHub:

https://github.com/Harsh-Vardhan17Singh

LinkedIn:

https://www.linkedin.com/in/harsh-vardhan-singh-618951335/

---

## ⭐ Support

If you found this project useful:

Star ⭐ the repository
