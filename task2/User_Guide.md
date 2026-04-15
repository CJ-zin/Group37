# User Guide: How to Run `code.py`

## 1. What This Project Includes

This project contains:

- `code.py` — the Python implementation of Dijkstra's shortest path algorithm
- `sample_graph.json` — a ready-to-run graph example in JSON format
- `Rename.md` — the report explaining the graph data structure and the algorithm
- `User_Guide.md` — this guide for running the code

## 2. Requirements

- Python **3.10** or newer
- Windows PowerShell, Command Prompt, or another terminal

No third-party packages are required. The script uses only the Python standard library.

## 3. How to Run the Code

### Option A: Run from the project folder

Open PowerShell and go to the folder that contains the files:

```powershell
cd "D:\save cjy"
python .\code.py
```

### Option B: Run with the full file path

If you do not want to change folders, you can run:

```powershell
python "D:\save cjy\code.py"
```

### If `python` is not recognized

Try the Python launcher:

```powershell
py .\code.py
```

## 4. How to Run a Custom Graph

You are no longer limited to the built-in example. `code.py` can now read **any graph** stored as a JSON adjacency list.

### JSON format

Use this structure:

```json
{
  "A": {"B": 2, "D": 1},
  "B": {"A": 2, "C": 3},
  "C": {"B": 3}
}
```

- Each key is a vertex name
- Each inner object maps a neighbor to the edge weight
- All weights must be **non-negative**

### Example file included in the project

The file `sample_graph.json` contains the same graph used in the report.

### Run with a custom graph file

```powershell
python .\code.py --graph-file .\sample_graph.json --start A
```

You can replace `sample_graph.json` with your own JSON file.

### Change the start vertex

If you want to compute shortest paths from another vertex, use `--start`:

```powershell
python .\code.py --graph-file .\sample_graph.json --start B
```

## 5. What the Script Does

When you run `code.py`, it will:

1. Load `sample_graph.json` by default, or a custom graph from a JSON file if `--graph-file` is used
2. Print an ASCII graph sketch first
3. Print the shortest-path route from the chosen start vertex to every other vertex

## 6. Expected Output Summary

The shortest distances from `A` should be:

- `A = 0`
- `B = 2`
- `C = 5`
- `D = 1`
- `E = 4`
- `F = 5`

A successful run should show route lines such as:

- `A -> B`
- `A -> D`
- `A -> E`
- `A -> B -> C`
- `A -> E -> F`

It will also show a layered ASCII graph visualization before the route list.

## 7. Troubleshooting

### Problem: `python` command not found

- Install Python from the official website
- Make sure **Add Python to PATH** is enabled during installation
- Or use `py` instead of `python`

### Problem: Output looks strange in the terminal

If your terminal encoding is not UTF-8, you can switch to UTF-8 in PowerShell:

```powershell
chcp 65001
```

### Problem: The script raises an error about negative weights

Dijkstra's algorithm only works with **non-negative edge weights**. If you want to use negative weights, you must switch to another algorithm such as Bellman-Ford.

## 8. Video Link

**5-minute introduction video:** [Insert your video URL here]

### Recommended video outline

A clear 5-minute video can show:

1. The report title and goal
2. The graph concept and Dijkstra's idea
3. The `code.py` file structure
4. Running the script in the terminal
5. The final output and a short conclusion

## 9. Quick Checklist Before Submission

- [ ] `code.py` runs successfully
- [ ] `Rename.md` contains the report
- [ ] `User_Guide.md` explains how to run the code
- [ ] `sample_graph.json` is included if you want to demonstrate custom graph input
- [ ] The video link has been replaced with the final uploaded URL

