import csv
import attr
import numpy as np
from collections import defaultdict


class BudgetDepletedError(Exception):
    pass


@attr.s
class Rating:
    """Movie rating."""
    user = attr.ib()
    movie = attr.ib()
    date = attr.ib()
    stars = attr.ib()


class DpQuerySession:
    """
    Respond to database queries with differential privacy.

    Args:
        db (str): Path to the ratings database csv-file.
        privacy_budget (float): Total differential privacy epsilon for the session.
    """

    def __init__(self, db, privacy_budget):
        self.db = db
        self.privacy_budget = privacy_budget
        self._spent_budget = 0
        self._load_db()
        self.SENSITIVITY = 1
        self._cached_responses = {}

    def _load_db(self):
        """Load the rating database from a csv-file."""
        self._entries = []
        with open(self.db) as f:
            reader = csv.reader(f, quotechar='"', delimiter=",")
            for email, movie, date, stars in reader:
                self._entries.append(
                    Rating(user=email, movie=movie, date=date, stars=int(stars))
                )

    @property
    def remaining_budget(self):
        """
        Calculate the remaining privacy budget.

        Returns:
            float: The remaining privacy budget.
        """
        return self.privacy_budget - self._spent_budget

    def get_count(self, movie_name, rating_threshold, epsilon):
        """
        Get the number of ratings where a given movie is rated at least as high as threshold.

        Args:
            movie_name (str): Movie name.
            rating_threshold (int): Rating threshold (number between 1 and 5).
            epsilon (float): Differential privacy epsilon to use for this query.

        Returns:
            float: The count with differentially private noise added.

        Raises:
            BudgetDepletedError: When query would exceed the total privacy budget.
        """
        if epsilon <= 0:
            raise ValueError("epsilon should be > 0")

        if (movie_name, rating_threshold) in self._cached_responses:
            return self._cached_responses[(movie_name, rating_threshold)]

        #Check to make sure that epsilon is not greater than the remaining privacy budget. " \
        #If epsilon is greater than the remaining privacy budget, the function raises a BudgetDepletedError."
        if epsilon > self.remaining_budget:
            raise BudgetDepletedError(f"Privacy budget exceeded: remaining budget is {self.remaining_budget}")

        # count represents the number of ratings for a particular movie
        # that meet or exceed the specified threshold
        count = len([rating for rating in self._entries if rating.movie == movie_name and rating.stars >= rating_threshold])

        noisy_count = count + np.random.laplace(loc=0, scale=self.SENSITIVITY/epsilon)
        self._cached_responses[(movie_name, rating_threshold)] = noisy_count
        self._spent_budget += epsilon

        return noisy_count
