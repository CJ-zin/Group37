# Hong Kong Smart Recycling Network System

### COMP2090SEF / COMP8090SEF Course Project

> This is the final submission version of the project.

## Project Background and Problem Definition

Data from the Hong Kong Environmental Protection Department shows that in 2024, Hong Kong's recycling rate was only 34%, while the municipal solid waste disposal volume reached 3.85 million tonnes. A major pain point leading to low citizen participation is the uneven distribution of recycling points and the lack of an incentive mechanism.

This project aims to develop an application based on OOP to address this practical issue. The system simulates Hong Kong's smart recycling network, improving the recycling rate by rewarding users with recycling points, while providing a smart route planning system to help users find the best recycling station.

## System Core Architecture and Implementation

This system applies all Object-Oriented Programming (OOP) core concepts required by the course and implements a variety of advanced data structures and algorithms:

### 1. Object-Oriented Programming (OOP)
* **Abstraction & Inheritance:** Implemented abstract base classes `WasteItem` and `RecyclingStation`, and derived multiple concrete subclasses (such as `PlasticWaste`, `BatteryWaste`, as well as `ResidentialStation` and `MallStation` with varying point multipliers), encapsulating their respective point calculation and processing logic.
* **Encapsulation:** The `User` class protects core user data through private attributes (such as `_points` and `_recycling_history`), and updates states through secure methods (such as `add_points` and `deduct_points`).
* **Polymorphism:** The `process_item()` method of the recycling station can dynamically accept any subclass of `WasteItem` and automatically invoke the correctly overridden method to calculate points.

### 2. Core Data Structures
* **Linked List:** Used to chronologically record and retrieve the user's recycling activity history.
* **Stack:** Used to provide an undo function, allowing users to safely roll back their most recently submitted accidental recycling operation.
* **Queue:** Used to simulate the queuing mechanism of multiple users at popular recycling stations.
* **Binary Search Tree (BST):** Used to manage user nodes and quickly generate a top-user leaderboard sorted by points via an in-order traversal.
* **Min Heap:** Acts as a priority queue, providing underlying sorting and access support for the core shortest path algorithm.

### 3. Graph Algorithms & Smart Recommendations
* **Graph Network Modeling:** Parses real open-source map data of Hong Kong (OpenStreetMap), transforming road intersections and recycling station geographical distributions into a weighted graph structure.
* **Dijkstra's Shortest Path Algorithm:** Based on the user's current coordinates, intelligently filters recycling stations that support a specific waste type, calculates the nearest recycling station, and generates a complete map navigation route.

### 4. Extensions & Advanced Features
* **Data Persistence:** Implemented JSON file system I/O to permanently save basic user information, salted and hashed passwords, point balances, and graph network topology caches.
* **Point Redemption Shop:** Introduced a mechanism that consumes points to redeem actual rewards (such as supermarket coupons, MTR discounts, etc.).
* **Graphical User Interface (GUI):** Improved from a console application to a visually appealing GUI. It utilizes `pywebview` combined with Vue 3 and Leaflet.js to build a highly interactive desktop map application, providing visual click-to-select locations, route drawing, and state tracking.

## File Structure

* `models.py`: Contains all business logic models (User entities, Waste factory, various Recycling stations, and the Reward shop).
* `data_structures.py`: Contains foundational data structures implemented from scratch (Linked List, Stack, Queue, Min Heap, and Binary Search Tree).
* `algorithm.py`: Contains pathfinding core logic and the specific implementation of Dijkstra's algorithm.
* `data_manager.py`: Handles map file parsing (OSM) and local JSON persistence read/write operations.
* `api.py`: Communication interface between the frontend GUI and the backend Python objects.
* `main.py`: The starting entry point of the desktop GUI application.
* `gui/index.html`: The user interaction interface and dynamic map rendering code based on the frontend technology stack.

## How to Run

1. Ensure you have Python 3.10 installed.
2. Install the required project dependencies.
   ```bash
   pip install -r requirements.txt
   ```
3. Clone this repository, and ensure that the `./data` directory contains at least `hong-kong-260322.osm` and `wasteless250918.csv`.
4. Run the main application in your terminal:
   ```bash
   python main.py
   ```
#Video Link: https://www.bilibili.com/video/BV1tpdvBSEzC/?vd_source=315e748f4594bd478154f8067b34da3b
