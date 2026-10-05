import os
import datetime


def take_photo():
    os.makedirs("photos", exist_ok=True)
    filename = f"photo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    path = os.path.join("photos", filename)

    # --- LAPTOP STUB ---
    # No real camera here, so we can't actually capture anything.
    # Returns None so photo_solver.py knows there's no real image yet.
    print(f"[stub] No laptop camera — would have saved to {path}")
    return None

    # --- PHONE VERSION (uncomment once running in Termux, remove stub above) ---
    # import subprocess
    # subprocess.run(["termux-camera-photo", "-c", "0", path])
    # return path
