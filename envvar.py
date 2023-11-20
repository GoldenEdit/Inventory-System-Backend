from dotenv import dotenv_values
import subprocess

# Load .env file
config = dotenv_values(".env")

# Convert to Heroku config:set format
config_str = " ".join([f"{key}={value}" for key, value in config.items()])

# Set Heroku config vars
subprocess.run(f"heroku config:set {config_str} --app inventory-system-backend", shell=True)
