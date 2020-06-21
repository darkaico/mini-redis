from dataclasses import (
    dataclass,
    field
)


@dataclass
class SortedList:

    zsorts: list = field(default_factory=list)
    zvalues: dict = field(default_factory=dict)
    zreverse: dict = field(default_factory=dict)

    def zadd(self, score, member):

        if self.exists(score, member):
            return 0

        self.zsorts.append(score)

        self.zsorts = sorted(self.zsorts)

        if score not in self.zvalues:
            self.zvalues[score] = []

        self.zvalues[score].append(member)
        self.zreverse[member] = score

        # NOTE: Current implementation only support 1 key at the time
        return 1

    def zrange(self, start, stop):
        if self.zcard() == 0:
            return []

        stop_index = stop % self.zcard() + 1

        return [zvalue for zkey in set(self.zsorts[start:stop_index]) for zvalue in self.zvalues[zkey]]

    def zrank(self, member):
        zsort = self.zreverse.get(member)
        if not zsort:
            return None

        return self.zsorts.index(zsort)

    def zcard(self):
        return len(self.zsorts)

    def exists(self, score, member):
        zsort = self.zreverse.get(member)

        return score == zsort
