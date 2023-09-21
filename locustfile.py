from locust import HttpUser, task


from locust import HttpUser, task, between


class MyLocustUserPerfectPath(HttpUser):
    wait_time = between(1, 5)  # Add a random wait time between tasks

    @task
    def index_page(self):
        # Define a task to access the homepage
        self.client.get("/")

    @task
    def login_and_book_valid_mail(self):
        response = self.client.post("/showSummary", {"email": "john@simplylift.co"})
        if "Welcome" in response.text:
            competition = "Spring Festival"
            club = "Simply Lift"
            self.client.get(f"/book/{competition}/{club}")

    @task
    def logout(self):
        self.client.get("/logout")


class MyLocustUserWorstPath(HttpUser):
    wait_time = between(1, 5)  # Add a random wait time between tasks

    @task
    def index_page(self):
        self.client.get("/")

    @task
    def login_and_book_invalid_mail(self):
        response = self.client.post("/showSummary", {"email": "definetlynotanemail"})

        if "Welcome" in response.text:
            competition = "Spring Festival"
            club = "Simply Lift"
            self.client.get(f"/book/{competition}/{club}")

    @task
    def logout_with_parameters(self):
        # Define a task to logout with parameters in the URL
        self.client.get(
            "/logout/?=randomkeywords/?=wrongurls/",
        )


class MyLocustLoadHeavyPath(HttpUser):
    # this user will be focused solely on the booking page in order to test db load times
    wait_time = between(0.5, 1)  # Add a random wait time between tasks

    @task
    def index_page(self):
        self.client.get("/")
