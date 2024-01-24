from pathlib import Path

from tools.statistics.analyse import (age, usage, completion_per_mission, duration_per_mission, completion_per_age,
                                      completion_per_usage, duration_per_age, duration_per_usage,
                                      completion_per_experience, duration_per_experience, experience, hardest_mission)

if __name__ == "__main__":
    from source.utils import compress

    directory = Path(r"./sondage/")

    # read every people survey data
    datas = [
        compress.uncompress_data(file.read_bytes())  # decompress the data
        for file in directory.rglob("*.rsl")
    ]

    # age.analyse(datas)
    # usage.analyse(datas)
    # experience.analyse(datas)
    # hardest_mission.analyse(datas)  # !

    # completion_per_mission.analyse(datas)
    # completion_per_age.analyse(datas)
    # completion_per_usage.analyse(datas)  # !
    # completion_per_experience.analyse(datas)

    # duration_per_mission.analyse(datas)
    # duration_per_age.analyse(datas)
    # duration_per_usage.analyse(datas)  # !
    # duration_per_experience.analyse(datas)  # !
