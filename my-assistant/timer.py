import threading


def start_timer(seconds, label="Timer"):
    def ring():
        print(f"\n⏰ {label} is up!")

    threading.Timer(seconds, ring).start()
    return f"{label} set for {seconds} seconds."
