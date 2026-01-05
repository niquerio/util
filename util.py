import typer
from rich.console import Console
from rich.table import Table
import subprocess
import json
import yaml
from datetime import datetime

with open("config.yaml", "r") as file:
  config = yaml.safe_load(file)

console = Console()
def main():
    repos = [ ]

    for repo in config["repos"]:
        command = ["gh", "release", "list", "-R", repo, "--limit", "1",  "--json",  "publishedAt"]
        result = subprocess.run(command, capture_output=True)
        date = datetime.fromisoformat(json.loads(result.stdout)[0]["publishedAt"])
        repos.append({"date": date, "name": repo})

    by_date = sorted(repos, key=lambda repo: repo["date"])
    table = Table("Repo", "Latest Release")
    for repo in by_date:
        table.add_row(repo["name"], datetime.strftime(repo["date"], "%d %b %Y"))
        
    console.print(table)
    
    


if __name__ == "__main__":
    typer.run(main)
