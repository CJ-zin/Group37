# models.py
from abc import ABC, abstractmethod
from data_structures import LinkedList
import datetime


# Abstraction and Inheritance
class WasteItem(ABC):
    """Abstract base class for waste items"""

    @abstractmethod
    def classify(self):
        """Return the category of the waste item"""
        pass

    @abstractmethod
    def calculate_points(self, weight: float) -> float:
        """Calculate points based on weight"""
        pass


class PlasticBottle(WasteItem):
    """Plastic Bottle class"""

    def classify(self):
        return "Plastic"

    def calculate_points(self, weight: float) -> float:
        # Plastics earn 10 points per kg
        return weight * 10.0


class OrganicFoodWaste(WasteItem):
    """Organic Food Waste subclass"""

    def classify(self):
        return "Organic Food Waste"

    def calculate_points(self, weight: float) -> float:
        # Organic food waste earns 2 points per kg
        return weight * 2.0


# Encapsulation
class User:
    """User class"""

    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name
        self._points = 0.0  # Private attribute: points
        self._recycling_history = LinkedList()  # Private attribute: history records

    # Getter for points
    @property
    def points(self):
        return self._points

    def add_points(self, points_to_add: float):
        """Safely add points"""
        if points_to_add > 0:
            self._points += points_to_add

    def add_history_record(self, record_detail: str):
        """Insert a history record into the linked list"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._recycling_history.append(f"[{timestamp}] {record_detail}")

    def print_history(self):
        """Print user's recycling history"""
        print(f"\n--- Recycling History for {self.name} ---")
        if self._recycling_history.is_empty():
            print("No recycling records available.")
        else:
            records = self._recycling_history.get_all_records()
            for record in records:
                print(record)
        print(f"Current Total Points: {self.points:.2f}")
        print("---------------------------------")


# Core processing class (Demonstrates Polymorphism)
class RecyclingStation:
    """Recycling Station class"""

    def __init__(self, station_id: str, location: str):
        self.station_id = station_id
        self.location = location

    def process_item(self, user: User, item: WasteItem, weight: float):
        """
        Polymorphism demonstration:
        Passing different WasteItem subclasses will automatically call their respectively overridden calculate_points methods.
        """
        category = item.classify()
        earned_points = item.calculate_points(weight)

        # Update user information
        user.add_points(earned_points)
        record = f"Recycled {weight:.2f}kg of {category} at {self.location}, earned {earned_points:.2f} points."
        user.add_history_record(record)

        print(f"\n[System] Disposal successful! You have disposed of {weight:.2f}kg of {category}.")
        print(f"[System] Points earned this time: {earned_points:.2f}. Current total points: {user.points:.2f}")