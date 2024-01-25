from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

from tools.statistics import extract


def analyse(datas: list[dict]) -> plt.Figure:
    ages_completion: dict[int, int] = defaultdict(lambda: 0)
    ages_count: dict[int, int] = defaultdict(lambda: 0)

    for data in datas:
        age = extract.age.extract(data)
        ages_count[age] += 1

        for survey, survey_data in data["surveys"].items():
            # only scan survey mission
            if not survey.startswith("mission-"):
                continue

            if extract.mission_completed.extract(data, survey):
                ages_completion[age] += 1

    x = list(ages_completion.keys())
    y = (
        np.array(list(ages_completion.values()))
        / np.array(list(ages_count.values()))
    )

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Nombre moyen de mission complété par âge")

    # bar chart
    bins = np.arange(min(x), max(x), 1)
    axes.hist(x, bins, weights=y, edgecolor="black")
    axes.set_xlabel("Âge")
    axes.set_ylabel("Complétion")

    return figure
