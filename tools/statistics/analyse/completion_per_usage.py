import matplotlib.pyplot as plt
import numpy as np

from tools.statistics import extract


def analyse(datas: list[dict]):
    usage_completion: dict[str, int] = {"always": 0, "often": 0, "sometime": 0, "rarely": 0, "never": 0}
    usage_count: dict[str, int] = {"always": 0, "often": 0, "sometime": 0, "rarely": 0, "never": 0}

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
    axes.set_title("Nombre moyen de mission complété par niveau")

    # bar chart
    axes.bar(x, y)

    plt.show(block=True)
