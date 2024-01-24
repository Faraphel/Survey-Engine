import matplotlib.pyplot as plt

from tools.statistics import extract, ressource


def analyse(datas: list[dict]) -> plt.Figure:
    missions = dict.fromkeys(ressource.mission.choices, 0)

    for data in datas:
        missions[extract.hardest_mission.extract(data)] += 1

    x = list(missions.keys())
    y = list(missions.values())

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Mission la plus difficile des personnes sondées")

    # bar chart
    axes.bar(x, y, edgecolor='black')
    axes.set_xticks(x)
    axes.set_xticklabels(x, rotation=45)

    return figure
