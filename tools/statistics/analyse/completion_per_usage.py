import matplotlib.pyplot as plt
import numpy as np

from tools.statistics import extract, ressource


def analyse(datas: list[dict]) -> plt.Figure:
    usage_completion: dict[str, int] = dict.fromkeys(ressource.usage.choices, 0)
    usage_count: dict[str, int] = dict.fromkeys(ressource.usage.choices, 0)

    for data in datas:
        usage = next(filter(
            lambda it: it[1]["checked"],
            data["surveys"]["question-usage-steam"]["choices"].items()
        ))[0]

        usage_count[usage] += 1

        for survey in data["surveys"].keys():
            # only scan survey mission
            if not survey.startswith("mission-"):
                continue

            if extract.mission_completed.extract(data, survey):
                usage_completion[usage] += 1

    x = list(usage_completion.keys())
    y = (
        np.array(list(usage_completion.values()))
        / np.array(list(usage_count.values()))
    )

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Nombre moyen de mission complété par habitude d'utilisation")

    # bar chart
    axes.bar(x, y, color=ressource.usage.colors, edgecolor='black')
    axes.set_xticks(x)
    axes.set_xticklabels(ressource.usage.labels)
    axes.set_xlabel("Usage")
    axes.set_ylabel("Complétion")

    return figure
