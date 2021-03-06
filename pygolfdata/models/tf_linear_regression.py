"""
A collection of function of Linear Regresion utilties using TensorFlow,
including input function, feature column construction, and model training.
"""
import math
from matplotlib import pyplot as plt
import numpy as np
from sklearn import metrics
import tensorflow as tf
from tensorflow.python.data import Dataset

tf.logging.set_verbosity(tf.logging.ERROR)


def construct_cross_feature_columns(df, feature_a, feature_b):
    """
    Construct TensorFlow Feature Columns.

    Args:
        df: pandas DataFrame of features
        feature_a: label of the first feature
        feature_b: label of the second feature
    """
    col_a = tf.feature_column.numeric_column(feature_a)
    col_b = tf.feature_column.numeric_column(feature_b)

    bucketized_a = tf.feature_column.bucketized_column(
        col_a, get_quantile_based_boundaries(df[feature_a], 10))
    bucketized_b = tf.feature_column.bucketized_column(
        col_b, get_quantile_based_boundaries(df[feature_b], 2))

    a_x_b = tf.feature_column.crossed_column(
        set([bucketized_a, bucketized_b]), hash_bucket_size=1000)

    return set([bucketized_a, bucketized_b, a_x_b])


def get_quantile_based_boundaries(feature_values, num_buckets):
    """
    A helper function to get bucket boundaries before it is passed to TensorFlow

    Args:
        feature_values: pandas Series of features to be bucketed
        num_buckets: number of buckets where the features go to
    """
    boundaries = np.arange(1.0, num_buckets) / num_buckets
    quantiles = feature_values.quantile(boundaries)
    return [quantiles[q] for q in quantiles.keys()]


def my_input_fn(
        features,
        targets,
        batch_size=1,
        shuffle=True,
        num_epochs=None):
    """
    Instruct TensorFlow how to preprocess the data,
    including converting the pandas feature into a dict of NumPy,
    then constructing a dataset object from our data
    before breaking it down into batches

    Args:
      features: pandas DataFrame of features
      targets: pandas Series of targets
      batch_size: Size of batches to be passed to the model
      shuffle: True or False. Whether to shuffle the data.
      num_epochs: Number of epochs for which data should be repeated.
                    None = repeat indefinitely
    Returns:
      Tuple of (features, labels) for next data batch
    """

    # Convert pandas data into a dict of np arrays.
    features = {key: np.array(value) for key, value in dict(features).items()}

    # Construct a dataset, and configure batching/repeating.
    ds = Dataset.from_tensor_slices((features, targets))  # warning: 2GB limit
    ds = ds.batch(batch_size).repeat(num_epochs)

    # Shuffle the data, if specified.
    if shuffle:
        ds = ds.shuffle(10000)

    # Return the next batch of data.
    features, labels = ds.make_one_shot_iterator().get_next()
    return features, labels


def construct_feature_columns(input_features):
    """
    Construct the TensorFlow Feature Columns.
    Args:
        input_features: The names of the numerical input features to use.
    Returns:
        A set of feature columns
    """
    return set([tf.feature_column.numeric_column(my_feature)
                for my_feature in input_features])


def train_model(
        learning_rate,
        steps,
        batch_size,
        training_examples,
        training_targets,
        validation_examples,
        validation_targets,
        feature_columns=None,
        use_ftrl=False):
    """
    Trains a linear regression model of multiple features.

    In addition to training, this function also prints training progress,
    as well as a plot of the training and validation loss over time.

    Args:
        learning_rate: A `float`, the learning rate.
        steps: A non-zero `int`, the total number of training steps.
        A training step consists of a forward
        and backward pass using a single batch.
        batch_size: A non-zero `int`, the batch size.
        training_examples: A `DataFrame` containing selected columns from
        `combined_shotlink_weather_data` to use for training.
        training_targets: A `DataFrame` containing exactly one column from
        `combined_shotlink_weather_data` to use as target for training.
        validation_examples: A `DataFrame` containing selected columns from
        `combined_shotlink_weather_data` to use for validation/test.
        validation_targets: A `DataFrame` containing selected columns from
        `combined_shotlink_weather_data` to use for validation/test.
        `feature_columns`: A set of input feature columns
        `use_ftrl`: To use FTRL optimization or the standard Gradient Descent
        optimization

    Returns:
        A `LinearRegressor` object trained on the training data.
    """

    periods = 10
    steps_per_period = steps / periods

    # Create a linear regressor object either using FTRL or Gradient Descent
    if use_ftrl:
        my_optimizer = tf.train.FtrlOptimizer(learning_rate=learning_rate)
    else:
        my_optimizer = tf.train.GradientDescentOptimizer(
            learning_rate=learning_rate)
    my_optimizer = tf.contrib.estimator.clip_gradients_by_norm(
        my_optimizer, 5.0)
    if not feature_columns:
        feature_columns = construct_feature_columns(training_examples)

    linear_regressor = tf.estimator.LinearRegressor(
        feature_columns,
        optimizer=my_optimizer
    )

    # Create input functions.
    training_input_fn = lambda: my_input_fn(
        training_examples,
        training_targets,
        batch_size=batch_size)

    predict_training_input_fn = lambda: my_input_fn(
        training_examples,
        training_targets,
        num_epochs=1,
        shuffle=False)

    predict_validation_input_fn = lambda: my_input_fn(
        validation_examples,
        validation_targets,
        num_epochs=1,
        shuffle=False)

    print("Training model...")
    print("RMSE (on training data):")
    training_rmse_list = []
    validation_rmse_list = []
    for period in range(0, periods):
        # Train the model, starting from the prior state.
        linear_regressor.train(
            input_fn=training_input_fn,
            steps=steps_per_period,
        )

        training_predictions = linear_regressor.predict(
            input_fn=predict_training_input_fn)
        training_predictions = np.array(
            [item['predictions'][0] for item in training_predictions])

        validation_predictions = linear_regressor.predict(
            input_fn=predict_validation_input_fn)
        validation_predictions = np.array(
            [item['predictions'][0] for item in validation_predictions])

        # Compute training and validation loss.
        training_rmse = math.sqrt(
            metrics.mean_squared_error(training_predictions, training_targets))
        validation_rmse = math.sqrt(
            metrics.mean_squared_error(
                validation_predictions,
                validation_targets
                ))
        # Occasionally print the current loss.
        print("{0}: {1:.2f}".format(period, training_rmse))
        # Add the loss metrics from this period to our list.
        training_rmse_list.append(training_rmse)
        validation_rmse_list.append(validation_rmse)
    print("Model training finished.")

    # Output a graph of loss metrics over periods.
    plt.ylabel("RMSE")
    plt.xlabel("Periods")
    plt.title("Root Mean Squared Error vs. Periods")
    plt.tight_layout()
    plt.plot(training_rmse, label="training")
    plt.plot(validation_rmse, label="test")
    plt.legend()

    return linear_regressor
