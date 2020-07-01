import statistics


class Aggregation(object):

    @staticmethod
    def take_first(vals) -> object:
        return vals[0]

    @staticmethod
    def take_last(vals) -> object:
        return vals[-1]

    @staticmethod
    def take_min(vals) -> float:
        return min(vals)

    @staticmethod
    def take_max(vals) -> float:
        return max(vals)

    @staticmethod
    def take_sum(vals) -> float:
        return sum(vals)

    @staticmethod
    def take_mean(vals) -> float:
        return statistics.mean(vals)

    @staticmethod
    def take_median(vals) -> float:
        return statistics.median(vals)

    @staticmethod
    def take_mode(vals) -> float:
        return statistics.mode(vals)

    @staticmethod
    def take_stdev(vals) -> float:
        return statistics.stdev(vals)

    @staticmethod
    def take_variance(vals) -> float:
        return statistics.variance(vals)
