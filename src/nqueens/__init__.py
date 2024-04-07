# SPDX-FileCopyrightText: 2024-present Joel Christiansen <greenbadge.jc@gmail.com>
#
# SPDX-License-Identifier: MIT
# for a nxn grid, find an arrangement of n queens such that no queen is attacking any other queen.

from copy import deepcopy
from dataclasses import dataclass
from typing import Iterator, Optional


@dataclass
class Pos:
    x: int
    y: int


class Grid:
    def __init__(self, n: int) -> None:
        self._grid: list[list[Optional[bool]]] = [[None] * n for _ in range(n)]

    def __getitem__(self, pos: Pos) -> Optional[bool]:
        return self._grid[pos.y][pos.x]

    def __setitem__(self, pos: Pos, value: Optional[bool]) -> None:
        self._grid[pos.y][pos.x] = value

    def __iter__(self) -> Iterator[list[Optional[bool]]]:
        return iter(self._grid)

    def free_pos(self) -> Iterator[Pos]:
        for y, row in enumerate(self._grid):
            for x, elem in enumerate(row):
                if elem is None:
                    yield Pos(x, y)


def print_board(board: Grid) -> None:
    for row in board:
        for elem in row:
            if elem:
                print("Q", end="")
            elif elem is False:
                print("x", end="")
            else:
                print(".", end="")
        print()


def set_attack(pos: Pos, board: Grid, n: int) -> list[Pos]:
    # horizontal and vertical
    changed = []
    for p in range(0, n):
        new_pos = Pos(x=p, y=pos.y)
        if new_pos != pos:
            if board[new_pos]:
                raise ValueError("Shouldn't be possible")
            if board[new_pos] is None:
                changed.append(new_pos)
            board[new_pos] = False
        new_pos = Pos(x=pos.x, y=p)
        if new_pos != pos:
            if board[new_pos]:
                raise ValueError(f"Shouldn't be possible {new_pos}")
            if board[new_pos] is None:
                changed.append(new_pos)
            board[new_pos] = False
    # diag
    for offset in ((-1, -1), (1, 1), (-1, 1), (1, -1)):
        x = pos.x
        y = pos.y
        while True:
            x = x + offset[0]
            y = y + offset[1]
            try:
                if x < 0 or y < 0:
                    break
                if board[Pos(x, y)] is None:
                    changed.append(Pos(x=x, y=y))
                board[Pos(x=x, y=y)] = False
            except IndexError:
                break
    return changed


class Board:
    def __init__(self, n: int) -> None:
        self._grid: Grid = Grid(n)
        self._n = n

    # list list optional bool -> None = maybe queen, False = no queen maybe not, True = Yes queen
    def solve(self, board: Optional[Grid] = None, n_queens: Optional[int] = None) -> bool:
        if board is None:
            board = self._grid
        if n_queens is None:
            n_queens = self._n

        for point in board.free_pos():
            new_board = deepcopy(board)
            new_board[point] = True
            set_pos = set_attack(point, new_board, self._n)

            if n_queens == 1:
                self._grid = new_board
                return True
            else:
                if self.solve(new_board, n_queens - 1):
                    return True
            new_board[point] = False
            for pos in set_pos:
                new_board[pos] = None
                board = new_board
        return False

    def print(self) -> None:
        print_board(self._grid)


def main(n: int) -> None:
    board = Board(n)
    board.solve()
    print()
    board.print()


if __name__ == "__main__":
    main(8)
