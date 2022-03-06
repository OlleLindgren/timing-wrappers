from __future__ import annotations

import collections
import datetime
import math
import statistics
import time
from termcolor import colored
from typing import Callable, List, Tuple


class TimeKeeper:
    """Class for tracking execution time of things"""

    # TimeKeeper rec stuff
    t: List[Tuple[datetime.datetime, str]]
    dt: List[datetime.timedelta]

    # TimeKeeper Track stuff
    tracks: dict = collections.defaultdict(list)

    def __init__(self) -> None:
        self.t = []
        self.dt = []
        self.rec('TimeKeeper created')

    def rec(self, name: str):
        self.t.append((datetime.datetime.now(), name))
        if len(self.t) > 1:
            self.dt.append(self.t[-1][0] - self.t[-2][0])
        else:
            self.dt.append(datetime.timedelta(seconds=0))

    @staticmethod
    def _get_col(exec_t_seconds: float | int) -> str:
        """Get color by execution time

        Args:
            exec_t_seconds (float | int): Execution time

        Returns:
            str: Color to print in
        """
        if exec_t_seconds > 60:
            return 'red'
        elif exec_t_seconds > 1:
            return 'yellow'
        elif exec_t_seconds > .001:
            return 'green'
        else:
            return 'blue'

    @staticmethod
    def str_format(dt: datetime.timedelta, name: str):
        s = dt.seconds
        mi = dt.microseconds

        return colored(f'{s:4d}:{mi:6d}   | {name}', TimeKeeper._get_col(s))

    def recp(self, name: str):
        self.rec(name)
        print(self.str_format(self.dt[-1], self.t[-1][1]))

    @classmethod
    def tracks_str(cls):
        result = ''
        for key, records in sorted(cls.tracks.items(), key=lambda tup: -sum(tup[1])):
            total = sum(records)
            avg = statistics.mean(records) if records else 0
            N = len(records)
            total_s = math.floor(total)
            total_mi = int((total - total_s) * 1e6)
            avg_s = math.floor(avg)
            avg_mi = int((avg - avg_s) * 1e6)

            result += colored(f'\n{total_s:4d}:{total_mi:6d} = {N:8d} * ({avg_s:4d}:{avg_mi:6d})   | {key}',
                              TimeKeeper._get_col(total_s))
        return result

    def __str__(self):
        result = f'TimeKeeper object with {len(self.t)-1} records and {len(self.tracks.keys())} tracked functions'

        result += '\n sec:min    =    calls * ( sec:min/call) | function'

        if len(self.t) > 1:
            dt = [self.t[i+1][0] - self.t[i][0] for i in range(len(self.t)-1)]
            result += '\n' + '\n'.join(
                self.str_format(_dt, s)
                for (_, s), _dt in zip(self.t[1:], dt))

        result += self.tracks_str()

        return result

    # decorator
    @classmethod
    def track(cls, key: str = None):
        """Decorator, used for tracking a function

        Args:
            key (str, optional): Optional key to store. Defaults to '<None>'.

        Returns:
            _type_: _description_
        """

        def pseudo_track(f: Callable):
            def wrapper(*args, **kwargs):
                t0 = time.time()
                try:
                    result = f(*args, **kwargs)
                finally:
                    dt = time.time() - t0
                    cls.tracks[key if key is not None else f.__name__].append(dt)
                return result
            return wrapper
        return pseudo_track
