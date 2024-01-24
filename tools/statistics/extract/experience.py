def extract(data: dict) -> str:
    return next(filter(
        lambda it: it[1]["checked"],
        data["surveys"]["question-experience"]["choices"].items()
    ))[0]
