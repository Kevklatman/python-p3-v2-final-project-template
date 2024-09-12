# lib/helpers.py

from models.scout import Scout
from models.players import Player
from models.evaluations import Evaluation


def add_scout():
    print("Add a new scout")
    name = input("Enter scout name: ")
    region = input("Enter scout region: ")
    
    scout = Scout.create(name, region)
    print(f"Scout {scout.name} ({scout.id}) added successfully.")
    
    while True:
        print("What would you like to do next?")
        print("0. Exit program")
        print("1. Add another scout")
        print("2. View all scouts")
        print("3. Return to main menu")
        choice = input("> ")
        
        if choice == "0":
            exit_program()
            break
        if choice == "1":
            add_scout()
            break
        if choice == "2":
            view_scouts()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")



def add_player():
    print("Add a new player")
    name = input("Enter player name: ")
    position = input("Enter player position: ")
    age = int(input("Enter player age: "))
    team = input("Enter player team: ")
    
    player = Player.create(name, position, age, team)
    print(f"Player {player.name} ({player.id}) added successfully.")
    
    while True:
        print("What would you like to do next?")
        print("0. Exit program")
        print("1. Add another player")
        print("2. Return to main menu")
        choice = input("> ")
        
        if choice == "0":
            exit_program()
            break
        if choice == "1":
            add_player()
            break
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")



def add_evaluation():
    print("Add a new evaluation")
    scout_id = int(input("Enter scout ID: "))
    player_id = int(input("Enter player ID: "))
    date = input("Enter evaluation date (YYYY-MM-DD): ")
    grade = input("Enter evaluation grade: ")
    notes = input("Enter evaluation notes: ")
    player_comparison = input("Enter comparison: ")
    
    evaluation = Evaluation.create(scout_id, player_id, date, grade, notes, player_comparison)
    print(f"Evaluation {evaluation.id} added successfully.")
    
    while True:
        print("What would you like to do next?")
        print("0. Exit program")
        print("1. Add another evaluation for this scout")
        print("2. Add a new evaluation")
        print("3. Return to main menu")
        choice = input("> ")
        
        if choice == "0":
            exit_program()
            break
        elif choice == "1":
            add_evaluation_for_scout(scout_id)
            break
        elif choice == "2":
            add_evaluation()
            break
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


def add_evaluation_for_scout(scout_id):
    print(f"Add another evaluation for scout with ID: {scout_id}")
    player_id = int(input("Enter player ID: "))
    date = input("Enter evaluation date (YYYY-MM-DD): ")
    grade = input("Enter evaluation grade: ")
    notes = input("Enter evaluation notes: ")
    player_comparison = input("Enter comparison: ")
    
    evaluation = Evaluation.create(scout_id, player_id, date, grade, notes, player_comparison)
    print(f"Evaluation {evaluation.id} added successfully.")



def view_scouts():
    print("All Scouts:")
    scouts = Scout.get_all()
    for scout in scouts:
        print(f"ID: {scout.id}, Name: {scout.name}, Region: {scout.region}")


def view_players():
    print("All Players:")
    players = Player.get_all()
    for player in players:
        print(f"ID: {player.id}, Name: {player.name}, Position: {player.position}, Age: {player.age}, Team: {player.team}")


def view_evaluations():
    print("All Evaluations:")
    evaluations = Evaluation.get_all()
    for evaluation in evaluations:
        print(f"ID: {evaluation.id}, Scout ID: {evaluation.scout_id}, Player ID: {evaluation.player_id}, Date: {evaluation.date}, Grade: {evaluation.grade}, Notes: {evaluation.notes} similar to {evaluation.player_comparison}")


def update_evaluation():
    print("Update an evaluation")
    eval_id = int(input("Enter evaluation ID: "))
    
    evaluation = Evaluation.get_by_id(eval_id)
    if evaluation:
        print(f"Updating evaluation {eval_id}")
        
        scout_id = input(f"Enter new scout ID (current: {evaluation.scout_id}): ")
        player_id = input(f"Enter new player ID (current: {evaluation.player_id}): ")
        date = input(f"Enter new evaluation date (YYYY-MM-DD) (current: {evaluation.date}): ")
        grade = input(f"Enter new evaluation grade (current: {evaluation.grade}): ")
        notes = input(f"Enter new evaluation notes (current: {evaluation.notes}): ")
        player_comparison = input(f"Enter new player comparison (current: {evaluation.player_comparison}): ")
        
        #updated evaluation attributes
        evaluation.update(
            scout_id=int(scout_id) if scout_id else None,
            player_id=int(player_id) if player_id else None,
            date=date if date else None,
            grade=grade if grade else None,
            notes=notes if notes else None,
            player_comparison=player_comparison if player_comparison else None
        )
        
        print(f"Evaluation {eval_id} updated successfully.")
    else:
        print(f"Evaluation {eval_id} not found.")

def delete_player():
    print("Delete a player")
    player_id = int(input("Enter player ID: "))
    
    player = Player.get_by_id(player_id)
    if player:
        player.delete()
        print(f"Player {player.name} ({player.id}) deleted successfully.")
    else:
        print(f"Player with ID {player_id} not found.")


def view_evaluations_by_scout_name():
    print("View evaluations by scout name")
    scout_name = input("Enter scout name: ")
    
    evaluations = Evaluation.get_by_scout_name(scout_name)
    if evaluations:
        print(f"Evaluations by scout {scout_name}:")
        for evaluation in evaluations:
            print(f"- Evaluation ID: {evaluation.id}")
            print(f"  Player ID: {evaluation.player_id}")
            print(f"  Date: {evaluation.date}")
            print(f"  Grade: {evaluation.grade}")
            print(f"  Notes: {evaluation.notes}")
            print(f"  Player Comparison: {evaluation.player_comparison}")
            print()
    else:
        print(f"No evaluations found for scout {scout_name}")



def exit_program():
    print("Goodbye!")
    exit()