import os
import sys
from unipath import Path

p = Path("/home/ZAR/is2_git/is2_git/")
sys.path = [p] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'is2.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.contrib.auth.management.commands import changepassword
from django.core import management

# Run the syncdb
management.call_command('syncdb', interactive=False)

# Create the super user and sets his password.
management.call_command('createsuperuser', interactive=False, username="admin", email="admin@zarpm.com")
command = changepassword.Command()
command._get_pass = lambda *args: 'admin'
command.execute("admin")