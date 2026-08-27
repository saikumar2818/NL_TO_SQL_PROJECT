#  Transactional Natural Language to SQL (NL-to-SQL) Engine

A production-ready Natural Language to SQL engine powered by **Gemini 2.5 Flash** and an in-memory **SQLite** instance. The engine translates plain-English queries into valid SQL, strictly enforces schema rules, classifies transactional risk, and requires Human-in-the-Loop (HITL) approval before executing data-modifying queries.

---

## 🔥 Key Highlights

* **Schema-Aware Translation:** Injects relational constraints, table schemas, and foreign keys directly into the model context.
* **Deterministic Output:** Generates structured JSON responses to classify operations (`READ` vs `WRITE`), report assumptions, and isolate missing entities.
* **Zero-Trust Safety & HITL Guardrails:** Blocks catastrophic commands (like `DELETE` without a `WHERE` clause) and requires CLI confirmation (`[y/N]`) prior to executing `INSERT`, `UPDATE`, or `DELETE` statements.
* **Interactive Rich UI:** Features syntax highlighting, execution status badges, mock database seeding, and a live terminal prompt loop.

---

## 🛠 Tech Stack

* **Language:** Python 3.10+
* **LLM Core:** Google Gemini 2.5 Flash (`google-genai`)
* **Database:** SQLite3 (In-Memory Engine)
* **CLI Architecture:** Rich UI (`rich`), `python-dotenv`

---

## 🚀 Quickstart Guide

### 1. Repository Setup

```bash
git clone https://github.com/your-username/nl-to-sql-engine.git
cd nl-to-sql-engine

```

### 2. Environment Activation & Dependencies

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

```

### 3. API Key Configuration

Create a `.env` file in the root project folder:

```env
GEMINI_API_KEY=your_gemini_api_key_here

```

### 4. Run the Engine

```bash
python main.py

```

---

## ⚡ Safety Matrix

| Query Intent | Classification | System Action |
| --- | --- | --- |
| **`SELECT` Operations** | `READ` | Validates syntax, executes query, and renders data in a formatted terminal table. |
| **`INSERT / UPDATE / DELETE`** | `WRITE` | Flags write risk, pauses execution, and requests explicit user approval (`[y/N]`). |
| **Mass Deletion (No `WHERE`)** | `HIGH_RISK` | Intercepted via system instruction, marked `is_executable: false`, and aborted. |
| **Invalid Column / Table** | `SCHEMA_ERROR` | Identifies missing attributes, displays an error panel, and stops execution. |

---
