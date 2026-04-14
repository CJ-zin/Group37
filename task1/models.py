# models.py
import datetime
import hashlib
import secrets
from abc import ABC, abstractmethod
from data_structures import LinkedList, Stack, Queue


class WasteItem(ABC):
    """Abstract Base Class for various types of waste items."""
    def __init__(self, qty_or_weight: float):
        self.qty = qty_or_weight

    @property
    @abstractmethod
    def category_name(self) -> str:
        pass

    @abstractmethod
    def calculate_base_points(self) -> float:
        """Polymorphic method to calculate unadjusted points based on waste type."""
        pass


class HighValueEwaste(WasteItem):
    @property
    def category_name(self): return "Regulated Electrical Equipment"
    def calculate_base_points(self): return self.qty * 100.0


class BatteryWaste(WasteItem):
    @property
    def category_name(self): return "Rechargeable Batteries"
    def calculate_base_points(self): return self.qty * 20.0


class PlasticWaste(WasteItem):
    @property
    def category_name(self): return "Plastics"
    def calculate_base_points(self): return self.qty * 6.0


class GeneralWaste(WasteItem):
    """Fallback class for standard waste types with dynamic points tracking."""
    def __init__(self, category: str, qty_or_weight: float, unit_point: float):
        super().__init__(qty_or_weight)
        self._category = category
        self.unit_point = unit_point

    @property
    def category_name(self): return self._category
    def calculate_base_points(self): return self.qty * self.unit_point


class WasteFactory:
    """Factory Pattern applied to generate appropriate WasteItem instances dynamically."""
    _rates = {
        'Barbeque Fork': 1, 'Beverage Cartons': 5, 'Clothes': 10, 'Computers': 50,
        'Fluorescent Lamp': 5, 'Food Waste': 2, 'Glass Bottles': 3, 'Metals': 8,
        'Other Description': 1, 'Paper': 4, 'Plastic Bottle': 10, 'Plastics': 6,
        'Printer Cartridges': 15, 'Rechargeable Batteries': 20,
        'Regulated Electrical Equipment': 100, 'Small Electrical and Electronic Equipment': 30
    }

    @classmethod
    def get_supported_types(cls):
        return list(cls._rates.keys())

    @classmethod
    def create_item(cls, category: str, qty: float) -> WasteItem:
        if category == 'Regulated Electrical Equipment': return HighValueEwaste(qty)
        if category == 'Rechargeable Batteries': return BatteryWaste(qty)
        if category == 'Plastics': return PlasticWaste(qty)
        rate = cls._rates.get(category, 1)
        return GeneralWaste(category, qty, rate)



class RecyclingStation(ABC):
    """Abstract Base Class representing a Recycling facility mapped to a graph node."""
    def __init__(self, st_id, name, lat, lng, node_id, waste_types):
        self.id = st_id
        self.name = name
        self.lat = lat
        self.lng = lng
        self.node = node_id
        self.waste_types = waste_types
        self.queue = Queue() # Tracking wait list

    @property
    @abstractmethod
    def multiplier(self) -> float:
        """Determines the station bonus coefficient applied to disposed waste."""
        pass

    @property
    @abstractmethod
    def station_type(self) -> str:
        pass

    def process_item(self, item: WasteItem) -> float:
        """Method demonstrating polymorphism to evaluate item base points accurately."""
        base = item.calculate_base_points()
        return base * self.multiplier


class ResidentialStation(RecyclingStation):
    @property
    def multiplier(self): return 1.0
    @property
    def station_type(self): return "Residential (1.0x)"


class MallStation(RecyclingStation):
    @property
    def multiplier(self): return 1.2
    @property
    def station_type(self): return "Mall (1.2x)"



class RewardShop:
    """Static inventory containing physical reward items."""
    ITEMS = [
        {"id": 1, "name": "MTR $10 Discount", "cost": 100},
        {"id": 2, "name": "Supermarket $50 Coupon", "cost": 450},
        {"id": 3, "name": "Eco-friendly Tote Bag", "cost": 200}
    ]


class User:
    """Core domain model representing an interacting account securely storing points and history."""
    def __init__(self, user_id: str, name: str, password: str = None, password_hash: str = None, salt: str = None):
        self.user_id = user_id
        self.name = name
        self._points = 0.0
        self._recycling_history = LinkedList()
        self._action_stack = Stack()

        if password_hash and salt:
            self._password_hash = password_hash
            self._salt = salt
        elif password:
            self._salt = secrets.token_hex(8)
            self._password_hash = self._hash_password(password, self._salt)
        else:
            raise ValueError("Must provide either a password or a password_hash/salt pair.")

    def _hash_password(self, password: str, salt: str) -> str:
        """Internal helper for salted hash creation."""
        return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

    def verify_password(self, password: str) -> bool:
        """Check provided password via hashing against stored credentials."""
        return self._password_hash == self._hash_password(password, self._salt)

    @property
    def points(self):
        """Getter for encapsulated user points."""
        return self._points

    def add_points(self, record_text: str, points_earned: float):
        """Credit points to user account and log to stack & history list."""
        self._points += points_earned
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record_detail = f"[{timestamp}] {record_text}"
        action_data = {"points": points_earned, "record": record_detail}
        self._recycling_history.append(action_data)
        self._action_stack.push(action_data)

    def deduct_points(self, amount: float, reason: str) -> bool:
        """Safely deduct points, guaranteeing the user has a sufficient balance."""
        if self._points >= amount:
            self._points -= amount
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record_detail = f"[{timestamp}] Redeemed: {reason} (-{amount} pts)"
            self._recycling_history.append({"points": -amount, "record": record_detail})
            return True
        return False

    def undo_last_action(self):
        """Revert last disposal utilizing the actions Stack."""
        if self._action_stack.is_empty():
            return False, "No recent disposal actions to undo."
        last_action = self._action_stack.pop()
        self._points -= last_action["points"]
        self._recycling_history.remove_last()
        return True, "Your last disposal has been reversed."