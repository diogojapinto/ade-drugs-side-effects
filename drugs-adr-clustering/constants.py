"""
    Reference for constants used in the application
"""


ORIGINAL_ID = 'original'    # identifier for the original SVD matrix
REDUCED_ID = 'reduced'      # identifier for the reduced SVD matrix
IMPROVED_ID = 'improved'    # identifier for the impoved SVD matrix (after gradient descent)

ADRS_WEIGHT = 5

NORMAL_TRAINING_SET_SIZE = 0.7
EXTENDED_TRAINING_SET_SIZE = 0.6
EXTENDED_TEST_SET_SIZE = 0.2

ENERGY_TO_RETAIN = 0.9

LEARNING_RATE = 0.3
REGULARIZATION_PARAM = 0.5    # trading of between predicted performance on the model
                                  # (high value), versus the complexity of the model (low value)

## Testing related:
NR_ITERATIONS = 1000
MIN_TO_KEEP = 0.3
MAX_TO_KEEP = 0.7
