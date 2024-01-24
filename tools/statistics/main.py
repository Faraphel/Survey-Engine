from pathlib import Path

from tools.statistics.analyse import (age, usage, completion_per_mission, duration_per_mission, completion_per_age,
                                      completion_per_usage, duration_per_age, duration_per_usage,
                                      completion_per_experience, duration_per_experience, experience, hardest_mission,
                                      language, duration_per_language, completion_per_language)

if __name__ == "__main__":
    from source.utils import compress

    # import matplotlib
    # matplotlib.use("pgf")
    # matplotlib.rcParams.update({
    #     "pgf.texsystem": "pdflatex",
    #     'font.family': 'serif',
    #     'font.size': 11,
    #     'text.usetex': True,
    #     'pgf.rcfonts': False,
    # })

    sondage_path = Path(r"./sondage/")
    graph_path = Path(r"./graph/")
    graph_path.mkdir(parents=True, exist_ok=True)

    # read every peoples survey data
    datas_all = [
        compress.uncompress_data(file.read_bytes())  # decompress the data
        for file in sondage_path.rglob("*.rsl")
    ]

    # keep only the datas before the steam new year update
    datas_steam_version_1 = list(filter(lambda data: data["time"] < 1704409200, datas_all))

    # keep only the datas after the steam new year update
    datas_steam_version_2 = list(filter(lambda data: data["time"] >= 1704409200, datas_all))

    # regroup all the datas
    datasets = {
        "all": datas_all,
        "version_1": datas_steam_version_1,
        "version_2": datas_steam_version_2,
    }

    for datas_name, datas in datasets.items():
        directory = graph_path / datas_name
        directory.mkdir(parents=True, exist_ok=True)

        age.analyse(datas).savefig(directory / "age.svg")
        usage.analyse(datas).savefig(directory / "usage.svg")
        experience.analyse(datas).savefig(directory / "experience.svg")
        hardest_mission.analyse(datas).savefig(directory / "hardest_mission.svg")
        language.analyse(datas).savefig(directory / "language.svg")

        completion_per_mission.analyse(datas).savefig(directory / "completion_per_mission.svg")
        completion_per_age.analyse(datas).savefig(directory / "completion_per_age.svg")
        completion_per_usage.analyse(datas).savefig(directory / "completion_per_usage.svg")
        completion_per_experience.analyse(datas).savefig(directory / "completion_per_experience.svg")
        completion_per_language.analyse(datas).savefig(directory / "completion_per_language.svg")

        duration_per_mission.analyse(datas).savefig(directory / "duration_per_mission.svg")
        duration_per_age.analyse(datas).savefig(directory / "duration_per_age.svg")
        duration_per_usage.analyse(datas).savefig(directory / "duration_per_usage.svg")
        duration_per_experience.analyse(datas).savefig(directory / "duration_per_experience.svg")
        duration_per_language.analyse(datas).savefig(directory / "duration_per_language.svg")
