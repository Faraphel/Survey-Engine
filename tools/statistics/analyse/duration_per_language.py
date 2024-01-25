import matplotlib.pyplot as plt
import numpy as np

from tools.statistics import extract, ressource


def analyse(datas: list[dict]) -> plt.Figure:
    languages_duration: dict[str, int] = dict.fromkeys(ressource.language.choices, 0)
    languages_count: dict[str, int] = dict.fromkeys(ressource.language.choices, 0)

    for data in datas:
        language = extract.language.extract(data)
        languages_count[language] += 1

        for survey in data["surveys"].keys():
            # only scan survey mission
            if not survey.startswith("mission-"):
                continue

            languages_duration[language] += extract.mission_duration.extract(data, survey)

    x = list(languages_duration.keys())
    y = (
        np.array(list(languages_duration.values()))
        / np.array(list(languages_count.values()))
    )

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Temps moyen passé par langue")

    # bar chart
    axes.bar(x, y, color=ressource.language.colors, edgecolor='black')
    axes.set_xticks(x)
    axes.set_xticklabels(ressource.language.labels)
    axes.set_xlabel("Langue")
    axes.set_ylabel("Durée")

    return figure
