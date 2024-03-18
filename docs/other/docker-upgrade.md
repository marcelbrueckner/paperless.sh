# Upgrading to a new version for Docker Compose users
This script takes a few steps to help automatically upgrade people using docker compose.  Rather than requiring lots of interactive work on the terminal, this just wraps up a bunch of best practices into one.  NOTE: This removes any unused docker containers at the end of the script.  If that's not something you want, comment that section out.

Otherwise, this script:

1. Runs the built-in backup script
1. Stops the Docker containers using Docker Compose
1. Pulls the new version of the Docker container
1. Restart the container, outputting to a file, and shows it so you can ensure that it's running correctly
1. Waits for user input to confirm if things are working
1. If the user indicates everything is working, proceed to stop and restart the container in daemon mode
1. Runs a Docker system prune to remove older versions of the container
