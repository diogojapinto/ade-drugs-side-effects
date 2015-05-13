import adrecs_interface as ai
import pandas as pd
import numpy as np
import scipy as sp
import pickle as pk
import rbm
import datetime
import time
from utils import get_training_and_test_sets
from sklearn.metrics import roc_curve, auc, precision_recall_fscore_support
from constants import MAX_TO_KEEP

def drug_adr_matrix():
    try:
        matrix_df = pd.read_pickle('data/bipartite_df.p')
    except FileNotFoundError:
        log('Fetching drug adr matrix')
        matrix_df = ai.get_drug_adr_matrix()

    return matrix_df

def train_and_test_set(matrix_df):
    try:
        train_set = pd.read_pickle('data/training_set.p')
        test_set = pd.read_pickle('data/test_set.p')
    except FileNotFoundError:
        log('Dividing matrix in test and training sets')
        train_set, test_set = get_training_and_test_sets(matrix_df)
        # Save test_set so it won't compromise future tests while using RMF
        pk.dump(test_set, open('data/test_set.p', 'wb'))

    return train_set, test_set

def predict(model, drug):
	latent_factors, latent_probs = model.run_visible(drug)
	pred_drug, pred_prob = model.run_hidden(latent_probs)

	return pred_drug, pred_prob

def RMSE(pred, ground_truth):

	rmse = 0
	for p, g in zip(pred, ground_truth):
		rmse = rmse + (p-g)*(p-g)

	rmse = rmse / len(pred)
	return np.sqrt(rmse)

def print_stats(stats, stat_name):
    print("\nMean " + stat_name + "= %f" % sp.mean(stats))
    print("Min " + stat_name + "= %f" % min(stats))
    print("Max " + stat_name + "= %f" % max(stats))
    print("Variance= %f" % sp.var(stats))
    print("Standard Deviation= %f" % sp.std(stats))

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

def create_model(matrix, hidden=3000, epochs=300):

	model = rbm.RBM(num_visible=matrix.shape[1], num_hidden=hidden)
	model.train(matrix, max_epochs=epochs)

	return model

def test():
	matrix_df = drug_adr_matrix()

	matrix_df, test_set = train_and_test_set(matrix_df)
	test_set_mat = test_set.as_matrix() / 5

	# retrieve the numpy matrix, drugs names and adrs names
	matrix = matrix_df.as_matrix()
	matrix = matrix / 5

	# train model
	model = create_model(matrix, hidden=2000, epochs=300)

	rmse = 0
	roc_areas = []
	threshs = []
	predictions = []
	for drug in test_set_mat:
		obj = drug.copy()

        # Put some of them in 0
		obj = random_delete_adrs(obj)

		d, p = predict(model, np.array([obj]))
		predictions.append(p[0])
		rmse = rmse + RMSE(p[0], drug)

		fpr, tpr, threshold = roc_curve(drug, p[0], pos_label=1)

		roc_auc = auc(fpr,tpr)
		roc_areas.append(roc_auc)
		
		youden = tpr + (1-fpr)
		maxIndex = np.where(youden == max(youden))
		threshs.append(threshold[maxIndex[0][0]])

	print(rmse / test_set_mat.shape[0])
	print_stats(roc_areas,'roc_area')

	precision_recall(predictions,sp.mean(threshs),test_set)

def log(message):
    """ logs a given message, binding a timestamp """
    timestamp = time.time()
    time_string = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    print('[' + time_string + ']', message)
	
if __name__ == "__main__":
    test()