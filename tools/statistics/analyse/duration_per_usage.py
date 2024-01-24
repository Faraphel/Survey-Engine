import matplotlib.pyplot as plt
import numpy as np

from tools.statistics import extract


def analyse(datas: list[dict]):
    usage_completion: dict[str, int] = {"always": 0, "often": 0, "sometime": 0, "rarely": 0, "never": 0}
    usage_count: dict[str, int] = {"always": 0, "often": 0, "sometime": 0, "rarely": 0, "never": 0}

    # TODO: faire des tranches d'âges ?

    for data in datas:
        usage = extract.usage.extract(data)
        usage_count[usage] += 1

        for survey in data["surveys"].keys():
            # only scan survey mission
            if not survey.startswith("mission-"):
                continue

            usage_completion[usage] += extract.mission_duration.extract(data, survey)

    x = list(usage_completion.keys())
    y = (
        np.array(list(usage_completion.values()))
        / np.array(list(usage_count.values()))
    )

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Temps moyen passé par niveau")

    # bar chart
    axes.bar(x, y)

    plt.show(block=True)
