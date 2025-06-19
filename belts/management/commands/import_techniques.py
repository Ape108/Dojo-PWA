# belts/management/commands/import_techniques.py

import csv
import os
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from belts.models import Belt, Technique

class Command(BaseCommand):
    help = 'Imports techniques from a semicolon-delimited TXT file for a specific belt. Correctly handles blank lines.'

    def add_arguments(self, parser):
        parser.add_argument('belt_name', type=str, help='The exact name of the belt (must exist in DB).')
        parser.add_argument('file_path', type=str, help='The path to the source TXT file.')

    def handle(self, *args, **options):
        belt_name = options['belt_name']
        file_path = options['file_path']

        try:
            belt = Belt.objects.get(name__iexact=belt_name)
        except Belt.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Belt "{belt_name}" not found. Please create it via the admin panel first.'))
            return

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found at: {file_path}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Starting import for belt: {belt.name}'))
        
        # This counter will only increment when we find a valid technique.
        technique_order_counter = 0

        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';', quotechar='"')
            for row in reader:
                # 1. Skip completely blank lines
                if not row:
                    continue

                # 2. Check for malformed rows (not blank, but not two columns)
                if len(row) != 2:
                    self.stdout.write(self.style.WARNING(f'Skipping malformed row: {row}'))
                    continue

                # If the row is valid, increment our counter
                technique_order_counter += 1
                
                technique_name = row[0].strip()
                description = row[1].strip()
                
                sanitized_name = slugify(technique_name)
                video_file_path = f'videos/{sanitized_name}.mp4'

                technique, created = Technique.objects.update_or_create(
                    belt=belt,
                    name=technique_name,
                    defaults={
                        'description': description,
                        'order_in_belt': technique_order_counter, # Use our reliable counter
                        'video_file': video_file_path
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'  [CREATED] {technique.name}'))
                else:
                    self.stdout.write(self.style.NOTICE(f'  [UPDATED] {technique.name}'))

        self.stdout.write(self.style.SUCCESS('Import complete!'))
