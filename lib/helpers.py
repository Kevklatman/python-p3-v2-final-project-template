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
    
    evaluation = Evaluation.create(scout_id, player_id, date, grade, notes)
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


def exit_program():
    print("Goodbye!")
    exit()