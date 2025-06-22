#!/usr/bin/env python3

import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

DATA_FILE = Path("incubator_data.json")
LOG_FILE = Path("incubator_log.txt")
DATE_FMT = "%Y-%m-%d"

RESET = "\033[0m"
def paint(txt, code):
    return f"\033[{code}m{txt}{RESET}"

PALETTE = {
    "empty": "2",
    "new": "37",
    "7day": "33;1",
    "14day": "36;1",
    "18day": "31;5;7",
    "done": "32;1",
}

def load_state():
    if DATA_FILE.exists():
        with DATA_FILE.open() as f:
            raw = json.load(f)
        return [datetime.strptime(ts, DATE_FMT).date() if ts else None for ts in raw]
    return [None] * 8

def save_state(slots):
    with DATA_FILE.open("w") as f:
        json.dump([dt.strftime(DATE_FMT) if dt else None for dt in slots], f, indent=2)

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_FILE.open("a") as log:
        log.write(f"[{timestamp}] {message}\n")

def add(slot_idx, when):
    if when > datetime.now().date():
        print("Date cannot be in the future.")
        return
    slots = load_state()
    if slots[slot_idx] is not None:
        print(f"Slot {slot_idx + 1} already occupied.")
        return
    slots[slot_idx] = when
    save_state(slots)
    log_event(f"Added egg to slot {slot_idx + 1} on {when}")

def remove(slot_idx):
    slots = load_state()
    if slots[slot_idx] is None:
        print(f"Slot {slot_idx + 1} already empty.")
        return
    removed_date = slots[slot_idx]
    slots[slot_idx] = None
    save_state(slots)
    log_event(f"Removed egg from slot {slot_idx + 1} (was added on {removed_date})")

def age_in_days(d):
    return (datetime.now().date() - d).days

def color_for_age(days):
    if days < 7:
        return PALETTE["new"]
    elif days < 14:
        return PALETTE["7day"]
    elif days < 18:
        return PALETTE["14day"]
    elif days < 21:
        return PALETTE["18day"]
    else:
        return PALETTE["done"]

def render():
    slots = load_state()
    cells = []
    for i, dt in enumerate(slots, 1):
        if dt is None:
            cells.append(paint(f" {i:>2} ▢ EMPTY ", PALETTE["empty"]))
        else:
            days = age_in_days(dt)
            hatch_day = dt + timedelta(days=21)
            cell_txt = f" {i:>2} \U0001F95A {days:02}d (H: {hatch_day.strftime('%m-%d')}) "
            cells.append(paint(cell_txt, color_for_age(days)))
    horiz = "+" + "+".join(["-" * 19] * 4) + "+"
    lines = [horiz]
    for row in (cells[:4], cells[4:]):
        lines.append("|" + "|".join(row) + "|")
        lines.append(horiz)
    print("\n".join(lines))

def parse_date(s):
    formats = ["%Y-%m-%d", "%m-%d-%Y", "%m/%d/%Y", "%m-%d", "%m/%d"]
    for fmt in formats:
        try:
            dt = datetime.strptime(s, fmt)
            if fmt in ["%m-%d", "%m/%d"]:
                dt = dt.replace(year=datetime.now().year)
            return dt.date()
        except ValueError:
            continue
    print("Date must be in format YYYY-MM-DD, MM-DD-YYYY, MM/DD/YYYY, MM-DD, or MM/DD")
    return None

def auto_refresh():
    while True:
        print("\033[2J\033[H", end="")
        render()
        print("\nPress Ctrl+C to exit auto-refresh.\n")
        time.sleep(3600)

def menu():
    while True:
        print("\n--- INCUBATOR MENU ---")
        print("[1] Show incubator once")
        print("[2] Add egg")
        print("[3] Remove egg")
        print("[4] Start auto-refresh")
        print("[5] Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            render()
        elif choice == "2":
            slot_input = input("Enter slot number (1-8): ").strip()
            if not slot_input.isdigit() or not (1 <= int(slot_input) <= 8):
                print("Invalid slot.")
                continue
            slot = int(slot_input)
            date_input = input("Enter date (YYYY-MM-DD, MM-DD-YYYY, MM/DD/YYYY, MM-DD, or MM/DD) or leave blank for today: ").strip()
            when = parse_date(date_input) if date_input else datetime.now().date()
            if when:
                add(slot - 1, when)
        elif choice == "3":
            slot_input = input("Enter slot number (1-8): ").strip()
            if not slot_input.isdigit() or not (1 <= int(slot_input) <= 8):
                print("Invalid slot.")
                continue
            remove(int(slot_input) - 1)
        elif choice == "4":
            auto_refresh()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def handle_args():
    args = sys.argv[1:]
    if not args:
        menu()
        return

    cmd = args[0].lower()
    if cmd == "help":
        print("""
Usage:
  python incubator.py                # Start interactive menu
  python incubator.py show           # Display incubator grid once
  python incubator.py add <slot> [date]   # Add egg to slot (1–8), optional date formats:
                                          #   YYYY-MM-DD
                                          #   MM-DD-YYYY
                                          #   MM/DD/YYYY
                                          #   MM-DD
                                          #   MM/DD
  python incubator.py remove <slot> # Remove egg from slot (1–8)
  python incubator.py help          # Show this help message
""")
    elif cmd == "show":
        render()
    elif cmd == "add" and len(args) >= 2:
        slot = int(args[1]) - 1
        date = parse_date(args[2]) if len(args) > 2 else datetime.now().date()
        if 0 <= slot < 8 and date:
            add(slot, date)
    elif cmd == "remove" and len(args) == 2:
        slot = int(args[1]) - 1
        if 0 <= slot < 8:
            remove(slot)
    else:
        print("Invalid command. Use 'python incubator.py help' for usage.")

if __name__ == "__main__":
    try:
        handle_args()
    except KeyboardInterrupt:
        print("\nExited.")
