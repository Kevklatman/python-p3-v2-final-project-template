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


def add_player():
    print("Add a new player")
    name = input("Enter player name: ")
    position = input("Enter player position: ")
    age = int(input("Enter player age: "))
    team = input("Enter player team: ")
    
    player = Player.create(name, position, age, team)
    print(f"Player {player.name} ({player.id}) added successfully.")


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
        print(f"ID: {evaluation.id}, Scout ID: {evaluation.scout_id}, Player ID: {evaluation.player_id}, Date: {evaluation.date}, Grade: {evaluation.grade}, Notes: {evaluation.notes}")


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
        
        # Update the evaluation attributes
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



def exit_program():
    print("Goodbye!")
    exit()