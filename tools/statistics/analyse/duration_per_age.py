from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

from tools.statistics import extract


def analyse(datas: list[dict]) -> plt.Figure:
    ages_duration: dict[int, int] = defaultdict(lambda: 0)
    ages_count: dict[int, int] = defaultdict(lambda: 0)

    # TODO: affichage en minutes ?

    for data in datas:
        age = extract.age.extract(data)
        ages_count[age] += 1

        for survey in data["surveys"].keys():
            # only scan survey mission
            if not survey.startswith("mission-"):
                continue

            ages_duration[age] += extract.mission_duration.extract(data, survey)

    x = list(ages_duration.keys())
    y = (
        np.array(list(ages_duration.values()))
        / np.array(list(ages_count.values()))
    )

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Temps moyen passé par âge")

    # bar chart
    bins = np.arange(min(x), max(x), 1)
    axes.hist(x, bins, weights=y, edgecolor="black")

    return figure
