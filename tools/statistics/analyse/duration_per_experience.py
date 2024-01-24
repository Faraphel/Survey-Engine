import matplotlib.pyplot as plt
import numpy as np

from tools.statistics import extract


def analyse(datas: list[dict]):
    experience_duration: dict[str, int] = {"yes": 0, "mixed": 0, "no": 0}
    experience_count: dict[str, int] = {"yes": 0, "mixed": 0, "no": 0}

    for data in datas:
        experience = extract.experience.extract(data)
        experience_count[experience] += 1

        for survey, survey_data in data["surveys"].items():
            # only scan survey mission
            if not survey.startswith("mission-"):
                continue

            if extract.mission_completed.extract(data, survey):
                experience_duration[experience] += extract.mission_duration.extract(data, survey)

    ages_x = list(experience_duration.keys())
    ages_y = (
        np.array(list(experience_duration.values()))
        / np.array(list(experience_count.values()))
    )

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Temps moyen passé par expérience")

    # bar chart
    axes.bar(ages_x, ages_y)

    plt.show(block=True)
