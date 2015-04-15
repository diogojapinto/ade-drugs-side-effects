import pandas as pd
import numpy as np
import scipy as sp
import pylab as pl
from constants import MAX_TO_KEEP, MIN_TO_KEEP, NR_ITERATIONS
from sklearn.metrics import roc_curve, auc, precision_recall_fscore_support

def test_latent_factors(q_mat, test_set):
    """ Computes the average error of the obtained latent factors model
        based on the average root_mean_square error of the test_set """
    errors = []
    nr_elems_retracted = []
    test_set = test_set.as_matrix()

    for _ in range(NR_ITERATIONS):
        nr_elems_retracted.append(0)
        line_i = np.random.randint(0, len(test_set))
        original_obj = test_set[line_i]
        obj = original_obj.copy()


        # put some of them in 0
        zeroed_elems_ratio = (MAX_TO_KEEP - MIN_TO_KEEP) * np.random.random_sample() + MIN_TO_KEEP
        candidates = obj > 0

        for index, elem in enumerate(candidates):
            if elem == False:
                continue
            prob = np.random.random_sample()
            if prob <= zeroed_elems_ratio:
                obj[index] = 0
                nr_elems_retracted[len(nr_elems_retracted) - 1] += 1

        obj_factors = obj.dot(q_mat.transpose())
        new_obj = obj_factors.dot(q_mat)

        errors.append(lf.compute_rmse(original_obj, new_obj))

    print("REMOVED OBJECTS COUNT")
    print("Mean : {0:8.6f}".format(sp.mean(nr_elems_retracted)))
    print("Minimum : {0:8.6f}".format(min(nr_elems_retracted)))
    print("Maximum : {0:8.6f}".format(max(nr_elems_retracted)))
    print("Variance : {0:8.6f}".format(sp.var(nr_elems_retracted)))
    print("Std. deviation : {0:8.6f}".format(sp.std(nr_elems_retracted)))

    print("ERRORS")
    print("Mean : {0:8.6f}".format(sp.mean(errors)))
    print("Minimum : {0:8.6f}".format(min(errors)))
    print("Maximum : {0:8.6f}".format(max(errors)))
    print("Variance : {0:8.6f}".format(sp.var(errors)))
    print("Std. deviation : {0:8.6f}".format(sp.std(errors)))

def test_single():
    """ Tests a single random drug, printing the dataframe """
    matrix_df = pd.read_pickle('data/test_set.p')
    _, q_mat, _ = pd.read_pickle('data/final_product.p')

    original_drug = matrix_df.ix[random.sample(matrix_df.index.tolist(), 1)]

    drug_name = original_drug.index.tolist()[0]

    print("Selected %s" % drug_name)

    original_drug = original_drug.as_matrix()[0]
    edited_drug = original_drug.copy()

    zeroed_elems_ratio = (MAX_TO_KEEP - MIN_TO_KEEP) * np.random.random_sample() + MIN_TO_KEEP
    candidates = edited_drug > 0

    for index, elem in enumerate(candidates):
        if elem == False:
            continue
        prob = np.random.random_sample()
        if prob <= zeroed_elems_ratio:
            edited_drug[index] = 0

    drug_factors = edited_drug.dot(q_mat)
    drug_prediction = drug_factors.dot(q_mat.transpose())

    print("Error: %f" % lf.compute_rmse(original_drug, drug_prediction))

    results_df = pd.DataFrame([original_drug, edited_drug, drug_prediction], 
                                  index=['original', 'test', 'prediction'])
    print(results_df)
    print(results_df.iloc[:, candidates])

    fpr, tpr, thresholds = roc_curve(original_drug, drug_prediction, pos_label = 5)
    roc_auc = auc(fpr,tpr)
    print("Area under the curve: %f" % roc_auc )

    # Plot ROC curve
    pl.clf()
    pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    pl.plot([0, 1], [0, 1], 'k--')
    pl.xlim([0.0, 1.0])
    pl.ylim([0.0, 1.0])
    pl.xlabel('False Positive Rate')
    pl.ylabel('True Positive Rate')
    pl.title('Receiver operating characteristic example')
    pl.legend(loc="lower right")
    pl.savefig('data/roc/' + drug_name)
    pl.show()

def test_roc(q_mat, test_set, plot=False):
    errors = []
    nr_elems_retracted = []

    drug_names = test_set.index.tolist()
    test_set = test_set.as_matrix()

    rows, cols = test_set.shape
    roc_areas = []

    print(q_mat.shape)
    threshs = []
    predictions = []

    for r in range(len(test_set)):

        original_obj = test_set[r]
        obj = original_obj.copy()

        # put some of them in 0
        zeroed_elems_ratio = 1-MAX_TO_KEEP
        candidates = obj > 0

        for index, elem in enumerate(candidates):
            if elem == False:
                continue
            prob = np.random.random_sample()
            if prob <= zeroed_elems_ratio:
                obj[index] = 0

        obj_factors = obj.dot(q_mat.transpose())
        drug_prediction = obj_factors.dot(q_mat)
        predictions.append(drug_prediction)

        fpr, tpr, thresholds = roc_curve(original_obj, drug_prediction, pos_label = 5)
        roc_auc = auc(fpr,tpr)
        roc_areas.append(roc_auc)

        youden = tpr + (1-fpr)
        maxIndex = np.where(youden == max(youden))
        threshs.append(thresholds[maxIndex[0][0]])

        # Plot ROC curve
        if(plot):
            pl.clf()
            pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
            pl.plot([0, 1], [0, 1], 'k--')
            pl.xlim([0.0, 1.0])
            pl.ylim([0.0, 1.0])
            pl.xlabel('False Positive Rate')
            pl.ylabel('True Positive Rate')
            pl.title('Receiver operating characteristic for %s' % drug_names[r])
            pl.legend(loc="lower right")
            pl.savefig('data/roc/' + drug_names[r])

    print("Mean Roc Area= %f" % sp.mean(roc_areas))
    print("Min Roc Area= %f" % min(roc_areas))
    print("Max Roc Area= %f" % max(roc_areas))
    print("Variance= %f" % sp.var(roc_areas))
    print("Standard Deviation= %f" % sp.std(roc_areas))
    print("\nMean thresholds= %f" % sp.mean(threshs))
    print("Min Threshold= %f" % min(threshs))
    print("Max Threshold %f" % max(threshs))
    print("Variance= %f" % sp.var(threshs))
    print("Standard Deviation= %f" % sp.std(threshs))

    return sp.mean(roc_areas), sp.mean(threshs), predictions

def precisionRecall(predictions, threshold, test_set):

    test_set = test_set.as_matrix()

    precisions = []
    recalls = []
    for p in range(len(predictions)):
        original_obj = test_set[p]
        pred = predictions[p].copy()

        idx = pred >= threshold
        pred[idx] = 5
        pred[~idx] = 0

        precision, recall, fbeta_score, support = precision_recall_fscore_support(original_obj,pred, average="macro", pos_label=5)
        precisions.append(precision)
        recalls.append(recall)

    print("\nMean Precision= %f" % sp.mean(precisions))
    print("Min Precision= %f" % min(precisions))
    print("Max Precision= %f" % max(precisions))
    print("Variance= %f" % sp.var(precisions))
    print("Standard Deviation= %f" % sp.std(precisions))
    print("\nMean Recall= %f" % sp.mean(recalls))
    print("Min Recall= %f" % min(recalls))
    print("Max Recall %f" % max(recalls))
    print("Variance= %f" % sp.var(recalls))
    print("Standard Deviation= %f" % sp.std(recalls))
