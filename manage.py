#!/usr/bin/env python
import click
import uvicorn
import subprocess
import os
import sys
from pathlib import Path
from typing import List

@click.group()
def cli():
    pass

@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to bind.')
@click.option('--port', default=8000, help='Port to bind.')
def runserver(host: str, port: int):
    """Run the FastAPI server."""
    uvicorn.run("main:app", host=host, port=port, reload=True)

@cli.command()
@click.argument('app_name')
def createapp(app_name: str):
    """Create a new app with the given name."""
    app_dir = Path(f"apps/{app_name}")
    app_dir.mkdir(parents=True, exist_ok=True)
    
    # Create app files
    (app_dir / "__init__.py").touch()
    (app_dir / "models.py").write_text("from sqlalchemy import Column, Integer, String\nfrom core.database import Base\n\n# Define your models here")
    (app_dir / "schemas.py").write_text("from pydantic import BaseModel\n\n# Define your schemas here")
    (app_dir / "routes.py").write_text("from fastapi import APIRouter\n\nrouter = APIRouter()\n\n# Define your routes here")
    (app_dir / "services.py").write_text("# Define your services here")
    
    # Create tests directory
    tests_dir = app_dir / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "__init__.py").touch()
    (tests_dir / "test_models.py").touch()
    (tests_dir / "test_routes.py").touch()
    (tests_dir / "test_services.py").touch()
    
    # Update INSTALLED_APPS in config
    config_path = Path("core/config.py")
    with config_path.open("r") as f:
        config_content = f.read()
    
    if f'"{app_name}"' not in config_content:
        config_content = config_content.replace(
            "INSTALLED_APPS: List[str] = [",
            f'INSTALLED_APPS: List[str] = ["{app_name}", '
        )
        with config_path.open("w") as f:
            f.write(config_content)
    
    click.echo(f"Created app '{app_name}' successfully and added it to INSTALLED_APPS.")

@cli.command()
def makemigrations():
    """Generate new migration."""
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", "New migration"])

@cli.command()
def migrate():
    """Apply migrations."""
    subprocess.run(["alembic", "upgrade", "head"])

@cli.command()
def test():
    """Run tests."""
    subprocess.run(["pytest"])

@cli.command()
def shell():
    """Run an interactive Python shell."""
    os.environ['PYTHONSTARTUP'] = 'core/shell_startup.py'
    subprocess.run(["python"])

@cli.command()
@click.argument('app_name')
def deleteapp(app_name: str):
    """Delete an existing app."""
    app_dir = Path(f"apps/{app_name}")
    if app_dir.exists():
        subprocess.run(["rm", "-rf", str(app_dir)])
        
        # Update INSTALLED_APPS in config
        config_path = Path("core/config.py")
        with config_path.open("r") as f:
            config_content = f.read()
        
        config_content = config_content.replace(f'"{app_name}", ', "")
        with config_path.open("w") as f:
            f.write(config_content)
        
        click.echo(f"Deleted app '{app_name}' successfully and removed it from INSTALLED_APPS.")
    else:
        click.echo(f"App '{app_name}' does not exist.")

@cli.command()
def listapps():
    """List all installed apps."""
    from core.config import settings
    click.echo("Installed apps:")
    for app in settings.INSTALLED_APPS:
        click.echo(f"- {app}")

if __name__ == "__main__":
    cli()

