# 🔗 CodeAlpha - Simple URL Shortener

A lightweight, robust URL shortening service featuring a RESTful API, SQLite persistent storage, and an interactive dark-themed web client.

Developed as part of the **CodeAlpha Backend Development Internship** (Task 1).

---

## 🌟 Features

- **Base62 Unique Hash Generation**: Generates 6-character alphanumeric tokens ($62^6 \approx 56.8 \text{ billion}$ unique combinations).
- **Collision Resistance**: Verifies candidate keys against the database to guarantee complete uniqueness.
- **HTTP 302 Redirection**: Performs temporary redirection with server-side click tracking per access.
- **Analytics & Click Tracking**: Increments real-time hit counts stored permanently in SQLite.
- **Asynchronous Web Client**: Single-page UI utilizing JavaScript Fetch API for real-time link creation and one-click clipboard copying.

---

## 🏗️ Database Schema & SQL Design

```sql
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT NOT NULL,
    short_code TEXT NOT NULL UNIQUE,
    clicks INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Core SQL Operations:
- **Save URL Mapping**:
  ```sql
  INSERT INTO urls (original_url, short_code) VALUES (?, ?);
  ```
- **Fetch Target URL**:
  ```sql
  SELECT * FROM urls WHERE short_code = ?;
  ```
- **Increment Click Counter**:
  ```sql
  UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?;
  ```

---

## 📡 REST API Endpoints

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Web application UI | `200 OK` |
| `POST` | `/api/shorten` | Shorten a long URL (`{"url": "..."}`) | `201 Created` / `400` |
| `GET` | `/<short_code>` | Redirects to original destination | `302 Found` / `404` |
| `GET` | `/api/stats/<short_code>` | Retrieve link analytics (clicks, timestamp) | `200 OK` / `404` |

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- Flask (`pip install flask`)

### 2. Run the Application
1. Open your terminal in the directory:
   ```powershell
   cd D:\url-shortener
   ```
2. Start the server:
   ```powershell
   python app.py
   ```
3. Visit the dashboard:
   ```
   http://127.0.0.1:5000
   ```

---

## 📂 Project Structure

```
url-shortener/
├── app.py              # Main Flask server, Base62 logic, and route handlers
├── database.py         # SQLite connection manager and SQL helper functions
├── urls.db             # Local SQLite database (auto-generated)
├── templates/
│   └── index.html      # Responsive frontend interface
└── .gitignore          # Prevents committing temporary and database files
```
