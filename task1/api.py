# api.py
import random
from models import User, WasteFactory, RewardShop
from data_structures import UserLeaderboardBST
from data_manager import initialize_network, load_users, save_users
from algorithm import dijkstra_find_station


class Api:
    """The interface layer between the Python backend and the PyWebView frontend GUI."""

    def __init__(self):
        self.users = load_users()
        self.current_user = None
        self.graph_data = initialize_network()
        self.waste_types = WasteFactory.get_supported_types()

    def auth_user(self, action, user_id, name, password):
        """Handle user registration and login."""
        if action == "register":
            if user_id in self.users: return {"error": "User ID already exists."}
            if not password or len(password) < 6: return {"error": "Password must be at least 6 characters long."}
            self.users[user_id] = User(user_id=user_id, name=name, password=password)
            save_users(self.users)
            return {"status": "success", "msg": "Registered successfully. Please login."}
        elif action == "login":
            if user_id not in self.users or not self.users[user_id].verify_password(password):
                return {"error": "Invalid ID or password."}
            self.current_user = self.users[user_id]
            return {"status": "success"}

    def update_profile(self, new_name):
        """Update current user's display name."""
        if not self.current_user: return {"error": "Not logged in"}
        self.current_user.name = new_name
        save_users(self.users)
        return {"status": "success"}

    def delete_account(self):
        """Remove the current user's account from the system."""
        if self.current_user:
            del self.users[self.current_user.user_id]
            self.current_user = None
            save_users(self.users)
            return {"status": "success"}

    def get_user_data(self):
        """Retrieve user details for frontend display."""
        if not self.current_user: return None
        return {
            "id": self.current_user.user_id,
            "name": self.current_user.name,
            "points": self.current_user.points,
            "history": [item["record"] for item in self.current_user._recycling_history.get_all_records()]
        }

    def get_waste_types(self):
        """Fetch all supported waste categories."""
        return self.waste_types

    def calculate_route_and_dispose(self, lat, lng, waste_category, qty):
        """Execute route calculation, simulate queuing, process disposal, and award points."""
        if not self.current_user: return {"error": "Not logged in."}

        res = dijkstra_find_station(float(lat), float(lng), waste_category, self.graph_data)
        if "error" in res: return res

        station_obj = res.pop('_station_obj')

        # Simulate station queuing mechanism
        station_obj.queue.enqueue(self.current_user.user_id)

        # Utilize factory pattern to instantiate the waste item
        waste_item = WasteFactory.create_item(waste_category, float(qty))
        pts = station_obj.process_item(waste_item)

        station_obj.queue.dequeue()

        # Update user's records and points
        record_text = f"Recycled {qty} units of {waste_category} at {station_obj.name} ({station_obj.station_type}). (+{pts:.1f} pts)"
        self.current_user.add_points(record_text, pts)
        save_users(self.users)

        res["earned_points"] = pts
        return res

    def undo_action(self):
        """Undo the last disposal entry."""
        if not self.current_user: return {"error": "Not logged in"}
        success, msg = self.current_user.undo_last_action()
        if success: save_users(self.users)
        return {"status": "success" if success else "error", "msg": msg}

    def get_leaderboard(self):
        """Construct a BST to generate a sorted leaderboard based on user points."""
        bst = UserLeaderboardBST()
        for u in self.users.values():
            bst.insert(u)
        return bst.get_inorder_ranking()

    def get_shop_items(self):
        """Retrieve available redemption items."""
        return RewardShop.ITEMS

    def redeem_item(self, item_id):
        """Exchange points for a selected reward."""
        if not self.current_user: return {"error": "Not logged in"}
        item = next((i for i in RewardShop.ITEMS if i["id"] == item_id), None)
        if not item: return {"error": "Item not found."}

        if self.current_user.deduct_points(item["cost"], item["name"]):
            save_users(self.users)
            return {"status": "success", "msg": f"Successfully redeemed {item['name']}!"}
        else:
            return {"error": "Insufficient points."}