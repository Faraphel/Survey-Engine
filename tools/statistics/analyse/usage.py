import matplotlib.pyplot as plt

from tools.statistics import extract, ressource


def analyse(datas: list[dict]) -> plt.Figure:
    usage_data = list(map(extract.usage.extract, datas))

    usages: dict[str, int] = dict.fromkeys(ressource.usage.choices, 0)
    for usage in usage_data:
        usages[usage] += 1

    x = list(usages.keys())
    y = list(usages.values())

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Expérience antérieure des personnes sondées")

    # bar chart
    axes.bar(x, y, edgecolor='black')

    return figure
