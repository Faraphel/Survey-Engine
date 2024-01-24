import matplotlib.pyplot as plt

from tools.statistics import extract


def analyse(datas: list[dict]):
    missions = {
        "mission-language": 0,
        "mission-price": 0,
        "mission-community-hub": 0,
        "mission-game-page": 0,
        "mission-game-dlc": 0,
        "mission-actuality-new": 0,
        "mission-profile": 0,
        "mission-game-discussion": 0,
        "mission-gift-card": 0,
        "mission-workshop": 0
    }

    for data in datas:
        missions[extract.hardest_mission.extract(data)] += 1

    x = list(missions.keys())
    y = list(missions.values())

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Mission la plus difficile des personnes sondées")

    # bar chart
    axes.bar(x, y)
    axes.set_xticks(x)
    axes.set_xticklabels(x, rotation=45)

    plt.show(block=True)
