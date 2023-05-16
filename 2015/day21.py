from aoc_components.puzzle_input import PuzzleInput
from typing import NamedTuple
from dataclasses import dataclass
import re
import math

shop_raw = """
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""

r = re.compile(r"^(.*)\s+(\d+)\s+(\d+)\s+(\d+)$")


@dataclass
class Fighter:
    max_hp: int
    hp: int
    dmg: int = 0
    amr: int = 0

    def reset(self):
        self.hp = self.max_hp

    def damage_to(self, defender: 'Fighter'):
        return max(self.dmg - defender.amr, 1)

    def moves_to_defeat(self, defender: 'Fighter'):
        turns = math.ceil(defender.max_hp / self.damage_to(defender))
        return turns


def defeats(attacker: Fighter, defender: Fighter):
    at = attacker.moves_to_defeat(defender)
    df = defender.moves_to_defeat(attacker)
    return at <= df


def defeats_by_round(player: Fighter, boss: Fighter):
    player.reset()
    boss.reset()
    my_dm = player.damage_to(boss)
    boss_dm = boss.damage_to(player)
    while True:
        boss.hp -= my_dm
        if boss.hp <= 0:
            return True

        player.hp -= boss_dm
        if player.hp <= 0:
            return False


class Item(NamedTuple):
    group: str
    name: str
    cost: int = 0
    damage: int = 0
    armor: int = 0


def parse_shop():
    items = {
        "Weapons": [],
        "Armor": [
            Item("Armor", "Skin")
            ],
        "Rings": [
            Item("Rings", "Finger 1"),
            Item("Rings", "Finger 2")
            ],
    }
    group = ""
    for line in shop_raw.splitlines():
        if not line:
            continue
        i = line.find(":")
        if i > -1:
            group = line[:i]
        else:
            m = r.match(line)
            if not m:
                raise RuntimeError()
            i = Item(group, m[1].strip(), int(m[2]), int(m[3]), int(m[4]))
            items[group].append(i)
    return items


def parse_boss(inp):
    for line in inp.splitlines():
        a, b = line.split(": ")
        if a.startswith("H"):
            hp = int(b)
        elif a.startswith("D"):
            dmg = int(b)
        elif a.startswith("A"):
            amr = int(b)
        else:
            raise RuntimeError()
    return Fighter(hp, hp, dmg, amr)


def iter_loadouts(items: dict):
    for weapon in items["Weapons"]:
        for armor in items["Armor"]:
            for ring1 in items["Rings"]:
                for ring2 in items["Rings"]:
                    if ring1 != ring2:
                        yield (weapon, armor, ring1, ring2)


def test():
    player = Fighter(8, 8, 5, 5)
    boss = Fighter(12, 12, 7, 2)
    assert defeats(player, boss)


def load(items: tuple) -> (int, Fighter):
    player = Fighter(100, 100)
    item: Item
    cost = 0
    for item in items:
        if not item:
            continue
        player.amr += item.armor
        player.dmg += item.damage
        cost += item.cost
    return cost, player


def run(boss: Fighter, items):
    min_ = float('inf')
    max_ = float('-inf')
    for loadout in iter_loadouts(items):
        cost, player = load(loadout)
        if defeats(player, boss):
            min_ = min(min_, cost)
        else:
            max_ = max(max_, cost)
    return (min_, max_)


if __name__ == "__main__":
    test()

    inp = PuzzleInput(__file__).get()
    boss = parse_boss(inp)

    shop = parse_shop()
    part1, part2 = run(boss, shop)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
