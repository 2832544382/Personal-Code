from typing import List

import numpy as np

N_DIMENSIONS = 10


def classify(train: np.ndarray, train_labels: np.ndarray, test: np.ndarray) -> List[str]:
    """Classify a set of feature vectors using a training set.

    This dummy implementation simply returns the empty square label ('.')
    for every input feature vector in the test data.

    Note, this produces a surprisingly high score because most squares are empty.

    Args:
        train (np.ndarray): 2-D array storing the training feature vectors.
        train_labels (np.ndarray): 1-D array storing the training labels.
        test (np.ndarray): 2-D array storing the test feature vectors.

    Returns:
        list[str]: A list of one-character strings representing the labels for each square.
    """

    """
    # try multi
    count1 = 0
    length1 = len(train_labels)

    dot = []
    wk = []
    wq = []
    wr = []
    wn = []
    wb = []
    wp = []
    bk = []
    bq = []
    br = []
    bn = []
    bb = []
    bp = []

    # get positions of each character
    while count1 != length1:
        if train_labels[count1] == 'K':
            wk.append(count1)
            count1 += 1
        elif train_labels[count1] == 'Q':
            wq.append(count1)
            count1 += 1
        elif train_labels[count1] == 'R':
            wr.append(count1)
            count1 += 1
        elif train_labels[count1] == 'N':
            wn.append(count1)
            count1 += 1
        elif train_labels[count1] == 'B':
            wb.append(count1)
            count1 += 1
        elif train_labels[count1] == 'P':
            wp.append(count1)
            count1 += 1
        elif train_labels[count1] == 'k':
            bk.append(count1)
            count1 += 1
        elif train_labels[count1] == 'q':
            bq.append(count1)
            count1 += 1
        elif train_labels[count1] == 'r':
            br.append(count1)
            count1 += 1
        elif train_labels[count1] == 'n':
            bn.append(count1)
            count1 += 1
        elif train_labels[count1] == 'b':
            bb.append(count1)
            count1 += 1
        elif train_labels[count1] == 'p':
            bp.append(count1)
            count1 += 1
        else:
            dot.append(count1)
            count1 += 1

    dot_array = np.array(dot)
    wk_array = np.array(wk)
    wq_array = np.array(wq)
    wr_array = np.array(wr)
    wn_array = np.array(wn)
    wb_array = np.array(wb)
    wp_array = np.array(wp)
    bk_array = np.array(bk)
    bq_array = np.array(bq)
    br_array = np.array(br)
    bn_array = np.array(bn)
    bb_array = np.array(bb)
    bp_array = np.array(bp)

    dot_n = np.array([])
    wk_n = np.array([])
    wq_n = np.array([])
    wr_n = np.array([])
    wn_n = np.array([])
    wb_n = np.array([])
    wp_n = np.array([])
    bk_n = np.array([])
    bq_n = np.array([])
    br_n = np.array([])
    bn_n = np.array([])
    bb_n = np.array([])
    bp_n = np.array([])

    # get correspond values
    for i in dot_array:
        dot_n = np.append(dot_n, train[i, :])
    for i in wk_array:
        wk_n = np.append(wk_n, train[i, :])
    for i in wq_array:
        wq_n = np.append(wq_n, train[i, :])
    for i in wr_array:
        wr_n = np.append(wr_n, train[i, :])
    for i in wn_array:
        wn_n = np.append(wn_n, train[i, :])
    for i in wb_array:
        wb_n = np.append(wb_n, train[i, :])
    for i in wp_array:
        wp_n = np.append(wp_n, train[i, :])
    for i in bk_array:
        bk_n = np.append(bk_n, train[i, :])
    for i in bq_array:
        bq_n = np.append(bq_n, train[i, :])
    for i in br_array:
        br_n = np.append(br_n, train[i, :])
    for i in bn_array:
        bn_n = np.append(bn_n, train[i, :])
    for i in bb_array:
        bb_n = np.append(bb_n, train[i, :])
    for i in bp_array:
        bp_n = np.append(bp_n, train[i, :])

    # reshape array to matrices
    dot_m = len(dot_n) // 10
    wk_m = len(wk_n) // 10
    wq_m = len(wq_n) // 10
    wr_m = len(wr_n) // 10
    wn_m = len(wn_n) // 10
    wb_m = len(wb_n) // 10
    wp_m = len(wp_n) // 10
    bk_m = len(bk_n) // 10
    bq_m = len(bq_n) // 10
    br_m = len(br_n) // 10
    bn_m = len(bn_n) // 10
    bb_m = len(bb_n) // 10
    bp_m = len(bp_n) // 10

    dot_n = np.reshape(dot_n, (dot_m, 10))
    wk_n = np.reshape(wk_n, (wk_m, 10))
    wq_n = np.reshape(wq_n, (wq_m, 10))
    wr_n = np.reshape(wr_n, (wr_m, 10))
    wn_n = np.reshape(wn_n, (wn_m, 10))
    wb_n = np.reshape(wb_n, (wb_m, 10))
    wp_n = np.reshape(wp_n, (wp_m, 10))
    bk_n = np.reshape(bk_n, (bk_m, 10))
    bq_n = np.reshape(bq_n, (bq_m, 10))
    br_n = np.reshape(br_n, (br_m, 10))
    bn_n = np.reshape(bn_n, (bn_m, 10))
    bb_n = np.reshape(bb_n, (bb_m, 10))
    bp_n = np.reshape(bp_n, (bp_m, 10))

    # combine all
    combine = [dot_n, wk_n, wq_n, wr_n, wn_n, wb_n, wp_n, bk_n, bq_n, br_n, bn_n, bb_n, bp_n]

    # all sorted divergence
    all_sorted = np.array([])
    all_sorted_num = np.array([])

    # compute all pairs
    for i in combine:
        for j in combine:
            mean_x1 = np.mean(i, axis=0)
            mean_x2 = np.mean(j, axis=0)
            var_x1 = np.var(i, axis=0)
            var_x2 = np.var(j, axis=0)
            d12 = 0.5 * (var_x1 / var_x2 + var_x2 / var_x1 - 2) + 0.5 * (mean_x1 - mean_x2) * (mean_x1 - mean_x2) * (
                    1.0 / var_x1 + 1.0 / var_x2)
            sorted_divergence = np.argsort(-d12)
            d12 = d12[sorted_divergence]
            all_sorted = np.append(all_sorted, sorted_divergence[0:3])
            all_sorted_num = np.append(all_sorted_num, d12[0:3])

    all_sorted = np.reshape(all_sorted, (len(all_sorted) // 3, 3))
    all_sorted_num = np.reshape(all_sorted_num, (len(all_sorted_num) // 3, 3))

    # remove duplicates
    duplicate_count = 0
    while duplicate_count <= all_sorted.shape[0]:
        all_sorted = np.delete(all_sorted, duplicate_count, 0)
        all_sorted_num = np.delete(all_sorted_num, duplicate_count, 0)
        duplicate_count += 13

    all_sorted = np.delete(all_sorted, all_sorted.shape[0] - 1, 0)
    all_sorted_num = np.delete(all_sorted_num, all_sorted_num.shape[0] - 1, 0)

    addition = np.array([])
    for i in range(all_sorted_num.shape[0]):
        addition = np.append(addition, np.sum(all_sorted_num[i, :]))

    greatest = np.argsort(-addition)
    addition = addition[greatest]

    k_select = all_sorted[greatest[0]]

    # k-features
    k_features = k_select.astype(int)

    # knn
    # choose k-features of train and test
    all_score = np.array([])
    all_labels = np.array([])
    label = np.array([])

    for i in range(greatest.shape[0]):
        k_select = all_sorted[greatest[i]]
        k_features = k_select.astype(int)

        train_k = train[:, k_features]
        test_k = test[:, k_features]

        x = np.dot(test_k, train_k.T)
        modtest = np.sqrt(np.sum(test_k * test_k, axis=1))
        modtrain = np.sqrt(np.sum(train_k * train_k, axis=1))
        dist = x / np.outer(modtest, modtrain.T)
        nearest = np.argmax(dist, axis=1)
        label = train_labels[nearest]
        count_score = 0

        for q in range(label.shape[0]):
            if train_labels[q] == label[q]:
                count_score += 1

        score = (100.0 * count_score / label.shape[0])

        all_score = np.append(all_score, score)
        all_score = np.argsort(-all_score)

        all_labels = np.append(all_labels, label)

    # calculation
    all_labels = np.reshape(all_labels, (1600, 155))
    label = all_labels[all_score[0]]
    """

    """
    # feature selection
    # count for location of data
    count = 0

    # get position of dot and letter in train_labels
    get_dot = []
    get_letter = []

    # length of train_labels
    length2 = len(train_labels)

    # separate '.' and letters to 2 arrays
    while count != length2:
        if train_labels[count] == '.':
            get_dot.append(count)
            count += 1
        else:
            get_letter.append(count)
            count += 1

    # transform get_dot and get letter to numpy array
    get_dot_array = np.array(get_dot)
    get_letter_array = np.array(get_letter)

    # use to store values in train
    num_dot = np.array([])
    num_letter = np.array([])

    # get correspond value from train
    for i in get_dot_array:
        num_dot = np.append(num_dot, train[i, :])

    for i in get_letter_array:
        num_letter = np.append(num_letter, train[i, :])

    # get length of rows of 2 matrices
    dot_length = len(num_dot) // 10
    letter_length = len(num_letter) // 10

    num_dot = np.reshape(num_dot, (dot_length, 10))
    num_letter = np.reshape(num_letter, (letter_length, 10))

    # choose k-features

    # mean values
    mean_dot = np.mean(num_dot, axis=0)
    mean_letter = np.mean(num_letter, axis=0)

    # variance values
    var_dot = np.var(num_dot, axis=0)
    var_letter = np.var(num_letter, axis=0)

    # multi-divergence
    d12 = 0.5 * (var_dot / var_letter + var_letter / var_dot - 2) + 0.5 * (mean_dot - mean_letter) * (
                mean_dot - mean_letter) * (1.0 / var_dot + 1.0 / var_letter)

    # sort d12 descend
    sorted_divergence = np.argsort(-d12)

    # k-features
    k_feature = sorted_divergence[0:3]
    train_try = train[:test.shape[0], k_feature]
    train = train[:, k_feature]
    test = test[:, k_feature]"""

    """
    # try euclidian distance
    distance = np.array([])
    for i in range(train_try.shape[0]):
        eu = 0
        for j in range(train_try.shape[1]):
            eu = np.sqrt(np.abs(train_try[i, j] ** 2 - test[i, j] ** 2))
            distance = np.append(distance, eu)

    distance = np.reshape(distance, (distance.shape[0] // 3, 3))
    nearest_dist = np.argmax(distance, axis=1)
    label_try = train_labels[nearest_dist]
    """

    # dist
    # cosine distance
    x = np.dot(test, train.transpose())
    modtest = np.sqrt(np.sum(test * test, axis=1))
    modtrain = np.sqrt(np.sum(train * train, axis=1))
    dist = x / np.outer(modtest, modtrain.transpose())
    print(dist)

    nearest = np.argmax(dist, axis=1)
    print(nearest)
    label = train_labels[nearest]

    return label


# The functions below must all be provided in your solution. Think of them
# as an API that it used by the train.py and evaluate.py programs.
# If you don't provide them, then the train.py and evaluate.py programs will not run.
#
# The contents of these functions are up to you but their signatures (i.e., their names,
# list of parameters and return types) must not be changed. The trivial implementations
# below are provided as examples and will produce a result, but the score will be low.


def reduce_dimensions(data: np.ndarray, model: dict) -> np.ndarray:
    """Reduce the dimensionality of a set of feature vectors down to N_DIMENSIONS.
    """
    # use the calculated eigenvector that stored in model
    data_mean = data - np.mean(data)
    data_std = data_mean / np.std(data_mean)
    ten_eigenvector = np.array(model["ten_eigenvectors"])
    reduced_data = np.dot(data_std, ten_eigenvector)
    return reduced_data


def process_training_data(fvectors_train: np.ndarray, labels_train: np.ndarray) -> dict:
    """Process the labeled training data and return model parameters stored in a dictionary.
    """

    # The design of this is entirely up to you.
    # Note, if you are using an instance based approach, e.g. a nearest neighbour,
    # then the model will need to store the dimensionally-reduced training data and labels.
    model = {}
    model["labels_train"] = labels_train.tolist()

    # pca -> ordered eigenvector
    fvectors_train_mean = fvectors_train - np.mean(fvectors_train, axis=0)
    fvectors_train_std = fvectors_train_mean / np.std(fvectors_train_mean)
    covx = np.cov(fvectors_train_std, rowvar=0)
    eigenvalue, eigenvector = np.linalg.eig(covx)
    ordered = np.argsort(eigenvalue)
    ordered = np.flip(ordered)
    eigenvector_ordered = eigenvector[ordered]
    ten_features = eigenvector_ordered[:, :N_DIMENSIONS]
    model["ten_eigenvectors"] = ten_features.tolist()

    fvectors_train_reduced = reduce_dimensions(fvectors_train, model)
    model["fvectors_train"] = fvectors_train_reduced.tolist()
    return model


def images_to_feature_vectors(images: List[np.ndarray]) -> np.ndarray:
    """Takes a list of images (of squares) and returns a 2-D feature vector array.
    """
    h, w = images[0].shape
    n_features = h * w
    fvectors = np.empty((len(images), n_features))
    for i, image in enumerate(images):
        fvectors[i, :] = image.reshape(1, n_features)

    return fvectors


def classify_squares(fvectors_test: np.ndarray, model: dict) -> List[str]:
    """Run classifier on a array of image feature vectors presented in an arbitrary order.
    """

    # Get some data out of the model. It's up to you what you've stored in here
    fvectors_train = np.array(model["fvectors_train"])
    labels_train = np.array(model["labels_train"])

    # Call the classify function.
    labels = classify(fvectors_train, labels_train, fvectors_test)

    return labels


def classify_boards(fvectors_test: np.ndarray, model: dict) -> List[str]:
    """Run classifier on a array of image feature vectors presented in 'board order'.
    """

    """ten_eigens = np.array(model["ten_eigenvectors"])
    reconstruct = np.dot(fvectors_test, ten_eigens.T)
    reconstruct_to_board = np.reshape(reconstruct, (reconstruct.shape[0]//64, reconstruct.shape[1]*64))
    for i in range(reconstruct_to_board.shape[0]):
        split = np.reshape(reconstruct_to_board[i], (64, 2500))
        split_mean = split - np.mean(split, axis=0)
        split_std = split_mean / np.std(split_mean)
        cov_split = np.cov(split_std, rowvar=0)
        eva, eve = np.linalg.eig(cov_split)
        eva_sort = np.argsort(eva)
        eva_sort = np.flip(eva_sort)
        eve_sorted = eve[eva_sort]
        ten_eve = eve_sorted[:, :N_DIMENSIONS]
        final = np.dot(reconstruct, ten_eve)"""

    return classify_squares(fvectors_test, model)
