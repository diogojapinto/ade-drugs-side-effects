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

        obj = random_delete_adrs(obj)

        obj_factors = obj.dot(q_mat.transpose())
        new_obj = obj_factors.dot(q_mat)

        errors.append(lf.compute_rmse(original_obj, new_obj))

    print("REMOVED OBJECTS COUNT")
    print_stats(nr_elems_retracted, "Removed")
    print("ERRORS")
    print_stats(errors,"Error")

def test_single():
    """ Tests a single random drug, printing the dataframe """
    matrix_df = pd.read_pickle('data/test_set.p')
    _, q_mat, _ = pd.read_pickle('data/final_product.p')

    original_drug = matrix_df.ix[random.sample(matrix_df.index.tolist(), 1)]

    drug_name = original_drug.index.tolist()[0]

    print("Selected %s" % drug_name)

    original_drug = original_drug.as_matrix()[0]
    edited_drug = original_drug.copy()

    edited_drug = random_delete_adrs(edited_drug)

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
    plot_roc(roc_auc,drug_name, fpr, tpr)

def test_roc(q_mat, test_set, plot=False):
    errors = []
    nr_elems_retracted = []
    threshs = []
    predictions = []
    roc_areas = []

    drug_names = test_set.index.tolist()
    test_set = test_set.as_matrix()
    rows, cols = test_set.shape

    for r in range(len(test_set)):

        # Retrieve drug to test
        original_obj = test_set[r]
        obj = original_obj.copy()

        # Put some of them in 0
        obj = random_delete_adrs(obj)

        # Make the prediction
        drug_prediction = predict(obj,q_mat)
        predictions.append(drug_prediction)

        # Create ROC curve
        fpr, tpr, thresholds = roc_curve(original_obj, drug_prediction, pos_label = 5)
        roc_auc = auc(fpr,tpr)
        roc_areas.append(roc_auc)

        # Use youden index to calculate the optimal threshold
        youden = tpr + (1-fpr)
        maxIndex = np.where(youden == max(youden))
        threshs.append(thresholds[maxIndex[0][0]])

        # Plot ROC curve
        if(plot):
            plot_roc(roc_auc, drug_names[r], fpr, tpr)

    print_stats(roc_areas, "Roc Area")
    print_stats(threshs, "Threshold")

    return sp.mean(roc_areas), sp.mean(threshs), predictions

def precision_recall(predictions, threshold, test_set):

    test_set = test_set.as_matrix()

    precisions = []
    recalls = []
    for p in range(len(predictions)):
        original_obj = test_set[p]
        pred = predictions[p].copy()

        # Apply threshold to predictions
        idx = pred >= threshold
        pred[idx] = 5
        pred[~idx] = 0

        # Calculate precision recall
        precision, recall, fbeta_score, support = precision_recall_fscore_support(original_obj,pred, average="macro", pos_label=5)
        precisions.append(precision)
        recalls.append(recall)

    print_stats(precisions,"Precision")
    print_stats(recalls, "Recall")

    return sp.mean(precisions), sp.mean(recalls)

def random_delete_adrs(drug):
    zeroed_elems_ratio = 1-MAX_TO_KEEP
    candidates = drug > 0

    for index, elem in enumerate(candidates):
        if elem == False:
            continue
        prob = np.random.random_sample()
        if prob <= zeroed_elems_ratio:
            drug[index] = 0

    return drug
    
def print_stats(stats, stat_name):
    print("\nMean " + stat_name + "= %f" % sp.mean(stats))
    print("Min " + stat_name + "= %f" % min(stats))
    print("Max " + stat_name + "= %f" % max(stats))
    print("Variance= %f" % sp.var(stats))
    print("Standard Deviation= %f" % sp.std(stats))

def plot_roc(area, name, fpr, tpr):
    pl.clf()
    pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % area)
    pl.plot([0, 1], [0, 1], 'k--')
    pl.xlim([0.0, 1.0])
    pl.ylim([0.0, 1.0])
    pl.xlabel('False Positive Rate')
    pl.ylabel('True Positive Rate')
    pl.title('Receiver operating characteristic for %s' % name)
    pl.legend(loc="lower right")
    pl.savefig('data/roc/' + name)    

def predict(obj, q_mat):
    obj_factors = obj.dot(q_mat.transpose())
    drug_prediction = obj_factors.dot(q_mat)

    return drug_prediction
