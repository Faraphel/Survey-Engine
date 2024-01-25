import matplotlib.pyplot as plt

from tools.statistics import extract, ressource


def analyse(datas: list[dict]) -> plt.Figure:
    usages: dict[str, int] = dict.fromkeys(ressource.usage.choices, 0)
    for usage in map(extract.usage.extract, datas):
        usages[usage] += 1

    x = list(usages.keys())
    y = list(usages.values())

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Habitude d'utilisation des personnes sondées")

    # bar chart
    axes.bar(x, y, color=ressource.usage.colors, edgecolor='black')
    axes.set_xticks(x)
    axes.set_xticklabels(ressource.usage.labels)

    return figure
