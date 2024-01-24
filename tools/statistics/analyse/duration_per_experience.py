import matplotlib.pyplot as plt
import numpy as np

from tools.statistics import extract, ressource


def analyse(datas: list[dict]) -> plt.Figure:
    experience_duration: dict[str, int] = dict.fromkeys(ressource.experience.choices, 0)
    experience_count: dict[str, int] = dict.fromkeys(ressource.experience.choices, 0)

    for data in datas:
        experience = extract.experience.extract(data)
        experience_count[experience] += 1

        for survey, survey_data in data["surveys"].items():
            # only scan survey mission
            if not survey.startswith("mission-"):
                continue

            if extract.mission_completed.extract(data, survey):
                experience_duration[experience] += extract.mission_duration.extract(data, survey)

    x = list(experience_duration.keys())
    y = (
        np.array(list(experience_duration.values()))
        / np.array(list(experience_count.values()))
    )

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Temps moyen passé par expérience")

    # bar chart
    axes.bar(x, y, edgecolor='black')

    return figure
