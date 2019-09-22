import json
import time
import logging
import functools

import pandas as pd
import numpy as np

from sklearn import linear_model
from dataclasses import dataclass
from typing import List, Dict

logger = logging.getLogger(__name__)


def timeit(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            output = func(*args, **kwargs)
            logger.info("Execution time %s" % (time.time() - start))
            return output
        return wrapper
    return decorator


class LinearRegression(object):

    class Methods:
        LINALG = "linalg"
        SKLEARN = "sklearn"
        GRADIENT = "gradient"

    @dataclass(frozen=True)
    class TrainedModel:
        target_column: str
        add_intercept: str
        predictors: List[str]
        weights: List[float]
        training_data: Dict
        sme: float

        @property
        def rsme(self):
            return np.sqrt(self.sme)

        def to_json(self, indent=None):
            return json.dumps(self.__dict__, indent=indent)

        def save(self, path, indent=None):
            with open(path, "w") as file:
                file.write(self.to_json(indent=indent))

        @staticmethod
        def from_json(path):
            with open(path, "r") as file:
                return LinearRegression.TrainedModel(**json.loads(file.read()))

    def __init__(self, data, target_column, add_intercept=""):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Argument <data> must be of type DataFrame")
        if target_column not in data.columns:
            raise ValueError("Argument <target_column> should be a col of <data>")
        self.data = data.copy()
        self.target_column = target_column
        self.predictors = [col for col in data.columns if col != target_column]
        self.add_intercept = add_intercept
        self._model = None
        if add_intercept:
            self.predictors.append(add_intercept)
            self.data[add_intercept] = 1

    def set_model(self, model_instance):
        self._model = model_instance
        return self

    def save(self, path):
        if not self._model:
            raise ValueError("Only trained models can be saved.")
        self._model.save(path)

    @staticmethod
    def load(model_path):
        model_instance = LinearRegression.TrainedModel.from_json(path=model_path)
        return LinearRegression(
            data=pd.DataFrame(model_instance.training_data),
            target_column=model_instance.target_column,
            add_intercept=model_instance.add_intercept
        ).set_model(model_instance)

    @staticmethod
    def from_path(data_path, target_column, add_intercept):
        data = pd.read_csv(data_path)
        return LinearRegression(data=data, target_column=target_column, add_intercept=add_intercept)

    @staticmethod
    def squared_mean_error(original, estimate):
        error = original - estimate
        return (error.T * error / len(original)).tolist()[0][0]

    def _get_training_variables(self):
        x = np.asmatrix(self.data[self.predictors].values)
        y = np.asmatrix(self.data[self.target_column].values).T
        return x, y

    def _get_data_without_interception(self):
        return self.data[[col for col in self.data.columns if col != self.add_intercept]]

    def _update_model(self, weights, sme):
        self._model = LinearRegression.TrainedModel(
            target_column=self.target_column,
            add_intercept=self.add_intercept,
            predictors=self.predictors,
            training_data=self._get_data_without_interception().to_dict(),
            weights=weights.tolist(),
            sme=sme
        )

    def train_linalg(self):
        x, y = self._get_training_variables()
        weights = np.linalg.inv(x.T * x) * x.T * y
        sme = self.squared_mean_error(y, x * weights)
        self._update_model(weights, sme)
        logging.info(f"Successful model training with RSME: {self._model.rsme}")

    def train_sklearn(self):
        x, y = self._get_training_variables()
        n = x.shape[-1]
        regression = linear_model.LinearRegression().fit(x, y)
        # Note: we need to replicate the coefficient vector.
        weights = np.asmatrix(regression.coef_.T) + \
                  np.asmatrix([0 if i != n - 1 else regression.intercept_[0] for i in range(n)]).T
        sme = self.squared_mean_error(y, x * weights)
        self._update_model(weights, sme)
        logging.info(f"Successful model training with RSME: {self._model.rsme}")

    def train_gradient_descent(self):
        # TODO: Provide a gradient descent implementation!
        pass

    def train(self, method=Methods.LINALG):
        if method == LinearRegression.Methods.LINALG:
            self.train_linalg()
        elif method == LinearRegression.Methods.SKLEARN:
            self.train_sklearn()
        elif method == LinearRegression.Methods.GRADIENT:
            self.train_gradient_descent()

    def predict(self, data=None, prediction="estimation"):
        data = data if data else self.data.copy()
        if not self._model:
            raise ValueError("Must train the model before prediction.")
        if self.add_intercept:
            data[self.add_intercept] = 1
        input_df = data[self.predictors]
        x = np.asmatrix(input_df.values)
        y_estimate = x * np.asmatrix(self._model.weights)
        data[prediction] = np.matrix.flatten(y_estimate).tolist()[0]
        return data[[col for col in data.columns if col != self.add_intercept]]
