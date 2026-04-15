"""Dijkstra shortest path demo based on `Rename.md`.

This script implements a priority-queue-based Dijkstra algorithm for a
non-negative weighted graph represented as an adjacency dictionary.

The file is designed to be both readable for course submission and directly
executable for a short classroom demo.
"""

from __future__ import annotations

import argparse
import json
import heapq
from math import inf
from pathlib import Path
from collections.abc import Mapping
from typing import Dict, Hashable, List, Tuple

Graph = Dict[Hashable, Dict[Hashable, float]]


def normalize_graph(graph: Mapping[Hashable, Mapping[Hashable, float]]) -> Graph:
    """Validate a graph and ensure every referenced vertex exists.

    The expected input format is an adjacency-list mapping:

        {
            "A": {"B": 2, "C": 5},
            "B": {"A": 2}
        }

    Missing target vertices are added automatically with empty neighbor lists.
    """

    normalized: Graph = {}

    for vertex, neighbors in graph.items():
        if not isinstance(neighbors, Mapping):
            raise TypeError(
                f"Neighbors for vertex {vertex!r} must be a mapping of neighbor -> weight."
            )

        normalized.setdefault(vertex, {})
        for neighbor, weight in neighbors.items():
            if not isinstance(weight, (int, float)):
                raise TypeError(
                    f"Edge weight for {vertex!r} -> {neighbor!r} must be numeric, got {type(weight).__name__}."
                )
            if weight < 0:
                raise ValueError(
                    f"Dijkstra's algorithm requires non-negative edge weights, but {vertex!r} -> {neighbor!r} has {weight}."
                )

            normalized[vertex][neighbor] = weight
            normalized.setdefault(neighbor, {})

    return normalized


def _run_dijkstra(
    graph: Mapping[Hashable, Mapping[Hashable, float]], start: Hashable
) -> Tuple[Graph, Dict[Hashable, float], Dict[Hashable, Hashable | None]]:
    """Internal Dijkstra implementation that also records predecessors."""

    normalized = normalize_graph(graph)

    if start not in normalized:
        raise KeyError(f"Start vertex {start!r} is not in the graph.")

    distances = {vertex: inf for vertex in normalized}
    previous: Dict[Hashable, Hashable | None] = {vertex: None for vertex in normalized}
    distances[start] = 0
    priority_queue: List[Tuple[float, Hashable]] = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in normalized[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    return normalized, distances, previous


def dijkstra(graph: Graph, start: Hashable) -> Dict[Hashable, float]:
    """Return the shortest distances from ``start`` to every vertex in ``graph``.

    Parameters
    ----------
    graph:
        Adjacency dictionary in the form {vertex: {neighbor: weight, ...}, ...}.
        All edge weights must be non-negative.
    start:
        The source vertex.

    Returns
    -------
    dict
        Mapping of each vertex to its shortest distance from ``start``.
    """

    _, distances, _ = _run_dijkstra(graph, start)
    return distances


def reconstruct_path(
    graph: Graph, start: Hashable, target: Hashable
) -> List[Hashable]:
    """Reconstruct one shortest path from ``start`` to ``target``.

    This helper is optional and is included so the script is useful beyond the
    distance-only example from the report.
    """

    normalized, distances, previous = _run_dijkstra(graph, start)

    if target not in normalized:
        raise KeyError(f"Target vertex {target!r} is not in the graph.")

    if distances.get(target, inf) == inf:
        return []

    path: List[Hashable] = []
    node: Hashable | None = target
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()
    return path


def load_graph_from_json(file_path: Path) -> Graph:
    """Load a graph from a JSON file in adjacency-list form."""

    try:
        raw_data = json.loads(file_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise FileNotFoundError(f"Could not read graph file {file_path!s}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Graph file {file_path!s} is not valid JSON: {exc}") from exc

    if not isinstance(raw_data, Mapping):
        raise ValueError("The JSON graph must be an object mapping vertices to neighbors.")

    return normalize_graph(raw_data)


def print_ascii_graph(graph: Graph, start: Hashable) -> None:
    """Render the graph as one connected ASCII canvas."""

    distances = dijkstra(graph, start)
    layers: Dict[float, List[Hashable]] = {}
    unreachable: List[Hashable] = []

    for vertex in sorted(graph, key=str):
        distance = distances.get(vertex, inf)
        if distance == inf:
            unreachable.append(vertex)
        else:
            layers.setdefault(distance, []).append(vertex)

    if not layers:
        print("ASCII graph: (empty)")
        return

    layer_keys = sorted(layers)
    x_gap = 18
    y_gap = 4
    margin_x = 6
    margin_y = 2

    positions: Dict[Hashable, Tuple[int, int]] = {}
    for layer_index, distance in enumerate(layer_keys):
        for row_index, vertex in enumerate(layers[distance]):
            positions[vertex] = (
                margin_x + layer_index * x_gap,
                margin_y + row_index * y_gap,
            )

    max_x = max(x for x, _ in positions.values()) + 6
    max_y = max(y for _, y in positions.values()) + 4
    canvas: List[List[str]] = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    def put(x: int, y: int, text: str) -> None:
        if y < 0 or y >= len(canvas):
            return
        for offset, ch in enumerate(text):
            xx = x + offset
            if 0 <= xx < len(canvas[y]):
                canvas[y][xx] = ch

    def draw_node(vertex: Hashable, x: int, y: int) -> None:
        put(x, y, f"({vertex})")

    def line_char(dx: int, dy: int) -> str:
        if dx == 0:
            return "|"
        if dy == 0:
            return "-"
        return "\\" if dx * dy > 0 else "/"

    def draw_edge(source: Hashable, target: Hashable, weight: float) -> None:
        sx, sy = positions[source]
        tx, ty = positions[target]

        source_anchor = sx + 1
        target_anchor = tx + 1
        points: List[Tuple[int, int]] = []

        x, y = source_anchor, sy
        points.append((x, y))

        step_x = 1 if target_anchor > x else -1 if target_anchor < x else 0
        step_y = 1 if ty > y else -1 if ty < y else 0

        # First move horizontally toward the target layer, then vertically, then horizontally again.
        bend_x = target_anchor if step_x >= 0 else max(0, target_anchor - 4)
        if bend_x == x:
            bend_x = x + 4 if x + 4 < len(canvas[0]) else x

        while x != bend_x:
            x += 1 if bend_x > x else -1
            points.append((x, y))

        while y != ty:
            y += 1 if ty > y else -1
            points.append((x, y))

        while x != target_anchor:
            x += 1 if target_anchor > x else -1
            points.append((x, y))

        for i in range(1, len(points) - 1):
            px, py = points[i - 1]
            cx, cy = points[i]
            nx, ny = points[i + 1]
            ch = line_char(cx - px, cy - py)
            canvas[cy][cx] = ch

        if len(points) >= 2:
            ex, ey = points[-1]
            canvas[ey][ex] = ">" if target_anchor >= source_anchor else "<"

        mid = points[len(points) // 2]
        label = str(int(weight) if float(weight).is_integer() else weight)
        put(max(0, mid[0] - len(label) // 2), max(0, mid[1] - 1), label)

    printed_edges = set()
    for source in sorted(graph, key=str):
        for target in sorted(graph[source], key=str):
            weight = graph[source][target]
            edge_signature = (frozenset((source, target)), weight)
            if edge_signature in printed_edges:
                continue
            printed_edges.add(edge_signature)

            if source not in positions or target not in positions:
                continue

            left, right = source, target
            if distances[left] > distances[right] or (
                distances[left] == distances[right] and str(left) > str(right)
            ):
                left, right = right, left

            draw_edge(left, right, weight)

    for vertex, (x, y) in positions.items():
        draw_node(vertex, x, y)

    print("ASCII graph:")
    for line in canvas:
        print("".join(line).rstrip())

    if unreachable:
        print("unreachable:", ", ".join(f"({vertex})" for vertex in unreachable))


def build_argument_parser() -> argparse.ArgumentParser:
    """Create the command-line interface for the demo."""

    parser = argparse.ArgumentParser(
        description=(
            "Run Dijkstra's shortest path algorithm on either the built-in sample graph "
            "or a custom adjacency-list graph stored in JSON."
        )
    )
    parser.add_argument(
        "--graph-file",
        type=Path,
        help=(
            "Path to a JSON file containing an adjacency-list graph. "
            "If omitted, the script loads sample_graph.json next to code.py."
        ),
    )
    parser.add_argument(
        "--start",
        default="A",
        help="Start vertex for shortest-path computation (default: A).",
    )
    return parser


def run_demo(graph: Graph, start: Hashable) -> None:
    """Print the ASCII graph and then the shortest paths from ``start``."""

    print_ascii_graph(graph, start)
    print()
    shortest_paths = dijkstra(graph, start)
    ordered_vertices = sorted(shortest_paths, key=str)
    for target in ordered_vertices:
        if target == start:
            continue
        path = reconstruct_path(graph, start, target)
        if path:
            print(f"{start} -> {target}: {path} (distance = {shortest_paths[target]})")
        else:
            print(f"{start} -> {target}: unreachable")


def main() -> None:
    parser = build_argument_parser()
    args = parser.parse_args()

    try:
        default_graph_file = Path(__file__).with_name("sample_graph.json")
        graph_file = args.graph_file if args.graph_file else default_graph_file

        graph = load_graph_from_json(graph_file)
        run_demo(graph, args.start)
    except (KeyError, TypeError, ValueError, FileNotFoundError) as exc:
        raise SystemExit(f"Error: {exc}") from exc


if __name__ == "__main__":
    main()

