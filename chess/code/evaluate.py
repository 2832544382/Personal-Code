import json
import os
import sys
from typing import Tuple

import numpy as np

import system
from utils import utils

EXPECTED_DIMENSIONALITY = 10  # Expected feature vector dimensionality
MAX_MODEL_SIZE = 3145728  # Max size of model file in bytes
NUM_TEST_PAGES = 10  # Number of test pages # TODO


def evaluate(image_dir: str, model_data: dict, board_metadata: list) -> Tuple[float, float]:

    images = utils.load_board_images(image_dir, board_metadata)
    true_labels = utils.load_board_labels(board_metadata)

    fvectors = system.images_to_feature_vectors(images)
    fvectors_reduced = system.reduce_dimensions(fvectors, model_data)

    # Check that teh dimensionality of the reduced feature vectors is correct.
    n_dimensions = fvectors_reduced.shape[1]
    if n_dimensions > EXPECTED_DIMENSIONALITY:
        print(
            f"Error: Your dimensionally reduced feature vector has {n_dimensions} dimensions.",
            f"The maximum allowed is {EXPECTED_DIMENSIONALITY}.",
        )
        sys.exit()

    # Classify and evaluate in full board mode. Feature vectors are in board order.
    output_labels_board = system.classify_boards(fvectors_reduced, model_data)
    score_board = 100.0 * np.sum(output_labels_board == np.array(true_labels)) / len(true_labels)

    # Shuffle everything so that board position cannot be inferred from the order
    # Note, feature vectors and labels are shuffled in the same way
    shuffled_indices = np.random.permutation(len(true_labels))
    fvectors_reduced = fvectors_reduced[shuffled_indices]
    true_labels = np.array(true_labels)[shuffled_indices]

    # Classify and evaluate again but now in isolated square mode with shuffled data
    output_labels_squares = system.classify_squares(fvectors_reduced, model_data)
    score_square = 100.0 * np.sum(output_labels_squares == true_labels) / len(true_labels)
    return score_square, score_board


def evaluate_interface(image_dir: str, model_file: str, testdata_file: str):

    # Check that the model file does not violate the maximum size rule.
    statinfo = os.stat(model_file)
    if statinfo.st_size > MAX_MODEL_SIZE:
        print("Error: model file exceeds allowed size limit.")
        sys.exit()

    # Load the results of the training process
    model_data = utils.load_jsongz(model_file)
    with open(testdata_file, "r", encoding="utf-8") as fp:
        board_metadata = json.load(fp)

    score_square, score_board = evaluate(image_dir, model_data, board_metadata)
    print(f"Square mode: score = {score_square:3.1f}% correct")
    print(f"Board mode: score = {score_board:3.1f}% correct")


def main():
    """Run the evaluation"""

    # Select dataset to use for the evaluation.
    testdata_file = "data/boards.dev.json"

    # Run evaluation with clean data and clean model.
    print("Running evaluation with the clean data.")
    image_dir = "data/clean"
    model_file = "data/model.clean.json.gz"
    evaluate_interface(image_dir, model_file, testdata_file)

    # Run evaluation with noisy data and noisy model.
    print("Running evaluation with the noisy data.")
    image_dir = "data/noisy"
    model_file = "data/model.noisy.json.gz"
    evaluate_interface(image_dir, model_file, testdata_file)


if __name__ == "__main__":
    main()
