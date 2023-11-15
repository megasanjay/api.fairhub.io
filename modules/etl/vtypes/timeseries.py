from .vtype import VType
import pandas as pd
from datetime import datetime


class SingleTimeseries(VType):
    def __init__(self) -> None:
        super(SingleTimeseries, self).__init__(
            "SingleTimeseries",
            [
                ("filterby", str),
                ("subgroup", str),
                ("color", str),
                ("datetime", datetime),
            ],
            pd._libs.tslibs.nattype.NaTType,
        )


class DoubleDiscreteTimeseries(VType):
    def __init__(self) -> None:
        super(DoubleDiscreteTimeseries, self).__init__(
            "DoubleDiscreteTimeseries",
            [
                ("filterby", str),
                ("subgroup", str),
                ("color", str),
                ("datetime", str),
                ("y", int),
            ],
            pd._libs.tslibs.nattype.NaTType,
        )


class DoubleContinuousTimeseries(VType):
    def __init__(self) -> None:
        super(DoubleContinuousTimeseries, self).__init__(
            "DoubleContinuousTimeseries",
            [
                ("filterby", str),
                ("subgroup", str),
                ("color", str),
                ("datetime", str),
                ("y", float),
            ],
            pd._libs.tslibs.nattype.NaTType,
        )


if __name__ == "__main__":
    pass
else:
    pass
