# main.py
from models import User, PlasticBottle, OrganicFoodWaste, RecyclingStation


def display_menu():
    print("\n=================================")
    print("  Welcome to HK Smart Recycling System (MVP)  ")
    print("=================================")
    print("1. Dispose of Plastic Bottles")
    print("2. Dispose of Organic Food Waste")
    print("3. Check My Points & History")
    print("4. Exit System")
    print("=================================")


def main():
    # Initialize test data
    test_user = User(user_id="U001", name="Mr. Chan (HK Citizen)")
    station_central = RecyclingStation(station_id="S001", location="Central Center Recycling Station")

    while True:
        display_menu()
        choice = input("Please enter your choice (1-4): ")

        if choice == '1' or choice == '2':
            # Exception handling: Ensure the input is a valid numerical format
            try:
                weight_str = input("Please enter the weight of the waste (kg): ")
                weight = float(weight_str)
                if weight <= 0:
                    print("\n[Error] Weight must be greater than 0!")
                    continue
            except ValueError:
                print("\n[Error] Invalid input, please enter a valid number!")
                continue

            # Instantiate the corresponding waste object
            item = PlasticBottle() if choice == '1' else OrganicFoodWaste()

            # Recycling station processes the waste disposal (Polymorphism call)
            station_central.process_item(user=test_user, item=item, weight=weight)

        elif choice == '3':
            test_user.print_history()

        elif choice == '4':
            print("\nThank you for your contribution to environmental protection in Hong Kong. Goodbye!")
            break

        else:
            print("\n[Error] Invalid choice, please try again!")


if __name__ == "__main__":
    main()