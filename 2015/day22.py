from aoc_components.puzzle_input import PuzzleInput
from typing import NamedTuple, Dict, List
from dataclasses import dataclass
import re
import math
from collections import defaultdict
from abc import ABC, abstractmethod


@dataclass
class Fighter:
    max_hp: int
    dmg: int = 0
    hp: int = 0
    amr: int = 0
    mana: int = 0
    mana_used: int = 0

    def copy(self):
        return Fighter(**vars(self))

    def reset(self):
        self.hp = self.max_hp

    def damage_to(self, defender: 'Fighter'):
        return max(self.dmg - defender.amr, 1)

    def moves_to_defeat(self, defender: 'Fighter'):
        turns = math.ceil(defender.max_hp / self.damage_to(defender))
        return turns


@dataclass
class SpellBase(ABC):
    cost: int

    def can_cast(self, player: Fighter):
        return player.mana >= self.cost

    @abstractmethod
    def cast(self, player: Fighter, boss: Fighter):
        pass


@dataclass
class Effect(SpellBase):
    max_turns: int
    active = False
    current_turn: int = 0

    def reset(self):
        self.active = False

    def start(self, player: Fighter, boss: Fighter):
        self.active = True
        self.current_turn = 1

    def end(self, player: Fighter, boss: Fighter):
        self.active = False

    def round_begin(self, player: Fighter, boss: Fighter):
        if self.active:
            self.current_turn += 1

    def cast(self, player: Fighter, boss: Fighter):
        """only call after round_start per turn"""
        self.start(player, boss)

    def round_end(self, player: Fighter, boss: Fighter):
        if self.current_turn >= self.max_turns:
            self.end(player, boss)

    def can_cast(self, player: Fighter):
        return super().can_cast(player) and ((not self.active) or self.current_turn == self.max_turns)


@dataclass
class Offensive(SpellBase):
    pass


@dataclass
class MagicMissile(Offensive):
    cost = 53
    damage = 4

    def cast(self, player: Fighter, boss: Fighter):
        boss.hp -= self.damage


@dataclass
class Drain(Offensive):
    cost = 73
    damage = 2
    heal = 2

    def cast(self, player: Fighter, boss: Fighter):
        boss.hp -= self.damage
        player.hp += self.heal


@dataclass
class Shield(Effect):
    cost = 113
    max_turns = 6
    armor = 7

    def start(self, player: Fighter, boss: Fighter):
        super().start(player, boss)
        player.amr += self.armor

    def end(self, player: Fighter, boss: Fighter):
        super().end(player, boss)
        player.amr += self.armor


@dataclass
class Poison(Effect):
    cost = 173
    max_turns = 6
    damage = 3

    def round_begin(self, player: Fighter, boss: Fighter):
        boss.hp -= self.damage


@dataclass
class Recharge(Effect):
    cost = 229
    max_turns = 5
    recharge = 101

    def round_begin(self, player: Fighter, boss: Fighter):
        player.mana += self.recharge


class Spells2:
    magic_missile = MagicMissile()
    drain = Drain()
    shield = Shield()
    poison = Poison()
    recharge = Recharge()

    all_ = (magic_missile, drain, shield, poison, recharge)

    effects: List[Effect] = [s for s in all_ if isinstance(s, Effect)]
    effects: List[Offensive] = [s for s in all_ if isinstance(s, Offensive)]


@dataclass
class Spell:
    name: str
    cost: int
    damage: int = 0
    max_turns: int = 1
    heal: int = 0
    armor: int = 0
    recharge: int = 0
    active = False
    current_turn: int = 0

    def can_cast(self, player: Fighter):
        return (not self.active) and player.mana >= self.cost

    def effect_start(self, player: Fighter, boss: Fighter):
        self.current_turn = 1
        self.active = True
        player.amr += self.armor

    def effect_end(self, player: Fighter, boss: Fighter):
        player.amr -= self.armor
        self.active = False

    def turn_start(self, player: Fighter, boss: Fighter):
        player.mana += self.recharge
        player.hp += self.heal
        boss.dmg -= self.damage


class Spells:
    magic_missile = Spell("Magic Missile", 53, damage=4)
    drain = Spell("Drain", 73, damage=2, heal=2)

    shield = Spell("Shield", 113, turns=6, armor=7)
    poison = Spell("Poison", 173, turns=6, damage=3)
    recharge = Spell("Recharge", 229, turns=5, recharge=101)

    all_ = (magic_missile, drain, shield, poison, recharge)


def parse_boss(inp):
    for line in inp.splitlines():
        a, b = line.split(": ")
        if a.startswith("H"):
            hp = int(b)
        elif a.startswith("D"):
            dmg = int(b)
        else:
            raise RuntimeError()
    return Fighter(hp, dmg)


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


def max_mana_cost_except_recharge():
    m = 0
    for s in Spells2.all_:
        if not isinstance(s, Recharge):
            m = max(m, s.cost)
    return m


def player_turn(player: Fighter, boss: Fighter):
    if (player.mana - Spells2.recharge.cost <= max_mana_cost_except_recharge()
       and Spells2.recharge.can_cast(player)):
        Spells2.recharge.cast(player)
        return

    for spell in (Spells2.shield, Spells2.poison):
        if spell.can_cast(player):
            spell.cast(player, boss)
            return



def run(boss: Fighter):
    player = Fighter(50, mana=500)
    for effect in Spells2.effects:
        effect.reset()

    is_player_turn = True
    while (player.hp > 0) and (boss.hp > 0):
        for effect in Spells2.effects:
            effect.round_begin(player, boss)
        if is_player_turn:
            player_turn(player, boss)
        else:
            player.hp -= boss.damage_to(player)

        for effect in Spells2.effects:
            effect.round_end(player, boss)
        is_player_turn ^= True


if __name__ == "__main__":
    # test()

    inp = PuzzleInput(__file__).get()
    boss = parse_boss(inp)

    part1, part2 = run(boss)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
