#!/usr/bin/env python
import os
import sys
from typing import List

import django
from django.contrib.auth import get_user_model
from django.core.management import call_command, execute_from_command_line

DEFAULT_ENVS = {
    "DJANGO_SETTINGS_MODULE": "PyLudus.settings",
    "SUPER_USERNAME": "admin",
    "SUPER_PASSWORD": "admin",
}

for key, value in DEFAULT_ENVS.items():
    os.environ.setdefault(key, value)


class SiteManager:
    """
    Manages the preparation and serving of the website.

    Handles both development and production environments.

    Usage:
        manage.py run [option]...

    Options:
        --debug    Runs a development server with debug mode enabled.
        --silent   Sets minimal console output.
        --verbose  Sets verbose console output.
    """

    def __init__(self, args: List[str]):
        self.debug = "--debug" in args
        self.silent = "--silent" in args

        if self.silent:
            self.verbosity = 0
        else:
            self.verbosity = 2 if "--verbose" in args else 1

        if self.debug:
            os.environ.setdefault("DEBUG", "true")
            print("Starting in debug mode.")

    @staticmethod
    def create_superuser() -> None:
        """Create a default django admin super user in development environments."""
        print("Creating a superuser.")

        name = os.environ["SUPER_USERNAME"]
        password = os.environ["SUPER_PASSWORD"]
        user = get_user_model()

        # Get or create admin superuser.
        if user.objects.filter(username=name).exists():
            user = user.objects.get(username=name)
            print("Admin superuser already exists.")
        else:
            user = user.objects.create_superuser(name, "", password)
            print("Admin superuser created.")

    def prepare_server(self) -> None:
        """Perform preparation tasks before running the server."""
        django.setup()

        print("Making migrations.")
        call_command("makemigrations", verbosity=self.verbosity)
        print("Applying migrations.")
        call_command("migrate", verbosity=self.verbosity)
        print("Collecting static files.")
        call_command(
            "collectstatic", interactive=False, clear=True, verbosity=self.verbosity
        )

        if self.debug:
            self.create_superuser()

    def run_server(self) -> None:
        """Prepare and run the web server."""
        in_reloader = os.environ.get("RUN_MAIN") == "true"

        # Prevent preparing twice when in dev mode due to reloader
        if not self.debug or in_reloader:
            self.prepare_server()

        print("Starting server.")

        # Run the development server
        call_command("runserver", "0.0.0.0:8000")


def main() -> None:
    """Entry point for Django management script."""
    # Use the custom site manager for launching the server
    if sys.argv[1] == "run":
        SiteManager(sys.argv).run_server()

    # Pass any others directly to standard management commands
    else:
        execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
