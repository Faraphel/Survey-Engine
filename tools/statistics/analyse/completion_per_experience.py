import matplotlib.pyplot as plt
import numpy as np

from tools.statistics import extract, ressource


def analyse(datas: list[dict]) -> plt.Figure:
    experience_completion: dict[str, int] = dict.fromkeys(ressource.experience.choices, 0)
    experience_count: dict[str, int] = dict.fromkeys(ressource.experience.choices, 0)

    for data in datas:
        experience = extract.experience.extract(data)
        experience_count[experience] += 1

        for survey, survey_data in data["surveys"].items():
            # only scan survey mission
            if not survey.startswith("mission-"):
                continue

            if extract.mission_completed.extract(data, survey):
                experience_completion[experience] += 1

    x = list(experience_completion.keys())
    y = (
        np.array(list(experience_completion.values()))
        / np.array(list(experience_count.values()))
    )

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Nombre moyen de mission complété par opinion")

    # bar chart
    axes.bar(x, y, color=ressource.experience.colors, edgecolor='black')
    axes.set_xticks(x)
    axes.set_xticklabels(ressource.experience.labels)
    axes.set_xlabel("Expérience")
    axes.set_ylabel("Complétion")

    return figure
