# 📚 Bookly – Book Review REST API

**Bookly** is a RESTful API built with **FastAPI** that allows users to manage books, write reviews, and handle authentication using JWT-based security.  
It supports user registration, email verification, password reset, book CRUD operations, and book reviews.

---

## 🚀 Features

### 👤 User Management
- User signup & login
- Email verification
- JWT-based authentication (Access & Refresh tokens)
- Get current logged-in user
- Logout (token revocation)
- Password reset (request & confirm)
- Send emails

### 📘 Book Management
- Create a new book
- Get all books
- Get a single book with reviews
- Get books submitted by a specific user
- Update book details
- Delete a book

### ⭐ Reviews
- Add reviews to books
- Rating & text-based reviews
- Reviews linked with users and books

---

## 🛠️ Tech Stack

- **Backend Framework:** FastAPI  
- **Language:** Python  
- **Authentication:** JWT (Bearer Tokens)  
- **API Documentation:** OpenAPI 3.1 (Swagger UI)  
- **Database:** SQL-based (PostgreSQL recommended)  
- **ORM:** SQLAlchemy / SQLModel  
- **Email Service:** FastAPI-Mail  

---

## 🔐 Authentication

Bookly uses **Bearer Token Authentication**.

- **Access Token** → Required for protected routes  
- **Refresh Token** → Used to generate a new access token  

### Security Schemes
- `AccessTokenBearer`
- `RefreshTokenBearer`

---

## 📦 API Endpoints Overview

### 🔑 Users

| Method | Endpoint | Description |
|------|---------|------------|
| POST | `/api/v1/users/signup` | Create user account |
| POST | `/api/v1/users/login` | Login user |
| GET | `/api/v1/users/verify/{token}` | Verify user account |
| GET | `/api/v1/users/me` | Get current user |
| GET | `/api/v1/users/logout` | Logout user |
| GET | `/api/v1/users/refresh-token` | Get new access token |
| POST | `/api/v1/users/send_mail` | Send email |
| POST | `/api/v1/users/password-reset-request` | Password reset request |
| GET | `/api/v1/users/password-reset-confirm/{token}` | Confirm password reset |

---

### 📚 Books

| Method | Endpoint | Description |
|------|---------|------------|
| GET | `/api/v1/books/` | Get all books |
| POST | `/api/v1/books/create-book` | Create a new book |
| GET | `/api/v1/books/{book_uid}` | Get book by UID |
| PATCH | `/api/v1/books/{book_uid}` | Update book |
| DELETE | `/api/v1/books/{book_uid}` | Delete book |
| GET | `/api/v1/books/user/{user_uid}` | Get books by user |

> 🔒 All book endpoints require an **Access Token**

---

### ✍️ Reviews

| Method | Endpoint | Description |
|------|---------|------------|
| POST | `/api/v1/reviews/book/{book_uid}` | Add review to book |

> 🔒 Requires authentication

---

## 📄 Data Models (Simplified)

### 📘 Book
- `uid`
- `title`
- `author`
- `publisher`
- `published_year`
- `language`
- `pages`
- `user_uid`
- `created_at`
- `updated_at`

### ⭐ Review
- `uid`
- `rating`
- `review_text`
- `user_uid`
- `book_uid`
- `created_at`
- `updated_at`

### 👤 User
- `uid`
- `username`
- `email`
- `first_name`
- `last_name`
- `is_verified`
- `books`
- `reviews`

---

## 📖 API Documentation

After running the server:

- **Swagger UI:**  
http://localhost:8000/docs


- **ReDoc:**  
http://localhost:8000/redoc


---

## ⚙️ Running the Project

```bash
# create virtual environment
python -m venv env
env\Scripts\activate #linux: source env/bin/activate 

# install dependencies
pip install -r requirements.txt

# run server
fastapi run src\  # for developer mode: fastapi dev src\

DATABASE_URL=
SECRET_KEY=
ACCESS_TOKEN_EXPIRE_MINUTES=
REFRESH_TOKEN_EXPIRE_DAYS=
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_SERVER=
MAIL_PORT=
