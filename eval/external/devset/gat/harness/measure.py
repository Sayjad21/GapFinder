"""devset GAT: run a command, then print its exit code, wall time and peak RSS to stderr (no /usr/bin/time
in python:3.7-slim)."""
import resource
import subprocess
import sys
import time

t = time.time()
rc = subprocess.call(sys.argv[1:])
rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
print(f"exit={rc} wall_s={time.time() - t:.0f} max_rss_kb={rss}", file=sys.stderr)
sys.exit(rc)
