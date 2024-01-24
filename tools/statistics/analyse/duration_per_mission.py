import matplotlib.pyplot as plt
import numpy as np

from tools.statistics import extract


def analyse(datas: list[dict]):
    durations: dict[str] = {
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
    # NOTE : marqué en rouge la durée d'abandon ?

    for data in datas:
        for survey in data["surveys"].keys():
            # only scan survey mission
            if not survey.startswith("mission-"):
                continue

            durations[survey] += extract.mission_duration.extract(data, survey)

    x = list(durations.keys())
    y = np.array(list(durations.values())) / len(datas)

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Temps moyen passé par test")

    # bar chart
    axes.bar(x, y)
    axes.set_xticks(x)
    axes.set_xticklabels(x, rotation=45)

    plt.show(block=True)
