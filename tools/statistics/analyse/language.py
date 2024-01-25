import matplotlib.pyplot as plt

from tools.statistics import extract, ressource


def analyse(datas: list[dict]) -> plt.Figure:
    languages = dict.fromkeys(ressource.language.choices, 0)
    for language in map(extract.language.extract, datas):
        languages[language] += 1

    x = list(languages.keys())
    y = list(languages.values())

    # prepare plotting
    figure: plt.Figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Langue des personnes sondées")

    # bar chart
    axes.bar(x, y, color=ressource.language.colors, edgecolor='black')
    axes.set_xticks(x)
    axes.set_xticklabels(ressource.language.labels)
    axes.set_xlabel("Langue")
    axes.set_ylabel("Quantité")

    return figure
