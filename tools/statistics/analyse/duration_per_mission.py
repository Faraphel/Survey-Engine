import matplotlib.pyplot as plt
import numpy as np

from tools.statistics import extract, ressource


def analyse(datas: list[dict]) -> plt.Figure:
    durations: dict[str] = dict.fromkeys(ressource.mission.choices, 0)

    # TODO : marqué en rouge la durée d'abandon ?
    # TODO : couleur par mission

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
    axes.set_title("Temps total passé par mission")

    # bar chart
    axes.bar(x, y, color=ressource.mission.colors, edgecolor='black')
    axes.set_xlabel("Mission")
    axes.set_ylabel("Durée")
    axes.set_xticks(x)
    axes.set_xticklabels(ressource.mission.labels, rotation=45, ha="right")
    figure.tight_layout()

    return figure
