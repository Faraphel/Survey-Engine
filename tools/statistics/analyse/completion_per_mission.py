import matplotlib.pyplot as plt

from tools.statistics import extract


def analyse(datas: list[dict]):
    completions: dict[str] = {
        "mission-language": 0,
        "mission-price": 0,
        "mission-community-hub": 0,
        "mission-game-page": 0,
        "mission-game-dlc": 0,
        "mission-actuality-new": 0,
        "mission-profile": 0,
        "mission-game-discussion": 0,
        "mission-gift-card": 0,
        "mission-workshop": 0,
    }

    # NOTE : séparé avant / après grosse mise à jour pour carte cadeau ?

    for data in datas:
        for survey in data["surveys"].keys():
            # only scan survey mission
            if not survey.startswith("mission-"):
                continue

            if extract.mission_completed.extract(data, survey):
                completions[survey] += 1

    x = list(completions.keys())
    y = list(completions.values())

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Nombre de personne ayant réussi par mission")

    # bar chart
    axes.bar(x, y)
    axes.set_xticks(x)
    axes.set_xticklabels(x, rotation=45)

    plt.show(block=True)
