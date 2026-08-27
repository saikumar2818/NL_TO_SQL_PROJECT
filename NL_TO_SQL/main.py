import os
import json
import sqlite3
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Rich UI Components
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.prompt import Prompt

from db_setup import init_in_memory_db

# Initialize Console
console = Console()

# 1. Environment & Database Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    console.print("[bold red]Error:[/bold red] GEMINI_API_KEY not set in .env file.", style="bold red")
    exit(1)

client = genai.Client(api_key=api_key)
db_conn = init_in_memory_db()

if not os.path.exists("system_prompt.txt"):
    console.print("[bold red]Error:[/bold red] system_prompt.txt file missing.", style="bold red")
    exit(1)

with open("system_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()


def convert_nl_to_sql(user_query: str) -> dict:
    """Translates user query using Gemini API with zero temperature."""
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.0,
        response_mime_type="application/json"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_query,
            config=config
        )
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {
            "is_executable": False,
            "operation_type": "READ",
            "clarification_needed": "Failed to parse JSON response from LLM."
        }
    except Exception as e:
        return {
            "is_executable": False,
            "operation_type": "READ",
            "clarification_needed": f"API Error: {str(e)}"
        }


def execute_generated_sql(sql_query: str, operation_type: str):
    """Executes SQL queries with safety confirmations for WRITE operations."""
    try:
        cursor = db_conn.cursor()
        
        # Human-in-the-Loop Confirmation for WRITE
        if operation_type == "WRITE":
            console.print("\n[bold yellow]⚠️ WRITE OPERATION DETECTED![/bold yellow]")
            confirm = Prompt.ask("Do you want to commit these changes to the database?", choices=["y", "n"], default="n")
            if confirm.lower() != 'y':
                console.print("[bold red]Transaction aborted by user.[/bold red]")
                return

        cursor.execute(sql_query)
        db_conn.commit()

        if operation_type == "WRITE":
            console.print(f"[bold green]✓ Database modified successfully! Rows affected: {cursor.rowcount}[/bold green]")
        else:
            rows = cursor.fetchall()
            if not rows:
                console.print("[bold yellow]Query executed successfully, but returned 0 rows.[/bold yellow]")
                return

            columns = [desc[0] for desc in cursor.description]
            table = Table(title="[bold green]Execution Results[/bold green]", show_header=True, header_style="bold cyan")
            
            for col in columns:
                table.add_column(col)
            for row in rows:
                table.add_row(*[str(val) for val in row])
                
            console.print(table)

    except sqlite3.Error as e:
        console.print(f"[bold red]Database Execution Error:[/bold red] {e}")


def display_pipeline_output(query: str, result: dict):
    """Renders formatted cards, syntax highlights, and UI elements."""
    console.print(f"\n[bold magenta]User Query:[/bold magenta] [italic]\"{query}\"[/italic]")

    if result.get("is_executable"):
        sql = result.get("sql_query", "")
        op_type = result.get("operation_type", "READ")
        
        title_style = "bold green" if op_type == "READ" else "bold yellow"
        syntax = Syntax(sql, "sql", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title=f"[{title_style}]✓ Validated {op_type} Query[/{title_style}]", border_style="green" if op_type == "READ" else "yellow"))

        if result.get("assumptions"):
            console.print("[dim]Assumptions Made:[/dim]")
            for a in result["assumptions"]:
                console.print(f"  • [cyan]{a}[/cyan]")

        execute_generated_sql(sql, op_type)
    else:
        msg = ""
        if result.get("missing_fields"):
            msg += f"[bold red]Missing Schema Entities:[/bold red] {', '.join(result['missing_fields'])}\n"
        if result.get("clarification_needed"):
            msg += f"[bold yellow]Blocked Reason:[/bold yellow] {result['clarification_needed']}"

        console.print(Panel(msg, title="[bold red]✗ Execution Blocked[/bold red]", border_style="red"))


def main():
    console.print(Panel.fit(
        "[bold cyan]Transactional NL-to-SQL Prompt Engineering Engine[/bold cyan]\n"
        "[dim]Powered by Gemini 2.5 Flash, Human-in-the-Loop Guards & SQLite[/dim]",
        border_style="cyan"
    ))

    test_suite = [
        "Find the total sales amount and order count for each region in 2025.",
        "Add a new customer named Ellen Ripley with email ellen@example.com from region West.",
        "Delete all records from customers.",
        "Show me employee salary details."
    ]

    console.print("\n[bold yellow]--- Running Automated Test Matrix ---[/bold yellow]")
    for query in test_suite:
        with console.status("[bold green]Processing via LLM...[/bold green]", spinner="dots"):
            res = convert_nl_to_sql(query)
        display_pipeline_output(query, res)
        console.print("[dim]" + "─" * 60 + "[/dim]")

    console.print("\n[bold cyan]--- Interactive Live Terminal ---[/bold cyan]")
    while True:
        user_input = Prompt.ask("\n[bold white]Enter Natural Language Question[/bold white] (type 'exit' to quit)")
        if user_input.lower() in ['exit', 'quit', 'q']:
            console.print("[bold cyan]Session closed.[/bold cyan]")
            break

        with console.status("[bold green]Generating Query...[/bold green]", spinner="dots"):
            res = convert_nl_to_sql(user_input)
        display_pipeline_output(user_input, res)


if __name__ == "__main__":
    main()