# 🤖 Transactional Natural Language to SQL (NL-to-SQL) Engine

A production-grade, human-in-the-loop NL-to-SQL translation and execution engine built with **Gemini 2.5 Flash**, **Python**, **Rich Terminal UI**, and an **In-Memory SQLite Engine**.

This project converts complex natural language questions into syntactically valid SQL queries, classifies operation risks (`READ` vs. `WRITE`), enforces zero-trust security guardrails, and executes validated statements live with formatted CLI tables.

---

## 🌟 Key Features

* **Schema-Injected Prompting:** Dynamic context injection of relational schemas (`customers`, `orders`, `order_items`) with foreign key constraints.
* **Deterministic Structured JSON Output:** Uses strict JSON schema enforcement to output actionable query metadata (`sql_query`, `operation_type`, `is_executable`, `assumptions`, `missing_fields`).
* **Human-in-the-Loop (HITL) Guardrails:** Automatically flags data-modifying queries (`INSERT`, `UPDATE`, `DELETE`) as `WRITE` operations and requires explicit CLI confirmation (`[y/N]`) before committing changes.
* **Destructive Command Mitigation:** Blocks high-risk operations (such as `DELETE` or `UPDATE` queries without explicit `WHERE` clauses) and invalid schema entities.
* **Real-Time Live SQL Execution:** Executes validated ANSI SQL against an in-memory SQLite database populated with mock enterprise data.
* **Rich Terminal UI:** Styled syntax highlighting, status badges, automated verification test suite, and an interactive prompt loop built with `rich`.

---

## 📁 Project Architecture

```text
nl_to_sql_project/
├── .env                  # API Key configuration
├── requirements.txt      # Project dependencies (google-genai, rich, python-dotenv)
├── system_prompt.txt     # System persona, schema definition & few-shot examples
├── db_setup.py           # In-memory SQLite database builder & mock data seeder
├── main.py               # Main CLI execution engine & terminal user interface
└── README.md             # Project documentation

```

---

## 🚀 Getting Started

### Prerequisites

* **Python 3.10+** installed on your system.
* A free **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/).

### Installation & Setup

1. **Clone or create the project folder:**
```bash
mkdir nl_to_sql_project
cd nl_to_sql_project

```


2. **Set up a Virtual Environment:**
* **Windows:**
```bash
python -m venv venv
venv\Scripts\activate

```


* **macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate

```




3. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


4. **Configure Environment Variables:**
Create a `.env` file in the root directory and add your API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here

```


5. **Run the Application:**
```bash
python main.py

```



---

## 🛠️ Usage & Workflow

When executed, the system runs through two phases:

1. **Automated Verification Test Suite:** Runs predefined edge-case tests covering multi-table JOINs, missing schema attributes, and blocked destructive queries.
2. **Interactive Live Terminal Session:** Accepts custom user prompts in real time.

### Example Prompts to Try:

* **Read Query (Aggregations & Joins):**
> *"Find the total sales amount and order count for each region in 2025."*


* **Write Query (Requires User Confirmation):**
> *"Add a new customer named Ellen Ripley with email ellen@example.com from region West."*


* **Blocked Destructive Query:**
> *"Delete all records from customers."*


* **Missing Schema Entity:**
> *"Show me employee salary details and department names."*



---

## 🛡️ Security & Guardrails

| Condition | Action Taken |
| --- | --- |
| **`SELECT` Query** | Formats syntax $\rightarrow$ Executes against SQLite $\rightarrow$ Renders result table. |
| **`INSERT / UPDATE / DELETE`** | Prompts user for explicit confirmation (`y/N`) before committing to the DB. |
| **Mass Delete (No `WHERE`)** | Intercepted by system prompt $\rightarrow$ Flagged `is_executable: false` $\rightarrow$ Blocked. |
| **Non-Existent Schema Fields** | Identifies missing fields $\rightarrow$ Explains missing entities $\rightarrow$ Aborts execution. |
