from pathlib import Path

if __name__ == "__main__":
    from source.utils import compress

    directory = Path(r"C:\Users\RC606\Downloads\résultats étude")

    # read every people survey data
    for file in directory.rglob("*.rsl"):
        # decompress the data
        data = compress.uncompress_data(file.read_bytes())

        


    ages = sorted(list(map(
        lambda data: data["surveys"]["question-age"]["value"],
        datas
    )))

    print(ages)
    print(sum(ages) / len(ages))
    print(ages[len(ages) // 2])
    print(min(ages))
    print(max(ages))

    print(datas[1]["surveys"]["question-usage-steam"])

    usages = sorted(list(map(
        lambda data: data["surveys"]["question-usage-steam"]["choices"],
        datas
    )))

    print(usages)
    print(sum(usages) / len(usages))
    print(usages[len(usages) // 2])
    print(min(usages))
    print(max(usages))
