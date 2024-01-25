from collections import Counter

import matplotlib.pyplot as plt

from tools.statistics import extract, ressource


def analyse(datas: list[dict]) -> plt.Figure:
    experiences: dict[str, int] = dict.fromkeys(ressource.experience.choices, 0)
    for data in datas:
        experience = extract.experience.extract(data)
        experiences[experience] += 1

    counter = Counter(experiences)
    x = list(counter.keys())
    y = list(counter.values())

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Opinion des personnes sondées")

    # bar chart
    axes.bar(x, y, color=ressource.experience.colors, edgecolor='black')
    axes.set_xticks(x)
    axes.set_xticklabels(ressource.experience.labels)
    axes.set_xlabel("Expérience")
    axes.set_ylabel("Quantité")

    return figure
