#!/usr/bin/env python3
"""
Stargazing App Launcher
Choose between GUI and terminal versions
"""

import sys
import subprocess
import os

def main():
    print("🌟 Stargazing Information App Launcher")
    print("=" * 40)
    print("Choose your preferred interface:")
    print("1. GUI Version (Recommended)")
    print("2. Terminal Version")
    print("3. Exit")
    print()

    while True:
        try:
            choice = input("Enter your choice (1-3): ").strip()

            if choice == '1':
                print("Launching GUI version...")
                subprocess.run([sys.executable, "stargazing_gui.py"])
                break
            elif choice == '2':
                print("Launching terminal version...")
                subprocess.run([sys.executable, "stargazing_app.py"])
                break
            elif choice == '3':
                print("Goodbye! 🌟")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

        except KeyboardInterrupt:
            print("\nGoodbye! 🌟")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if name == "main":
    main()