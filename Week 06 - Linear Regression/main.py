import fire
import logging

from util import LinearRegression, timeit, pd

logger = logging.getLogger(__name__)


class Main(object):

    @property
    def about(self):
        return "This is a simple implementation of linear regression."

    @staticmethod
    @timeit(logger)
    def train_linear_regression(data_path, target_column, method, intercept_colname="intercept", save_path=""):
        lr = LinearRegression.from_path(data_path=data_path, target_column=target_column, add_intercept=intercept_colname)
        lr.train(method=method)
        if save_path:
            lr.save(path=save_path)

    @staticmethod
    @timeit(logger)
    def score_linear_regression(model_path, data_path=None, prediction="estimation", save_output=""):
        data = pd.read_csv(data_path) if data_path else data_path
        lr = LinearRegression.load(model_path)
        output = lr.predict(data=data, prediction=prediction)
        print(output)
        if save_output:
            output.to_csv(save_output)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(Main)
