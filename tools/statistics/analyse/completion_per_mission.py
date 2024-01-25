import matplotlib.pyplot as plt

from tools.statistics import extract, ressource


def analyse(datas: list[dict]) -> plt.Figure:
    completions: dict[str] = dict.fromkeys(ressource.mission.choices, 0)

    # TODO : couleur par mission

    for data in datas:
        for survey in data["surveys"].keys():
            # only scan survey mission
            if not survey.startswith("mission-"):
                continue

            if extract.mission_completed.extract(data, survey):
                completions[survey] += 1

    x = list(completions.keys())
    y = list(completions.values())

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Nombre de mission total complété")

    # bar chart
    axes.bar(x, y, color=ressource.mission.colors, edgecolor='black')
    axes.set_xlabel("Mission")
    axes.set_ylabel("Complétion")
    axes.set_xticks(x)
    axes.set_xticklabels(ressource.mission.labels, rotation=45, ha="right")
    figure.tight_layout()

    return figure
