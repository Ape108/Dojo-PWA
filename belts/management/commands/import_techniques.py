import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from belts.models import Belt, Technique
import os

class Command(BaseCommand):
    help = 'Imports techniques from a semicolon-delimited TXT file for a specific belt.'

    def add_arguments(self, parser):
        parser.add_argument('belt_name', type=str, help='The exact name of the belt (must exist in DB).')
        parser.add_argument('file_path', type=str, help='The path to the source TXT file.')

    def handle(self, *args, **options):
        belt_name = options['belt_name']
        file_path = options['file_path']

        try:
            belt = Belt.objects.get(name=belt_name)
        except Belt.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Belt "{belt_name}" not found. Please create it via the admin panel first.'))
            return
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found at: {file_path}'))
            return
        
        self.stdout.write(f'Starting import for belt: {belt.name}')

        with open(file_path, mode='r', encoding='utf-8') as f:
            # Use csv.reader to handle the specified format 
            # (semicolon delimited, quoted fields)
            reader = csv.reader(f, delimiter=';', quotechar='"')
            for index, row in enumerate(reader):
                if len(row) != 2:
                    self.stdout.write(self.style.WARNING(f'Skipping malformed row {index + 1}: {row}'))
                    continue

                technique_name = row[0].strip()
                description = row[1].strip()
                order_in_belt = index + 1

                # Autmoatically generate the expected video file path based on the technique name.
                # E.g., "Kimono Grab" -> "videos/kimono-grab.mp4"
                sanitized_name = slugify(technique_name)
                video_file_path = f'videos/{sanitized_name}.mp4'

                # Use update_or_create to avoid duplicates and allow re-running the script
                technique, created = Technique.objects.update_or_create(
                    belt=belt,
                    name=technique_name,
                    defaults={
                        'description': description,
                        'order_in_belt': order_in_belt,
                        'video_file': video_file_path # Assign the expected path
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'[CREATED] {technique_name}'))
                else:
                    self.stdout.write(self.style.NOTICE(f'[UPDATED] {technique_name}'))

        self.stdout.write(self.style.SUCCESS('Import complete. Remember to upload the corresponding video files to Google Cloud Storage.'))