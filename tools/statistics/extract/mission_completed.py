def extract(data: dict, mission: str) -> bool:
    events = data["surveys"][mission]["event"]

    try:
        checks = next(filter(lambda event: event["type"] == "check", events))
    except StopIteration:
        return False
    else:
        return True
