import random


def tell_joke(data):
    if not data["jokes"]:
        return "I don't have any jokes saved."
    return random.choice(data["jokes"])


def tell_fact(data):
    if not data["facts"]:
        return "I don't have any facts saved."
    return random.choice(data["facts"])


def add_joke(data, joke):
    data["jokes"].append(joke)
    return "Joke added."


def add_fact(data, fact):
    data["facts"].append(fact)
    return "Fact added."


def delete_joke(data, index):
    if 0 <= index < len(data["jokes"]):
        data["jokes"].pop(index)
        return "Joke deleted."
    return "Couldn't find that joke."


def delete_fact(data, index):
    if 0 <= index < len(data["facts"]):
        data["facts"].pop(index)
        return "Fact deleted."
    return "Couldn't find that fact."
