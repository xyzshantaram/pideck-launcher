import random


def generate_username():
    adjectives = [
        "Brave",
        "Clever",
        "Curious",
        "Energetic",
        "Friendly",
        "Gentle",
        "Happy",
        "Lucky",
        "Patient",
        "Quiet",
        "Silly",
        "Smart",
        "Strong",
        "Wise",
        "Zealous",
    ]
    animals = [
        "Lion",
        "Tiger",
        "Bear",
        "Wolf",
        "Fox",
        "Eagle",
        "Shark",
        "Snake",
        "Rabbit",
        "Hawk",
        "Dolphin",
        "Dragon",
        "Elephant",
        "Giraffe",
        "Kangaroo",
    ]
    numbers = (
        [str(i).zfill(3) for i in range(101, 1000)]
        + ["000"]
        + [str(i).zfill(3) for i in range(111, 1000, 111)]
    )

    adjective = random.choice(adjectives)
    animal = random.choice(animals)
    number = random.choice(numbers)

    return f"{adjective}{animal}{number}"
