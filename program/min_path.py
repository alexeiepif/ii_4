#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
from typing import Any, Generator

from tree import Problem, depth_limited_search, path_states

# Для построенного графа лабораторной работы 1
# (имя файла начинается с PR.AI.001.) напишите программу на языке
# программирования Python, которая с помощью алгоритма поиска
# с ограничением глубины находит минимальное расстояние между
# начальным и конечным пунктами.
# Сравните найденное решение с решением, полученным вручную.


class MinPathProblem(Problem):
    def __init__(
        self,
        initial: tuple[str, str],
        goal: tuple[str, str],
        nodes: list[dict[str, Any]],
        edges: list[dict[str, Any]],
    ) -> None:
        super().__init__(initial, goal)
        self.nodes = nodes
        self.edges = edges

    def actions(self, state: tuple[str, str]) -> Generator[dict[str, Any], None, None]:
        for edge in self.edges:
            if edge["data"]["source"] == state[0] or edge["data"]["target"] == state[0]:
                yield edge["data"]

    def result(
        self, state: tuple[str, str], action: dict[str, Any]
    ) -> tuple[str, str] | None:
        if state[0] == action["source"]:
            target = action["target"]
        else:
            target = action["source"]
        for node in self.nodes:
            if node["data"]["id"] == target:
                return (node["data"]["id"], node["data"]["label"])
        return None

    def is_goal(self, state: tuple[str, str]) -> bool:
        return state == self.goal  # type: ignore

    def action_cost(
        self, s: tuple[str, str], a: dict[str, Any], s1: tuple[str, str]
    ) -> int:
        return a["weight"]  # type: ignore


def load_elems(path: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    with open(path, encoding="utf-8") as f:
        elems = json.load(f)

    for i, elem in enumerate(elems):
        if not elem.get("position", None):
            nodes_index = i
            break

    nodes = elems[:nodes_index]
    edges = elems[nodes_index:]
    return nodes, edges


def solve(
    init: tuple[str, str],
    goal: tuple[str, str],
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> tuple[int, list[tuple[str, str]]]:
    problem = MinPathProblem(init, goal, nodes, edges)
    limit = 8
    b = depth_limited_search(problem, limit)
    length = b.path_cost
    path = path_states(b)
    return length, path


if __name__ == "__main__":
    nodes, edges = load_elems("json/elem_full.json")
    for node in nodes:
        if node["data"]["label"] == "Липецк":
            initial = (node["data"]["id"], node["data"]["label"])
        elif node["data"]["label"] == "Самара":
            goal = (node["data"]["id"], node["data"]["label"])
    length, path = solve(initial, goal, nodes, edges)
    print("Длина кратчайшего пути:", length)
    print("Кратчайший путь:", path)
