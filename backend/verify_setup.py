import sys
import os

# Add local directory to path
sys.path.append(os.getcwd())

print("Attempting to import app.main...")
try:
    from app.main import app
    print("SUCCESS: app.main imported successfully.")
except Exception as e:
    print(f"ERROR: Failed to import app.main: {e}")
    sys.exit(1)

print("Checking GPIO Mock/Real...")
try:
    from app.iot.gpio_controller import gpio_manager
    print(f"SUCCESS: GPIO Controller loaded. Is Mock: {not getattr(gpio_manager, 'setup_board', None)}") 
    # Logic above is just a print, real check is if it crashed
except Exception as e:
    print(f"ERROR: Failed to load GPIO Controller: {e}")
    sys.exit(1)

print("Verification complete.")
