import matplotlib.pyplot as plt

from tools.statistics import extract


def analyse(datas: list[dict]):
    usage_data = list(map(extract.usage.extract, datas))

    usages: dict[str, int] = {"always": 0, "often": 0, "sometime": 0, "rarely": 0, "never": 0}
    for usage in usage_data:
        usages[usage] += 1

    usages_x = list(usages.keys())
    usages_y = list(usages.values())

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Expérience des personnes sondées")

    # bar chart
    axes.bar(usages_x, usages_y)

    plt.show(block=True)
