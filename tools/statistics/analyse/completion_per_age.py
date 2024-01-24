from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

from tools.statistics import extract


def analyse(datas: list[dict]):
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

    ages_x = list(ages_completion.keys())
    ages_y = (
        np.array(list(ages_completion.values()))
        / np.array(list(ages_count.values()))
    )

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Nombre moyen de mission complété par âge")

    # bar chart
    axes.bar(ages_x, ages_y)

    plt.show(block=True)
