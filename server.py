import json
from flask import Flask, render_template, request, redirect, flash, url_for
from dataclasses import dataclass


@dataclass
class Club:
    name: str
    email: str
    points: int


@dataclass
class Competition:
    name: str
    numberOfPlaces: int
    date: str


def load_clubs():
    with open("clubs.json") as clubs_json:
        list_of_clubs = json.load(clubs_json)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as competitions_json:
        list_of_competitions = json.load(competitions_json)["competitions"]
        return list_of_competitions


def list_of_dicts_filter(list_of_dicts, key, value):
    return [element for element in list_of_dicts if element.get(key) == value]


def list_of_dicts_get(list_of_dicts, key, value):
    filtered_list = list_of_dicts_filter(list_of_dicts, key, value)
    len_filtered_list = len(filtered_list)
    if len_filtered_list == 1:
        return filtered_list[0]
    elif len_filtered_list > 1:
        print(f"Error: More than one element found for key : {key} and value : {value}")
    else:
        print(f"Error: No element found for key : {key} and value : {value}")
    return None


class baseRouter:
    """
    This is the main router of the application the goal here is to make an MVC architecture using flask
    """

    app = Flask(__name__)
    app.secret_key = "something_special"

    clubs = load_clubs()
    competitions = load_competitions()

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/show_summary", methods=["POST"])
    def show_summary():
        competitions = load_competitions()
        clubs = load_clubs()
        club = list_of_dicts_get(clubs, "email", request.form["email"])
        error_message = ""
        if club is None:
            print("Club email address not found in show_summary")
            error_message = "Email address not found"
            return render_template("index.html", error_message=error_message)

        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
        )

    @app.route("/book/<competition>/<club>")
    def book(competition, club):
        clubs = load_clubs()
        competitions = load_competitions()
        found_club = list_of_dicts_get(clubs, "name", club)
        found_competition = list_of_dicts_get(competitions, "name", competition)
        if found_club and found_competition:
            return render_template(
                "booking.html", club=found_club, competition=found_competition
            )
        else:
            flash("Something went wrong-please try again")
            return render_template("welcome.html", club=club, competitions=competitions)

    @app.route("/purchase_places", methods=["POST"])
    def purchase_places():
        competitions = load_competitions()
        clubs = load_clubs()
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


app = baseRouter().app
app.run(debug=True)
