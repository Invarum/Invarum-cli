# cli/invarum/main.py
import typer
import time
from rich.console import Console
from rich.table import Table
from invarum import config
from invarum.client import InvarumClient

app = typer.Typer(
    name="invarum",
    help="Invarum CLI: Quality Engineering for LLMs",
    add_completion=False,
    no_args_is_help=True
)
console = Console()

@app.command()
def login(
    key: str = typer.Option(..., prompt=True, hide_input=True, help="Your Invarum API Key")
):
    """
    Save your API key to a local configuration file.
    """
    if not key.startswith("inv_sk_"):
        console.print("[red]Error:[/red] Key must start with 'inv_sk_'")
        raise typer.Exit(1)

    config.save_api_key(key)
    console.print(f"[bold green]Success![/bold green] API Key saved to {config.CONFIG_FILE}")

@app.command()
def run(
    prompt: str = typer.Argument(..., help="The prompt to evaluate"),
    task: str = typer.Option("default", "--task", "-t", help="Task type")
):
    """
    Run a prompt through the Invarum engine.
    """
    # 1. Get Auth
    key = config.get_api_key()
    if not key:
        console.print("[red]Error:[/red] Not logged in. Run [bold]invarum login[/bold] first.")
        raise typer.Exit(1)

    client = InvarumClient(key)

    # 2. Submit
    try:
        with console.status("[bold green]Submitting to engine..."):
            run_id = client.submit_run(prompt, task)
        console.print(f"Run ID: [cyan]{run_id}[/cyan]")
    except ValueError as e:
        console.print(f"[red]Auth Error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Connection Error:[/red] {e}")
        raise typer.Exit(1)

    # 3. Poll
    try:
        with console.status("[bold green]Running physics engine (this may take a moment)..."):
            result = client.wait_for_run(run_id)
    except Exception as e:
        console.print(f"[red]Run Failed:[/red] {e}")
        raise typer.Exit(1)

    # 4. Display Results
    
    # Logic: If 'metrics' key exists, use it. Otherwise, assume keys are at the top level (result).
    metrics = result.get("metrics") or result
    
    table = Table(title=f"Run ID: {result.get('run_id')}")
    table.add_column("Metric", style="cyan")
    table.add_column("Score", justify="right")
    
    # Helper to safely format floats, handling None/Null from DB
    def fmt(val):
        try:
            return f"{float(val):.3f}"
        except (ValueError, TypeError):
            return "0.000"

    table.add_row("Alpha (Task)",      fmt(metrics.get('alpha')))
    table.add_row("Beta (Coherence)",  fmt(metrics.get('beta')))
    table.add_row("Gamma (Entropy)",   fmt(metrics.get('gamma')))
    table.add_row("Delta (Efficiency)",fmt(metrics.get('delta')))
    
    console.print(table)
    
    # Logic for Pass/Fail
    # Check 'policy_pass' explicitly. Handle boolean or null.
    pass_status = result.get("policy_pass")
    
    if pass_status is True:
        console.print(f"\n[bold green]PASSED POLICY GATES[/bold green]")
    elif pass_status is False:
        console.print(f"\n[bold red]FAILED POLICY GATES[/bold red]")
    else:
        # Handle cases where it might be null (e.g., still processing or unknown)
        console.print(f"\n[bold yellow]POLICY STATUS UNKNOWN[/bold yellow]")

    # Optional: Print Dashboard Link
    console.print(f"\nView full details: https://app.invarum.com/runs/{run_id}")