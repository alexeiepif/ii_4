#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Вы работаете над разработкой системы навигации для робота-пылесоса.
# Робот способен передвигаться по различным комнатам в доме,
# но из-за ограниченности ресурсов (например, заряда батареи) и времени на уборку,
# важно эффективно выбирать путь. Ваша задача - реализовать алгоритм,
# который поможет роботу определить, существует ли путь к целевой комнате,
# не превышая заданное ограничение по глубине поиска.
# Дано дерево, где каждый узел представляет собой комнату в доме.
# Узлы связаны в соответствии с возможностью перемещения робота
# из одной комнаты в другую. Необходимо определить, существует ли путь
# от начальной комнаты (корень дерева) к целевой комнате (узел с заданным значением),
# так, чтобы робот не превысил лимит по глубине перемещения.


from typing import Generator, Optional

from tree import Problem
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


class NavigateProblem(Problem):
    def __init__(self, initial: BinaryTreeNode, goal: int):
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


def solve(root: BinaryTreeNode, goal: int, limit: int) -> bool:
    problem = NavigateProblem(root, goal)
    r = dls(problem, limit)
    return bool(r)


if __name__ == "__main__":
    root = BinaryTreeNode(
        1,
        BinaryTreeNode(2, None, BinaryTreeNode(4)),
        BinaryTreeNode(3, BinaryTreeNode(5), None),
    )
    goal = 4
    limit = 2
    print("Первое дерево-пример:", solve(root, goal, limit))

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
    print("Второе дерево:", solve(root2, goal, limit))
