import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open("clubs.json") as clubs_json:
        listOfClubs = json.load(clubs_json)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as competitions_json:
        listOfCompetitions = json.load(competitions_json)["competitions"]
        return listOfCompetitions


def list_of_dicts_filter(list_of_dicts, key, value):
    return [element for element in list_of_dicts if element[key] == value]


def list_of_dicts_get(list_of_dicts, key, value):
    filtered_list = list_of_dicts_filter(list_of_dicts, key, value)
    if len(filtered_list == 1):
        return filtered_list[0]
    print("Error: More than one element found")
    return None


class baseRouter:
    """
    This is the main router of the application the goal here is to make an MVC architecture using flask
    """

    def __init__(self) -> None:
        # Loading database
        self.clubs = loadClubs()
        self.competitions = loadCompetitions()

    app = Flask(__name__)
    app.secret_key = "something_special"

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/showSummary", methods=["POST"])
    def showSummary(self):
        club = [club for club in self.clubs if club["email"] == request.form["email"]]
        print(club)
        return render_template(
            "welcome.html", club=club, competitions=self.competitions
        )

    @app.route("/book/<competition>/<club>")
    def book(self, competition, club):
        foundClub = [c for c in self.clubs if c["name"] == club][0]
        foundCompetition = [c for c in self.competitions if c["name"] == competition][0]
        if foundClub and foundCompetition:
            return render_template(
                "booking.html", club=foundClub, competition=foundCompetition
            )
        else:
            flash("Something went wrong-please try again")
            return render_template(
                "welcome.html", club=club, competitions=self.competitions
            )

    @app.route("/purchasePlaces", methods=["POST"])
    def purchasePlaces(self):
        competitions = loadCompetitions()
        clubs = loadClubs()
        competition = [
            c for c in competitions if c["name"] == request.form["competition"]
        ][0]
        club = [c for c in clubs if c["name"] == request.form["club"]][0]
        placesRequired = int(request.form["places"])
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )
        flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions)

    # TODO: Add route for points display

    @app.route("/logout")
    def logout():
        return redirect(url_for("index"))
