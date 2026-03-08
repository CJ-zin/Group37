# Hong Kong Smart Recycling Network System

### COMP2090SEF / COMP8090SEF Course Project

> This is the preliminary code submission version for the March 8 deadline. The current version represents the Pre-submission stage, focusing on establishing a robust Object-Oriented Programming (OOP) foundation and basic data structures.

## Project Background and Problem Definition

According to data from the Hong Kong Environmental Protection Department, the recycling rate in Hong Kong in 2024 was only 34%, while the municipal solid waste disposal volume reached 3.85 million tonnes. A major pain point leading to low citizen participation is the uneven distribution of recycling points and the lack of incentive mechanisms.

This project aims to develop an OOP-based application to address this real-life problem. The system will simulate a smart recycling network in Hong Kong, aiming to improve recycling rates by rewarding users with recycling points, while providing a smart route planning system to help users find the optimal recycling stations.

## Current Implementation

The current preliminary codebase has successfully implemented the core business logic using a multi-module architecture. We have strictly applied all four fundamental Object-Oriented Programming (OOP) concepts introduced in the course:


**Abstraction and Inheritance:** We implemented an abstract base class `WasteItem` and created concrete subclasses such as `PlasticBottle` and `OrganicFoodWaste`, each defining its own point calculation logic.

**Encapsulation:** The `User` class uses private attributes and getter/setter methods for properties to protect sensitive data (e.g., `_points` and `_recycling_history`).

**Polymorphism:** The `RecyclingStation.process_item()` method can dynamically accept any `WasteItem` subclass and execute the correctly overridden methods.

**Data Structures:** We implemented a custom `LinkedList` from scratch to efficiently store and retrieve users' chronological recycling history records.

### File Structure

- `models.py`: Contains all business logic models (Users, Waste, Recycling Stations).
- `data_structures.py`: Contains the foundational data structures (Linked List).
- `main.py`: The entry point for the console-based interactive application.

## Future Development Roadmap (Final Submission)

To fulfill all course requirements and build a comprehensive system, we plan to incorporate the following features and algorithms for the final submission on April 12:

### 1. Advanced OOP & Course Data Structures

- **Queue:** To simulate queuing mechanisms for multiple users at popular recycling stations.
- **Stack:** To provide an "undo" feature, allowing users to safely revert accidentally submitted operations.
- **Binary Search Tree (BST):** To manage and quickly query user profiles and point leaderboards.
- **Extended Models:** Introduce a `RewardShop` for point redemption and customized `RecyclingStation` subclasses with different reward multipliers (e.g., residential vs. shopping mall stations).

### 2. Self-Study Data Structure & Algorithm


- **Graph (Data Structure):** We will model the geographical distribution of Hong Kong's recycling stations as a graph, where nodes represent stations and edges represent walking distance/time.
- **Dijkstra's Algorithm:** We will implement Dijkstra's algorithm (using a binary heap/priority queue) to calculate the shortest path. This will provide users with smart recommendations for the nearest or most cost-effective recycling stations based on their current location.

### 3. Optional Advanced Features

* **Data Persistence:** Implement JSON file I/O for saving and loading user data and the graph network topology.
* **Graphical User Interface (GUI):** Transition from a console application to a user-friendly GUI.

## How to Run the Current Version

1. Ensure you have Python 3.x installed.
2. Clone this repository.
3. Run the main application in your terminal:

```bash
python main.py

```

## Declaration

In accordance with the University's academic honesty policy, a full declaration regarding the originality of the code and the usage of any generative AI models (such as ChatGPT, Gemini, etc.) during the development process will be included in the final written report.
