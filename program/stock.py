#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Представьте, что вы разрабатываете систему для управления складом,
# где товары упорядочены в структуре, похожей на двоичное дерево.
# Каждый узел дерева представляет место хранения, которое может вести
# к другим местам хранения (левому и правому подразделу).
# Ваша задача — найти наименее затратный путь к товару,
# ограничив поиск заданной глубиной, чтобы гарантировать,
# что поиск займет приемлемое время.

from typing import Generator, Optional

from tree import Node, Problem
from tree import depth_limited_search as dls


class BinaryTreeNode:
    def __init__(
        self,
        value: int,
        left: Optional["BinaryTreeNode"] = None,
        right: Optional["BinaryTreeNode"] = None,
    ):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"<{self.value}>"


class StockProblem(Problem):
    def __init__(self, initial: BinaryTreeNode, goal: int) -> None:
        super().__init__(initial, goal)

    def actions(self, state: BinaryTreeNode) -> Generator[BinaryTreeNode, None, None]:
        left = state.left
        right = state.right
        if left:
            yield left
        if right:
            yield right

    def result(self, state: BinaryTreeNode, action: BinaryTreeNode) -> BinaryTreeNode:
        return action

    def is_goal(self, state: BinaryTreeNode) -> bool:
        return state.value == self.goal  # type: ignore


def solve(root: BinaryTreeNode, goal: int, limit: int) -> Node:
    problem = StockProblem(root, goal)
    r: Node = dls(problem, limit)
    return r


if __name__ == "__main__":
    root = BinaryTreeNode(
        1,
        BinaryTreeNode(2, None, BinaryTreeNode(4)),
        BinaryTreeNode(3, BinaryTreeNode(5), None),
    )
    goal = 4
    limit = 2
    r = solve(root, goal, limit)
    if r:
        st = f"Цель найдена: {r.state}"  # type: ignore
    else:
        st = "Цель не найдена"
    print("Первое дерево-пример. ", st)

    root2 = BinaryTreeNode(
        1,
        BinaryTreeNode(
            2,
            BinaryTreeNode(4, None, BinaryTreeNode(8)),
            BinaryTreeNode(5),
        ),
        BinaryTreeNode(
            3,
            BinaryTreeNode(6),
            BinaryTreeNode(7, None, BinaryTreeNode(9)),
        ),
    )
    goal = 8
    limit = 2
    r = solve(root2, goal, limit)
    if r:
        st = f"Цель найдена: {r.state}"  # type: ignore
    else:
        st = "Цель не найдена"
    print("Второе дерево. ", st)
