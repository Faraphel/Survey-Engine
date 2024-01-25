import matplotlib.pyplot as plt
import numpy as np

from tools.statistics import extract, ressource


def analyse(datas: list[dict]) -> plt.Figure:
    x = list(map(extract.age.extract, datas))

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Âge des personnes sondées")

    # bar chart
    bins = np.arange(min(x), max(x), 1)
    axes.hist(x, bins=bins, edgecolor='black')
    axes.set_xlabel("Âge")
    axes.set_ylabel("Quantité")

    return figure
