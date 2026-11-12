import json
from pathlib import Path
from django.core.management.base import BaseCommand
from portfolio.models import Project
class Command(BaseCommand):
 help='Add initial projects without overwriting admin edits.'
 def handle(self,*args,**options):
  rows=json.loads((Path(__file__).resolve().parents[2]/'seed_projects.json').read_text())
  added=0
  for row in rows:
   slug=row.pop('slug')
   _,created=Project.objects.get_or_create(slug=slug,defaults=row)
   added+=created
  self.stdout.write(self.style.SUCCESS(f'Added {added} projects; existing projects preserved.'))
