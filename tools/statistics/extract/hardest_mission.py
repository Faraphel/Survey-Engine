def extract(data: dict) -> str:
    return next(filter(
        lambda it: it[1]["checked"],
        data["surveys"]["question-hardest-mission"]["choices"].items()
    ))[0]
