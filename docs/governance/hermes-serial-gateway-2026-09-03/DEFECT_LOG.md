# Defect Log

After one-off CLI import, commands placed after `docker compose run` in a script piped through SSH did not execute because Compose consumed the remaining standard input. This left the workflow temporarily deactivated.

Containment and repair: production version was published in a separate offline command, n8n was started separately, and GET/POST registration plus Facebook challenge were verified. Root cause is documented: future one-off Compose commands in piped scripts must use `</dev/null` or separate SSH calls.

Final production state is healthy and registered.
