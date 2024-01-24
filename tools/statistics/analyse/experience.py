from collections import Counter

import matplotlib.pyplot as plt

from tools.statistics import extract


def analyse(datas: list[dict]):
    experiences: dict[str, int] = {"yes": 0, "mixed": 0, "no": 0}
    for data in datas:
        experience = extract.experience.extract(data)
        experiences[experience] += 1

    counter = Counter(experiences)
    x = list(counter.keys())
    y = list(counter.values())

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Nombre de personne par expérience")

    # bar chart
    axes.bar(x, y)

    plt.show(block=True)
