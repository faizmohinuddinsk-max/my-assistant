APP_PACKAGES = {
    "camera": "com.android.camera",
    "whatsapp": "com.whatsapp",
    "music": "com.android.music",
    "browser": "com.android.chrome",
}


def open_app(name):
    name = name.lower()
    if name not in APP_PACKAGES:
        return f"I don't know how to open {name}."

    print(f"[stub] Opening {name}...")

    return f"Opening {name}."
