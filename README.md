# 🚀 Spotifly Backend (FastAPI)

This is the backend service for Spotifly, built using [FastAPI](https://fastapi.tiangolo.com/), with dependencies managed by [uv](https://github.com/astral-sh/uv).  
This guide is for **frontend developers** or collaborators who **do not have Python installed** and want to run the backend locally.

---

## 📦 Requirements

- [Python 3.12.3](https://www.python.org/downloads/release/python-3123/)
- [uv](https://github.com/astral-sh/uv) (ultrafast package manager)

---

## ✅ Step-by-Step Setup

### 1. 📥 Install Python 3.12.3

If you don't have Python installed:

- **Windows/macOS/Linux**: Download from [python.org](https://www.python.org/downloads/release/python-3123/)
- During install:
  - ✅ Check **"Add Python to PATH"**
  - ✅ Enable `pip`

To verify:

```bash
python3 --version 
# or
python --version
```

### 2. 📥 Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# or with Homebrew (macOS)
brew install astral-sh/uv/uv
```

```bash
uv --version
```

## 3. 📁 Clone the Repository

```bash
git clone https://github.com/your-org/spotifly-backend.git
cd spotifly-backend
```

## 4. 🐍 Create and Activate Virtual Environment

```bash
uv venv
source .venv/bin/activate   # macOS/Linux
# or
.venv\Scripts\activate.bat  # Windows CMD
```

## 5. 📦 Install Dependencies

```bash
uv pip install .
# Or from lockfile (if `uv.lock` exists)
uv pip install --locked
```

## 6. 🚀 Run the API Server

```bash
uvicorn main:app --reload
```

Swagger can be found on: http://localhost:8000/docs when running the backend