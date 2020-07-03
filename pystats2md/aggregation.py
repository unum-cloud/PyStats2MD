import statistics


class Aggregation(object):

    @staticmethod
    def take_first(vals) -> object:
        if len(vals) == 0:
            return 0
        return vals[0]

    @staticmethod
    def take_last(vals) -> object:
        if len(vals) == 0:
            return 0
        return vals[-1]

    @staticmethod
    def take_min(vals) -> float:
        if len(vals) == 0:
            return 0
        return min(vals)

    @staticmethod
    def take_max(vals) -> float:
        if len(vals) == 0:
            return 0
        return max(vals)

    @staticmethod
    def take_sum(vals) -> float:
        if len(vals) == 0:
            return 0
        return sum(vals)

    @staticmethod
    def take_mean(vals) -> float:
        if len(vals) == 0:
            return 0
        return statistics.mean(vals)

    @staticmethod
    def take_median(vals) -> float:
        if len(vals) == 0:
            return 0
        return statistics.median(vals)

    @staticmethod
    def take_mode(vals) -> float:
        if len(vals) == 0:
            return 0
        return statistics.mode(vals)

    @staticmethod
    def take_stdev(vals) -> float:
        if len(vals) == 0:
            return 0
        return statistics.stdev(vals)

    @staticmethod
    def take_variance(vals) -> float:
        if len(vals) == 0:
            return 0
        return statistics.variance(vals)
