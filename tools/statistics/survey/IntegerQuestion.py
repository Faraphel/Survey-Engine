class IntegerQuestion:
    def get_average(self, datas: list[int]):
        return sum(datas) / len(datas)

    def get_median(self, datas: list[int]):
        return datas[len(datas) // 2]
