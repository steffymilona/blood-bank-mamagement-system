"""
Blood Bank Management System
A simple console application to manage donors, blood stock and requests.
Data is saved in data.json so nothing is lost when the program closes.
"""

import json
import os
from datetime import datetime

DATA_FILE = "data.json"
BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


# ---------- Data handling ----------
def default_data():
    return {
        "donors": [],
        "stock": {group: 0 for group in BLOOD_GROUPS},
        "transactions": [],
    }


def load_data():
    if not os.path.exists(DATA_FILE):
        return default_data()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for group in BLOOD_GROUPS:
            data["stock"].setdefault(group, 0)
        return data
    except (json.JSONDecodeError, KeyError):
        print("Warning: data file is damaged. Starting with empty data.")
        return default_data()


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ---------- Input helpers ----------
def ask_int(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = int(input(prompt).strip())
            if minimum is not None and value < minimum:
                print(f"Please enter a number of at least {minimum}.")
                continue
            if maximum is not None and value > maximum:
                print(f"Please enter a number no greater than {maximum}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def ask_blood_group():
    while True:
        group = input(f"Blood group {BLOOD_GROUPS}: ").strip().upper()
        if group in BLOOD_GROUPS:
            return group
        print("Invalid blood group. Try again.")


def ask_phone():
    while True:
        phone = input("Phone number: ").strip()
        if phone.isdigit() and 7 <= len(phone) <= 15:
            return phone
        print("Enter digits only (7 to 15 digits).")


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ---------- Features ----------
def add_donor(data):
    print("\n--- Add Donor ---")
    name = input("Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    age = ask_int("Age: ", 1, 120)
    if age < 18 or age > 65:
        print("Donor must be between 18 and 65 years old.")
        return
    group = ask_blood_group()
    phone = ask_phone()

    donor_id = max((d["id"] for d in data["donors"]), default=0) + 1
    data["donors"].append(
        {
            "id": donor_id,
            "name": name,
            "age": age,
            "blood_group": group,
            "phone": phone,
            "last_donation": None,
        }
    )
    save_data(data)
    print(f"Donor added successfully. Donor ID: {donor_id}")


def view_donors(data, group_filter=None):
    donors = data["donors"]
    if group_filter:
        donors = [d for d in donors if d["blood_group"] == group_filter]
    if not donors:
        print("No donors found.")
        return
    print(f"\n{'ID':<5}{'Name':<22}{'Age':<6}{'Group':<8}{'Phone':<16}{'Last Donation'}")
    print("-" * 75)
    for d in donors:
        print(
            f"{d['id']:<5}{d['name']:<22}{d['age']:<6}{d['blood_group']:<8}"
            f"{d['phone']:<16}{d['last_donation'] or 'Never'}"
        )


def search_donors_by_group(data):
    print("\n--- Search Donors by Blood Group ---")
    group = ask_blood_group()
    view_donors(data, group)


def record_donation(data):
    print("\n--- Record Donation ---")
    if not data["donors"]:
        print("No donors registered yet. Add a donor first.")
        return
    view_donors(data)
    donor_id = ask_int("Enter Donor ID: ", 1)
    donor = next((d for d in data["donors"] if d["id"] == donor_id), None)
    if donor is None:
        print("Donor not found.")
        return
    units = ask_int("Units donated (1-2): ", 1, 2)

    data["stock"][donor["blood_group"]] += units
    donor["last_donation"] = now()
    data["transactions"].append(
        {
            "date": now(),
            "type": "donation",
            "blood_group": donor["blood_group"],
            "units": units,
            "person": donor["name"],
        }
    )
    save_data(data)
    print(f"{units} unit(s) of {donor['blood_group']} added to stock.")


def view_stock(data):
    print("\n--- Blood Stock ---")
    print(f"{'Group':<10}{'Units':<8}")
    print("-" * 18)
    for group in BLOOD_GROUPS:
        units = data["stock"][group]
        warning = "  (LOW)" if units < 3 else ""
        print(f"{group:<10}{units:<8}{warning}")


def issue_blood(data):
    print("\n--- Issue Blood to Patient ---")
    patient = input("Patient name: ").strip()
    if not patient:
        print("Patient name cannot be empty.")
        return
    group = ask_blood_group()
    available = data["stock"][group]
    if available == 0:
        print(f"Sorry, no {group} blood is available.")
        return
    units = ask_int(f"Units required (available: {available}): ", 1)
    if units > available:
        print("Not enough stock available.")
        return

    data["stock"][group] -= units
    data["transactions"].append(
        {
            "date": now(),
            "type": "issue",
            "blood_group": group,
            "units": units,
            "person": patient,
        }
    )
    save_data(data)
    print(f"{units} unit(s) of {group} issued to {patient}.")


def view_transactions(data):
    print("\n--- Transaction History ---")
    if not data["transactions"]:
        print("No transactions yet.")
        return
    print(f"{'Date':<18}{'Type':<10}{'Group':<8}{'Units':<7}{'Person'}")
    print("-" * 60)
    for t in data["transactions"]:
        print(
            f"{t['date']:<18}{t['type']:<10}{t['blood_group']:<8}"
            f"{t['units']:<7}{t['person']}"
        )


def delete_donor(data):
    print("\n--- Delete Donor ---")
    donor_id = ask_int("Enter Donor ID to delete: ", 1)
    for donor in data["donors"]:
        if donor["id"] == donor_id:
            confirm = input(f"Delete {donor['name']}? (y/n): ").strip().lower()
            if confirm == "y":
                data["donors"].remove(donor)
                save_data(data)
                print("Donor deleted.")
            else:
                print("Cancelled.")
            return
    print("Donor not found.")


# ---------- Main menu ----------
def main():
    data = load_data()
    actions = {
        "1": add_donor,
        "2": view_donors,
        "3": search_donors_by_group,
        "4": record_donation,
        "5": view_stock,
        "6": issue_blood,
        "7": view_transactions,
        "8": delete_donor,
    }

    while True:
        print("\n===== BLOOD BANK MANAGEMENT SYSTEM =====")
        print("1. Add donor")
        print("2. View all donors")
        print("3. Search donors by blood group")
        print("4. Record a donation")
        print("5. View blood stock")
        print("6. Issue blood to patient")
        print("7. View transaction history")
        print("8. Delete donor")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(data)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()