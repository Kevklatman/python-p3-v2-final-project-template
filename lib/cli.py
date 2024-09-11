# lib/cli.py
from helpers import (
    exit_program,
    add_scout,
    add_player,
    add_evaluation,
    view_scouts,
    view_players,
    view_evaluations,
    update_evaluation,
    delete_player
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            add_scout()
        elif choice == "2":
            add_player()
        elif choice == "3":
            add_evaluation()
        elif choice == "4":
            view_scouts()
        elif choice == "5":
            view_players()
        elif choice == "6":
            view_evaluations()
        elif choice == "7":
            update_evaluation()
        elif choice == "8":
            delete_player()  # Add the delete player option
        else:
            print("Invalid choice")


def menu():
    print("Baseball Scout Manager CLI")
    print("---------------------------")
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Add a scout")
    print("2. Add a player")
    print("3. Add an evaluation")
    print("4. View all scouts")
    print("5. View all players")
    print("6. View all evaluations")
    print("7. Update an evaluation")
    print("8. Delete a player")  # Add the delete player option to the menu


if __name__ == "__main__":
    main()
