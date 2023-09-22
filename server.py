import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs(use_mock_data=False):
    json_file = "clubs.json" if not use_mock_data else "mock_clubs_unique.json"
    with open(json_file) as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions(use_mock_data=False):
    json_file = (
        "competitions.json" if not use_mock_data else "mock_competitions_unique.json"
    )
    with open(json_file) as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        for comp in listOfCompetitions:
            comp["isCurrent"] = (
                datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") >= datetime.now()
            )
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions(use_mock_data=True)
clubs = loadClubs(use_mock_data=True)
page_size = 10


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/clubs_list")
def clubs_list():
    page = request.args.get("page", default=0, type=int)
    if page < 0:
        paginated_clubs = clubs[(page - 1) * page_size : page * page_size]
    else:
        paginated_clubs = clubs[page * page_size : (page + 1) * page_size]
    return render_template("clubs.html", clubs=paginated_clubs, page=page)


@app.route("/showSummary", methods=["POST"])
def showSummary():
    clubs_by_email = [club for club in clubs if club["email"] == request.form["email"]]
    len_clubs_by_email = len(clubs_by_email)
    if len_clubs_by_email == 1:
        loggedInClub = [
            club for club in clubs if club["email"] == request.form["email"]
        ][0]
        return render_template(
            "welcome.html", club=loggedInClub, competitions=competitions, clubs=clubs
        )
    elif len_clubs_by_email == 0:
        msg = "We couldn't find any club with this email"
        return render_template("index.html", club_not_found_error_message=msg)
    else:
        # [TODO] : We should implement this case if it is possible that clubs share an email
        msg = "We found multiple clubs with this email"
        return render_template("index.html", club_not_found_error_message=msg)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClubs = [c for c in clubs if c["name"] == club]

    if len(foundClubs) == 0:
        flash(
            "You tried to manually access a club that does not exist, please use list below"
        )
        return render_template("welcome.html", club=club, competitions=competitions)
    if len(foundClubs) > 1:
        flash("There are multiple clubs with this name, please use list below")
        return render_template("welcome.html", club=club, competitions=competitions)

    foundClub = foundClubs[0]
    foundCompetitions = [c for c in competitions if c["name"] == competition]
    if len(foundCompetitions) == 0:
        flash(
            "You tried to manually access a competition that does not exist, please use list below"
        )
        return render_template("welcome.html", club=club, competitions=competitions)
    if len(foundCompetitions) > 1:
        flash("There are multiple competitions with this name, please use list below")
        return render_template("welcome.html", club=club, competitions=competitions)
    foundCompetition = foundCompetitions[0]
    return render_template("booking.html", club=foundClub, competition=foundCompetition)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form.get("places", 0) or 0)
    availablePlaces = int(competition["numberOfPlaces"])
    clubPoints = int(club["points"])

    if placesRequired <= 0:
        flash("You must purchase at least one place")
        return render_template("booking.html", club=club, competition=competition)

    # We need to store the number of places booked by each club
    placesBookedByClub = competition["places"].get(club["email"], 0)
    if (placesBookedByClub + placesRequired) > 12:
        flash(
            f"You cannot book more than 12 places for a competition, you already have too many places booked for this competition"
        )
        return render_template("booking.html", club=club, competition=competition)

    if placesRequired > clubPoints:
        flash("Sorry, you do not have enough points")
        return render_template("booking.html", club=club, competition=competition)

    if availablePlaces < placesRequired or availablePlaces == 0:
        flash("Sorry, there are not enough places remaining")
        return render_template("booking.html", club=club, competition=competition)

    competition["numberOfPlaces"] = availablePlaces - placesRequired
    club["points"] = clubPoints - placesRequired
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
