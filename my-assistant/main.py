import memory
import brain
import calls

data = memory.load()
pending = None

print("Arthur is ready. Type 'quit' to exit.")

while True:
    text = input("> ").strip()
    if text.lower() in ("quit", "exit"):
        print("Goodbye.")
        break
    if not text:
        continue

    reply, pending = brain.handle(text, data, pending)
    print(reply)
    memory.save(data)

    if pending is None and reply.startswith("Calling"):
        name = reply.split(" ")[1].rstrip(".")
        number = data["contacts"].get(name, "")
        calls.place_call(name, number)
