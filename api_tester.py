import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/crud"


def menu():
    print("\nWhat would you like to do?")
    print("1. Get all employees")
    print("2. Add new employee")
    print("3. Update employee")
    print("4. Delete employee")
    print("5. Exit")
    return input("Choose: ")


def test_employee_api():
    while True:
        choice = menu()

        if choice == '1':
            res = requests.get(f"{BASE_URL}/employees")
            print(json.dumps(res.json(), indent=2))

        elif choice == '2':
            print("\nAdd New Employee")
            eid = int(input("Eid (must exist in PERSON): "))
            title = input("Title: ")
            rank = input("Rank: ")
            super_id = int(input("Supervisor ID: "))

            payload = {
                "Eid": eid,
                "Title": title,
                "Emp_rank": rank,
                "Super_id": super_id
            }

            res = requests.post(f"{BASE_URL}/employees", json=payload)
            print(res.json())

        elif choice == '3':
            eid = int(input("Employee ID to update: "))
            title = input("New Title: ")
            rank = input("New Rank: ")
            super_id = int(input("New Supervisor ID: "))

            payload = {
                "Title": title,
                "Emp_rank": rank,
                "Super_id": super_id
            }

            res = requests.put(f"{BASE_URL}/employees/{eid}", json=payload)
            print(res.json())

        elif choice == '4':
            eid = int(input("Employee ID to delete: "))
            res = requests.delete(f"{BASE_URL}/employees/{eid}")
            print(res.json())

        elif choice == '5':
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    test_employee_api()
