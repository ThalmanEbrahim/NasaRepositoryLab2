#!/usr/bin/env python3
"""
Stargazing App Launcher
Choose between GUI and terminal versions
"""

# import needed modules
import sys
import subprocess
import os

def main():
    # show welcome message
    print("🌟 Stargazing Information App Launcher")
    print("=" * 40)
    print("Choose your preferred interface:")
    print("1. GUI Version (Recommended)")
    print("2. Terminal Version")
    print("3. Exit")
    print()

    # keep asking until user makes valid choice
    while True:
        try:
            # get user input
            choice = input("Enter your choice (1-3): ").strip()

            # check what user chose
            if choice == '1':
                # run gui version
                print("Launching GUI version...")
                subprocess.run([sys.executable, "stargazing_gui.py"])
                break
            elif choice == '2':
                # run terminal version
                print("Launching terminal version...")
                subprocess.run([sys.executable, "stargazing_app.py"])
                break
            elif choice == '3':
                # exit program
                print("Goodbye! 🌟")
                break
            else:
                # invalid choice
                print("Invalid choice. Please enter 1, 2, or 3.")

        except KeyboardInterrupt:
            # user pressed ctrl+c
            print("\nGoodbye! 🌟")
            break
        except Exception as e:
            # handle any errors
            print(f"Error: {e}")
            break

# run main function when script is executed
if name == "main":
    main()