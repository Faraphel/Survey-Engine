from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

from tools.statistics import extract


def analyse(datas: list[dict]) -> plt.Figure:
    languages_completion: dict[str, int] = defaultdict(lambda: 0)
    languages_count: dict[str, int] = defaultdict(lambda: 0)

    for data in datas:
        language = extract.language.extract(data)
        languages_count[language] += 1

        for survey, survey_data in data["surveys"].items():
            # only scan survey mission
            if not survey.startswith("mission-"):
                continue

            if extract.mission_completed.extract(data, survey):
                languages_completion[language] += 1

    x = list(languages_completion.keys())
    y = (
        np.array(list(languages_completion.values()))
        / np.array(list(languages_count.values()))
    )

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Nombre moyen de mission complété par langue")

    # bar chart
    axes.bar(x, y, edgecolor='black')

    return figure
