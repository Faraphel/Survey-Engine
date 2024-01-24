def extract(data: dict, mission: str) -> float:
    return data["surveys"][mission]["event"][-1]["time"]
