import matplotlib.pyplot as plt
import numpy as np

from tools.statistics import extract


def analyse(datas: list[dict]) -> plt.Figure:
    x = list(map(extract.age.extract, datas))

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Nombre de personne par âge")

    # bar chart
    bins = np.arange(min(x), max(x), 1)
    axes.hist(x, bins=bins, edgecolor='black')

    return figure
