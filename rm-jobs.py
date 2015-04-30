#!/usr/bin/python
import os, sys, time
import settings

# Change this to make the remove time go up (month, day, etc.)
REMOVE_TIME = 7 * 86400

now = time.time()
query_dirs = [ name for name in os.listdir(settings.QUERY_FOLDER) if os.path.isdir(os.path.join(settings.QUERY_FOLDER, name)) ]
count = 0

for f in query_dirs:
    if os.stat(os.path.join(settings.QUERY_FOLDER, f)).st_mtime < now - REMOVE_TIME:
        count += 1
        shutil.rmtree(os.path.join(settings.QUERY_FOLDER, name))

sys.stdout.write('Removed ' + str(count) + ' queries\n')
sys.stdout.flush()

