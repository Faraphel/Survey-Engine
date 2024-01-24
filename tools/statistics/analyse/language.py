from collections import Counter

import matplotlib.pyplot as plt

from tools.statistics import extract


def analyse(datas: list[dict]) -> plt.Figure:
    languages = list(map(extract.language.extract, datas))

    counter = Counter(languages)
    x = list(counter.keys())
    y = list(counter.values())

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Langue des personnes sondées")

    # bar chart
    axes.bar(x, y, edgecolor='black')

    return figure
