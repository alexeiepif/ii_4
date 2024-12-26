#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Представьте, что вы разрабатываете систему
# для автоматического управления инвестициями, где дерево решений используется
# для представления последовательности инвестиционных решений
# и их потенциальных исходов. Цель состоит в том, чтобы найти
# наилучший исход (максимальную прибыль) на определённой глубине принятия решений,
# учитывая ограниченные ресурсы и время на анализ.

from typing import Generator, Optional

from tree import LIFOQueue, Node, Problem, expand, is_cycle


class BinaryTreeNode:
    def __init__(
        self,
        value: int,
        left: Optional["BinaryTreeNode"] = None,
        right: Optional["BinaryTreeNode"] = None,
    ) -> None:
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"<{self.value}>"


class InvestProblem(Problem):
    def __init__(self, initial: BinaryTreeNode) -> None:
        super().__init__(initial)

    def actions(self, state: BinaryTreeNode) -> Generator[BinaryTreeNode, None, None]:
        left = state.left
        right = state.right
        if left:
            yield left
        if right:
            yield right

    def result(self, state: BinaryTreeNode, action: BinaryTreeNode) -> BinaryTreeNode:
        return action


def dls(problem: Problem, limit: int = 10) -> int:
    """В первую очередь ищем самые глубокие узлы в дереве поиска."""
    frontier = LIFOQueue([Node(problem.initial)])  # type: ignore
    result = []
    while frontier:
        node = frontier.pop()
        if len(node) == limit:
            result.append(node.state.value)  # type: ignore
        elif not is_cycle(node):
            for child in expand(problem, node):
                frontier.append(child)
    return max(result) if result else 0


def solve(root: BinaryTreeNode, limit: int) -> int:
    problem = InvestProblem(root)
    r = dls(problem, limit)
    return r


if __name__ == "__main__":
    root = BinaryTreeNode(
        3,
        BinaryTreeNode(1, BinaryTreeNode(0), None),
        BinaryTreeNode(5, BinaryTreeNode(4), BinaryTreeNode(6)),
    )
    limit = 2
    r = solve(root, limit)
    if r:
        st = f"Максимальное значение на указанной глубине: {r}"
    else:
        st = "Дерево не настолько глубокое"
    print("Первое дерево-пример. ", st)

    root2 = BinaryTreeNode(
        19,
        BinaryTreeNode(
            11,
            BinaryTreeNode(16, None, BinaryTreeNode(10)),
            BinaryTreeNode(15),
        ),
        BinaryTreeNode(
            6,
            BinaryTreeNode(18),
            BinaryTreeNode(13, None, BinaryTreeNode(12)),
        ),
    )

    limit = 3
    r = solve(root2, limit)
    if r:
        st = f"Максимальное значение на указанной глубине: {r}"
    else:
        st = "Дерево не настолько глубокое"
    print("Второе дерево: ", st)
