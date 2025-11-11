"""
Management command to create sample data.
Example command following the boilerplate template.
"""
from django.core.management.base import BaseCommand
from typing import Any


class Command(BaseCommand):
    """Command to create sample data for development/testing."""
    
    help = 'Create sample data for the application'
    
    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            '--number',
            type=int,
            default=10,
            help='Number of items to create',
        )
    
    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the command."""
        number = options['number']
        self.stdout.write(
            self.style.SUCCESS(f'Creating {number} sample items...')
        )
        # Add your data creation logic here
        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )

