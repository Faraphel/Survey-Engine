def extract(data: dict) -> str:
    return next(filter(
        lambda it: it[1]["checked"],
        data["surveys"]["question-usage-steam"]["choices"].items()
    ))[0]
