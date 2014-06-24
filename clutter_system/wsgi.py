"""
WSGI config for clutter_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
#import site

#Add virtual environment
#site.addsitedir('/var/venv/main_site/lib/python2.7/site-packages')

# Configure PYTHONPATH
paths = ["/home/cmaclell/clutter/clutter_system/",
         "/home/cmaclell/clutter/clutter/",
         "/home/cmaclell/clutter/"]
       #"/var/venv/main_site/lib/python2.7/site-packages"]

for path in paths:
    if path not in sys.path:
            sys.path.append(path)

#print(sys.path)

# To fix multiple django instances on same domain.
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clutter.server-settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "clutter.server-settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

