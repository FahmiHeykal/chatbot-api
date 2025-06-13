# Chatbot API – FastAPI + OpenAI + PostgreSQL

Ini adalah Chatbot REST API lengkap menggunakan FastAPI. API ini memungkinkan user untuk login, mengirim pesan ke chatbot (OpenAI GPT), dan mendapatkan ringkasan harian/mingguan. Data tersimpan di PostgreSQL dan sistem autentikasi menggunakan JWT dengan akses admin/user.

## Fitur Utama

- Autentikasi JWT (register, login)
- Chat dengan AI (GPT-3.5)
- Log seluruh percakapan per user
- Ringkasan otomatis (harian & mingguan)
- Admin panel: melihat log semua user & hasil ringkasan
- Endpoint untuk generate ringkasan manual
- Dokumentasi Swagger otomatis (/docs)

## Teknologi yang Digunakan

- FastAPI
- OpenAI GPT-3.5
- PostgreSQL
- SQLAlchemy
- JWT (OAuth2)
- Pydantic
- Uvicorn

## Endpoint Utama
Register : POST /auth/register  
Login & dapatkan token : POST /auth/token  
Kirim chat : POST /chat/  
Lihat log chat sendiri : GET /chat/logs  
Lihat profil user : GET /chat/me  
Admin - lihat semua log : GET /admin/logs  
Admin - lihat semua ringkasan : GET /admin/summaries/  
Admin - generate ringkasan manual : POST /admin/summaries/daily atau /weekly

## Cara Menjalankan Proyek

1. Clone repo ini :  
`git clone https://github.com/FahmiHeykal/chatbot-api.git`

2. Buat virtual environment dan install dependencies:  
`python -m venv venv 
 venv/bin/activate`  
`pip install -r requirements.txt`

3. Buat file .env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=supersecretkey
OPENAI_API_KEY=sk-xxxx
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
CORS_ORIGINS=["*"]

4. Jalankan server:  
`uvicorn main:app --reload`

5. Akses dokumentasi API di browser:  
`http://localhost:8000/docs`

## Catatan

- Token dikirim via header Authorization: Bearer <token>
- Model OpenAI default : gpt-3.5
- Ringkasan otomatis dijalankan berdasarkan data user
- Admin hanya bisa diatur manual via database
