import os
import ast

BALANCE_FILE = "balance.txt"
WAREHOUSE_FILE = "warehouse.txt"
OPERATIONS_FILE = "operations.txt"


def show_commands():
    print("\nAvailable commands:")
    print("Balance")
    print("Sale")
    print("Purchase")
    print("Account")
    print("List")
    print("Warehouse")
    print("Review")
    print("End\n")


def load_data(filename, default):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                data = f.read()
                return ast.literal_eval(data)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return default
    else:
        return default


def save_data(filename, data):
    try:
        with open(filename, "w") as f:
            f.write(str(data))
    except Exception as e:
        print(f"Error saving {filename}: {e}")


def main():
    balance = load_data(BALANCE_FILE, 0.0)
    warehouse = load_data(WAREHOUSE_FILE, {})
    operations = load_data(OPERATIONS_FILE, [])

    show_commands()

    while True:
        command = input("\nEnter a command: ").strip().lower()

        if command == "balance":
            try:
                amount = float(input("Enter amount to add/subtract: "))
                balance += amount
                operations.append(f"Balance changed by {amount}, new balance: {balance}")
            except ValueError:
                print("Invalid amount!")

        elif command == "sale":
            product = input("Enter product name: ").strip()
            try:
                price = float(input("Enter price per unit: "))
                quantity = int(input("Enter quantity: "))
                if product not in warehouse or warehouse[product]['quantity'] < quantity:
                    print("Not enough stock for this sale.")
                else:
                    total = price * quantity
                    balance += total
                    warehouse[product]['quantity'] -= quantity
                    operations.append(f"Sold {quantity} of {product} at {price} each. Total: {total}")
            except ValueError:
                print("Invalid input!")

        elif command == "purchase":
            product = input("Enter product name: ").strip()
            try:
                price = float(input("Enter price per unit: "))
                quantity = int(input("Enter quantity: "))
                total = price * quantity
                if total > balance:
                    print("Insufficient funds for this purchase.")
                else:
                    balance -= total
                    if product not in warehouse:
                        warehouse[product] = {'price': price, 'quantity': quantity}
                    else:
                        warehouse[product]['quantity'] += quantity
                        warehouse[product]['price'] = price
                    operations.append(f"Purchased {quantity} of {product} at {price} each. Total: {total}")
            except ValueError:
                print("Invalid input!")

        elif command == "account":
            print(f"Current account balance: {balance}")

        elif command == "list":
            if not warehouse:
                print("Warehouse is empty.")
            else:
                print("Warehouse Inventory:")
                for product, details in warehouse.items():
                    print(f"{product}: {details['quantity']} units, Price: {details['price']}")

        elif command == "warehouse":
            product = input("Enter product name: ").strip()
            if product in warehouse:
                details = warehouse[product]
                print(f"{product}: {details['quantity']} units, Price: {details['price']}")
            else:
                print(f"{product} not found in warehouse.")

        elif command == "review":
            try:
                from_idx = input("Enter start index: ")
                to_idx = input("Enter end index: ")

                start = int(from_idx) if from_idx else 0
                end = int(to_idx) if to_idx else len(operations)

                if start < 0 or end > len(operations) or start > end:
                    print("Invalid index range.")
                else:
                    for op in operations[start:end]:
                        print(op)
            except ValueError:
                print("Invalid index. Please enter valid integers.")

        elif command == "end":
            save_data(BALANCE_FILE, balance)
            save_data(WAREHOUSE_FILE, warehouse)
            save_data(OPERATIONS_FILE, operations)
            print("All data saved.")
            break

        else:
            print("Invalid command!")

        show_commands()


if __name__ == "__main__":
    main()