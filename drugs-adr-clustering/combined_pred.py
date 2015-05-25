import prediction_main as pm
import rbm_prediction as rpred
import numpy as np
import scipy as sp
import pandas as pd
import test
from sklearn import svm, cross_validation
from sklearn.metrics import roc_curve, auc, precision_recall_fscore_support
from descriptors_cleaner import append_descriptors

def main():
    matrix_df = pm.get_drug_adr_matrix()
    drugs = matrix_df.index.values.tolist()
    adrs = matrix_df.columns.values.tolist()

    # append descriptors
    matrix_df = append_descriptors(matrix_df)

    # retrieve the numpy matrix, drugs names and adrs names
    matrix = matrix_df.as_matrix() / 5

    # Divide into train, validation and test set
    matrix, test_set = cross_validation.train_test_split(matrix, test_size=0.3)
    matrix, validation_set = cross_validation.train_test_split(matrix, test_size=0.01)

    # Train SVD model with training set, having the positive value as 5
    best_q_mat, best_threshold = pm.train_model(pd.DataFrame(matrix)*5, True, len(adrs))
    rbm = rpred.create_model(matrix, hidden=2000, epochs=300)

    # Points to combine the two methods
    X = []
    # Labels
    y = []

    for drug in validation_set:
        # Retrieve drug to test
        obj = drug.copy()

        # Put some of them in 0
        obj = test.random_delete_adrs(obj, len(adrs))

        # Make RBM prediction
        _, rbm_pred = rpred.predict(rbm, np.array([obj]))

        # Make SVD prediction
        svd_pred = test.predict(obj, best_q_mat) / 5

        for e1,e2,label in zip((rbm_pred[0])[0:len(adrs)], svd_pred[0:len(adrs)], drug[0:len(adrs)]):
            X.append([e1,e2])
            y.append(label)


    print("Training SVM with",len(y), "examples.")
    svm_threshold = svm.SVC()
    svm_threshold.fit(X,y)
    print("SVM Trained")

    print("Training SVR with",len(y), "examples.")
    regression_threshold = svm.SVR()
    regression_threshold.fit(X,y)
    print("SVR Trained")

    threshs = []

    print("Computing optimal threshold")
    for drug in validation_set:

        # Retrieve drug to test
        obj = drug.copy()

        # Put some of them in 0
        obj = test.random_delete_adrs(obj,len(adrs))

        # Make RBM prediction
        _, rbm_pred = rpred.predict(rbm, np.array([obj]))

        # Make SVD prediction
        svd_pred = test.predict(obj, best_q_mat) / 5

        prob_prediction = []

        for e1,e2 in zip((rbm_pred[0])[0:len(adrs)],svd_pred[0:len(adrs)]):
            prob_prediction.append(regression_threshold.predict([[e1,e2]])[0])

        # Create ROC curve
        fpr, tpr, thresholds = roc_curve(drug[0:len(adrs)], prob_prediction, pos_label = 1)

        youden = tpr + (1-fpr)
        maxIndex = np.where(youden == max(youden))
        threshs.append(thresholds[maxIndex[0][0]])

    rmse_svd = 0
    rmse_rbm = 0
    rmse = 0
    precisions = []
    recalls = []
    reg_precisions = []
    reg_recalls = []
    roc_areas = []
    thresh = sp.mean(threshs)
    iteration = 0

    for drug in test_set:
        #print("iteration", iteration, "(", (iteration / test_set.shape[0])*100, "%)")
        # Retrieve drug to test
        obj = drug.copy()

        # Put some of them in 0
        obj = test.random_delete_adrs(obj,len(adrs))

        # Make RBM prediction
        _, rbm_pred = rpred.predict(rbm, np.array([obj]))

        # Make SVD prediction
        svd_pred = test.predict(obj, best_q_mat) / 5

        combined_prediction = []
        prob_prediction = []

        for e1,e2 in zip((rbm_pred[0])[0:len(adrs)],svd_pred[0:len(adrs)]):
            combined_prediction.append(svm_threshold.predict([[e1,e2]])[0])
            prob_prediction.append(regression_threshold.predict([[e1,e2]])[0])

        combined_prediction = np.array(combined_prediction)
        prob_prediction = np.array(prob_prediction)

        # Compute RMSE for each prediction
        rmse_svd = rmse_svd + rpred.RMSE(svd_pred[0:len(adrs)], drug[0:len(adrs)])
        rmse_rbm = rmse_rbm + rpred.RMSE((rbm_pred[0])[0:len(adrs)], drug[0:len(adrs)])
        rmse = rmse + rpred.RMSE(combined_prediction, drug[0:len(adrs)])

        # Create ROC curve
        fpr, tpr, _ = roc_curve(drug[0:len(adrs)], prob_prediction, pos_label = 1)
        roc_auc = auc(fpr,tpr)
        roc_areas.append(roc_auc)

        # Calculate precision recall
        precision, recall, _, _ = precision_recall_fscore_support(drug[0:len(adrs)],combined_prediction, average="macro", pos_label=1)
        precisions.append(precision)
        recalls.append(recall)

        # Apply threshold to predictions
        idx = prob_prediction >= thresh
        prob_prediction[idx] = 1
        prob_prediction[~idx] = 0

        # Calculate precision recall
        precision, recall, _, _ = precision_recall_fscore_support(drug[0:len(adrs)],prob_prediction, average="macro", pos_label=1)
        reg_precisions.append(precision)
        reg_recalls.append(recall)

        iteration = iteration+1

    rmse_svd = rmse_svd / test_set.shape[0]
    rmse_rbm = rmse_rbm / test_set.shape[0]
    rmse = rmse / test_set.shape[0]

    print(rmse_svd)
    print(rmse_rbm)
    print(rmse)

    test.print_stats(roc_areas, "Roc Area")
    test.print_stats(precisions,"Precision")
    test.print_stats(recalls, "Recall")

    test.print_stats(reg_precisions,"Reg Precision")
    test.print_stats(reg_recalls, "Reg Recall")

if __name__ == "__main__":
    main()