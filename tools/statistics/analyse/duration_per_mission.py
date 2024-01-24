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
    axes.set_title("Temps moyen passé par test")

    # bar chart
    axes.bar(x, y, edgecolor='black')
    axes.set_xticks(x)
    axes.set_xticklabels(x, rotation=45)

    return figure
