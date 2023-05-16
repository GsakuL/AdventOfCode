from typing import NamedTuple

from aoc_components import PuzzleInput

class They:
    Rock = "A"
    Paper = "B"
    Scissors = "C"

class Me:
    Rock = "X"
    Paper = "Y"
    Scissors = "Z"

class Result:
    loose = 0
    draw = 3
    win = 6

class End:
    lose = "X"
    draw = "Y"
    win = "Z"

class Round(NamedTuple):
    they: str
    me: str

shape_points = {
    Me.Rock: 1,
    Me.Paper: 2,
    Me.Scissors: 3,
}

def parse(txt: str):
    for line in txt.splitlines():
        a,b = line.strip().upper().split(" ")
        yield Round(a,b)

results = {
    (They.Rock, Me.Rock): Result.draw,
    (They.Rock, Me.Paper): Result.win,
    (They.Rock, Me.Scissors): Result.loose,

    (They.Paper, Me.Rock): Result.loose,
    (They.Paper, Me.Paper): Result.draw,
    (They.Paper, Me.Scissors): Result.win,

    (They.Scissors, Me.Rock): Result.win,
    (They.Scissors, Me.Paper): Result.loose,
    (They.Scissors, Me.Scissors): Result.draw,
}

wanted_results = {
    (They.Rock, End.win): Me.Paper,
    (They.Rock, End.draw): Me.Rock,
    (They.Rock, End.lose): Me.Scissors,

    (They.Paper, End.win): Me.Scissors,
    (They.Paper, End.draw): Me.Paper,
    (They.Paper, End.lose): Me.Rock,

    (They.Scissors, End.win): Me.Rock,
    (They.Scissors, End.draw): Me.Scissors,
    (They.Scissors, End.lose): Me.Paper,
}

def my_score_part_one(pair: Round):
    return results[pair] + shape_points[pair.me]

def my_score_part_two(pair: Round):
    my_pick = wanted_results[pair]
    return results[(pair.they, my_pick)] + shape_points[my_pick]


if __name__ == "__main__":
    puzzle = PuzzleInput(__file__).get()
    strategy = list(parse(puzzle))

    score_1 = sum((my_score_part_one(play) for play in strategy))
    print(f"Part 1: {score_1}")

    score_2 = sum((my_score_part_two(play) for play in strategy))
    print(f"Part 2: {score_2}")
