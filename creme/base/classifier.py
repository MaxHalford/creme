import abc
import typing

import pandas as pd

from creme import base

from .predictor import Predictor


class Classifier(Predictor):
    """A classifier."""

    @abc.abstractmethod
    def fit_one(self, x: dict, y: base.typing.ClfTarget) -> 'Classifier':
        """Update the model with a set of features `x` and a label `y`.

        Parameters:
            x: A dictionary of features.
            y: A label.

        Returns:
            self

        """

    def predict_proba_one(self, x: dict) -> typing.Dict[base.typing.ClfTarget, float]:
        """Predict the probability of each label for a dictionary of features `x`.

        Parameters:
            x: A dictionary of features.

        Returns:
            A dictionary which associates a probability which each label.

        """

        # Some classifiers don't have the ability to output probabilities, and instead only
        # predict labels directly. Therefore, we cannot impose predict_proba_one as an abstract
        # method that each classifier has to implement. Instead, we raise an exception to indicate
        # that a classifier does not support predict_proba_one.
        raise NotImplementedError

    def predict_one(self, x: dict) -> base.typing.ClfTarget:
        """Predict the label of a set of features `x`.

        Parameters:
            x: A dictionary of features.

        Returns:
            The predicted label.

        """

        # The following code acts as a default for each classifier, and may be overriden on an
        # individual basis.
        y_pred = self.predict_proba_one(x)
        if y_pred:
            return max(y_pred, key=y_pred.get)
        return None

    @property
    def _multiclass(self):
        return False


class MiniBatchClassifier:
    """Used for classifiers which can operate on mini-batches.

    """

    @abc.abstractmethod
    def fit_many(self, X: pd.DataFrame, y: pd.Series) -> 'MiniBatchClassifier':
        """Update the model with a mini-batch of features `X` and boolean targets `y`.

        Parameters:
            X: A dataframe of features.
            y: A series of boolean target values.

        Returns:
            self

        """

    def predict_proba_many(self, X: pd.DataFrame) -> pd.DataFrame:
        """Predict the outcome probabilities for a mini-batch of features.

        Parameters:
            X: A dataframe of features.

        Returns:
            A dataframe with probabilities of `True` and `False` for each sample.

        """

        # Some classifiers don't have the ability to output probabilities, and instead only
        # predict labels directly. Therefore, we cannot impose predict_proba_many as an abstract
        # method that each classifier has to implement. Instead, we raise an exception to indicate
        # that a classifier does not support predict_proba_many.
        raise NotImplementedError

    def predict_many(self, X: pd.DataFrame) -> pd.Series:
        """Predict the outcome of a set of features `x`.

        Parameters:
            X: A dataframe of features.

        Returns:
            The predicted outcome.

        """

        # The following code acts as a default for each classifier, and may be overriden on an
        # individual basis.
        return self.predict_proba_many(X).idxmax(axis='columns')
