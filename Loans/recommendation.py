import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold
from .models import Loan
from django.shortcuts import get_object_or_404
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse






def recemmend_for_fsp(user, loan_id):
    train = pd.read_csv('Dataset/train.csv')
    train.head()

    test = pd.read_csv('Dataset/test.csv')
    test.head()

    train['Loan_Status'].value_counts(normalize=True) 



    test_original=test.copy()

    train=train.drop(['Income_bin', 'Coapplicant_Income_bin', 'LoanAmount_bin', 'Total_Income_bin', 'Total_Income'], axis=1)
    train['Dependents'].replace('3+', 3,inplace=True)
    test['Dependents'].replace('3+', 3,inplace=True)
    train['Loan_Status'].replace('N', 0,inplace=True)
    train['Loan_Status'].replace('Y', 1,inplace=True)
    matrix = train.corr()
    train['Gender'].fillna(train['Gender'].mode()[0], inplace=True)
    train['Married'].fillna(train['Married'].mode()[0], inplace=True)
    train['Dependents'].fillna(train['Dependents'].mode()[0], inplace=True)
    train['Self_Employed'].fillna(train['Self_Employed'].mode()[0], inplace=True)
    train['Credit_History'].fillna(train['Credit_History'].mode()[0], inplace=True)
    train['Loan_Amount_Term'].fillna(train['Loan_Amount_Term'].mode()[0], inplace=True)
    train['LoanAmount'].fillna(train['LoanAmount'].median(), inplace=True)

    test['Gender'].fillna(train['Gender'].mode()[0], inplace=True)
    test['Married'].fillna(train['Married'].mode()[0], inplace=True)
    test['Dependents'].fillna(train['Dependents'].mode()[0], inplace=True)
    test['Self_Employed'].fillna(train['Self_Employed'].mode()[0], inplace=True)
    test['Credit_History'].fillna(train['Credit_History'].mode()[0], inplace=True)
    test['Loan_Amount_Term'].fillna(train['Loan_Amount_Term'].mode()[0], inplace=True)
    test['LoanAmount'].fillna(train['LoanAmount'].median(), inplace=True)

    train['LoanAmount_log']=np.log(train['LoanAmount'])
    train['LoanAmount_log'].hist(bins=20)
    test['LoanAmount_log']=np.log(test['LoanAmount'])
    train=train.drop('Loan_ID',axis=1)
    test=test.drop('Loan_ID',axis=1)

    X = train.drop('Loan_Status',1)
    y = train.Loan_Status


    X = pd.get_dummies(X)
    train=pd.get_dummies(train)
    test=pd.get_dummies(test)
    x_train, x_cv, y_train, y_cv = train_test_split(X,y, test_size=0.3)
    model = LogisticRegression()
    model.fit(x_train, y_train)
    LogisticRegression()
    pred_cv = model.predict(x_cv)
    pred_test = model.predict(test)
    submission = get_object_or_404(Loan, id=loan_id).beneficiaries.filter(user=user)
    submission['Loan_Status']=pred_test
    submission['Loan_ID']=test_original['Loan_ID']
    submission['Loan_Status'].replace(0, 'N', inplace=True)
    submission['Loan_Status'].replace(1, 'Y', inplace=True)
    pd.DataFrame(submission, columns=['Loan_ID','Loan_Status']).to_csv('Output/logistic.csv')

    i=1
    mean = 0
    kf = StratifiedKFold(n_splits=5,random_state=1)
    for train_index,test_index in kf.split(X,y):
        xtr,xvl = X.loc[train_index],X.loc[test_index]
        ytr,yvl = y[train_index],y[test_index]
        model = LogisticRegression(random_state=1)
        model.fit(xtr,ytr)
        pred_test=model.predict(xvl)
        score=accuracy_score(yvl,pred_test)
        mean += score
        i+=1
        pred_test = model.predict(test)
        pred = model.predict_proba(xvl)[:,1]

        submission['Loan_Status'].replace(0, 'N', inplace=True)

        
    submission['Loan_Status'].replace(1, 'Y', inplace=True)
    submission['Loan_Status']=pred_test
    submission['Loan_ID']=test_original['Loan_ID']
    submission['Loan_Status'].replace(0, 'N', inplace=True)
    submission['Loan_Status'].replace(1, 'Y', inplace=True)
    pd.DataFrame(submission, columns=['Loan_ID','Loan_Status']).to_csv('Output/Log1.csv')



def recommend_loan_for_msme(loan_id, user):
    loans = get_object_or_404(Loan, id=loan_id).beneficiaries.filter(user=user)
    credit_csv_file = open("credit_rating.csv", mode = "w")
    rating_files = ['combined_data_1.txt']
    for file in rating_files:
        with open(file) as f:
            for line in f:
                line = line.strip()
                if line.endswith(":"):
                    loan_id = line.replace(":", "")
                else:
                    row_data = []
                    row_data = [item for item in line.split(",")]
                    row_data.insert(0, loan_id)
                    credit_csv_file.write(",".join(row_data))  
                    credit_csv_file.write('\n')
                    
    credit_csv_file.close()
    df = pd.read_csv('credit_rating.csv', sep=",", names = ["loan_id","customer_id", "rating", "date"])
    return  loans

def get_user_item_sparse_matrix(df):
    sparse_data = sparse.csr_matrix((df.rating, (df.customer_id, df.loan_id)))
    return sparse_data

def compute_user_similarity(sparse_matrix, limit=100):
    train_data = "test2.csv"
    train_sparse_data = get_user_item_sparse_matrix(train_data)
    row_index, col_index = sparse_matrix.nonzero()
    rows = np.unique(row_index)
    similar_arr = np.zeros(61700).reshape(617,100)
    
    for row in rows[:limit]:
        sim = cosine_similarity(sparse_matrix.getrow(row), train_sparse_data).ravel()
        similar_indices = sim.argsort()[-limit:]
        similar = sim[similar_indices]
        similar_arr[row] = similar
    
    similar_arrsimilar_user_matrix = compute_user_similarity(train_sparse_data, 100)
    return similar_arrsimilar_user_matrix

def clean_balance_sheet(sparse_matrix, limit=100):
    loan_rating_df = "credit_rating.csv"
    split_value = int(len(loan_rating_df) * 0.80)
    train_data = loan_rating_df[:split_value]
    train_sparse_data = get_user_item_sparse_matrix(train_data)
    row_index, col_index = sparse_matrix.nonzero()
    rows = np.unique(row_index)
    similar_arr = np.zeros(61700).reshape(617,100)
    
    for row in rows[:limit]:
        sim = cosine_similarity(sparse_matrix.getrow(row), train_sparse_data).ravel()
        similar_indices = sim.argsort()[-limit:]
        similar = sim[similar_indices]
        similar_arr[row] = similar
    
    similar_arrsimilar_user_matrix = compute_user_similarity(train_sparse_data, 100)
    return similar_arrsimilar_user_matrix

sample_sparse_matrix = 0

def get_average_rating(sparse_matrix, is_user):
    ax = 1 if is_user else 0
    sum_of_ratings = sparse_matrix.sum(axis = ax).A1  
    no_of_ratings = (sparse_matrix != 0).sum(axis = ax).A1 
    rows, cols = sparse_matrix.shape
    average_ratings = {i: sum_of_ratings[i]/no_of_ratings[i] for i in range(rows if is_user else cols) if no_of_ratings[i] != 0}
    return average_ratings


def check_financial_statement():
    global_avg_rating = get_average_rating(sample_sparse_matrix, False)
    global_avg_users = get_average_rating(sample_sparse_matrix, True)
    global_avg_credits = get_average_rating(sample_sparse_matrix, False)
    sample_train_users, sample_train_credits, sample_train_ratings = sparse.find(sample_sparse_matrix)
    new_features_csv_file = open("/content/credit_dataset/new_features.csv", mode = "w")
    
    for user, credit, rating in zip(sample_train_users, sample_train_credits, sample_train_ratings):
        similar_arr = list()
        similar_arr.append(user)
        similar_arr.append(credit)
        similar_arr.append(sample_sparse_matrix.sum()/sample_sparse_matrix.count_nonzero())
        
        similar_users = cosine_similarity(sample_sparse_matrix[user], sample_sparse_matrix).ravel()
        indices = np.argsort(-similar_users)[1:]
        ratings = sample_sparse_matrix[indices, credit].toarray().ravel()
        top_similar_user_ratings = list(ratings[ratings != 0][:5])
        top_similar_user_ratings.extend([global_avg_rating[credit]] * (5 - len(ratings)))
        similar_arr.extend(top_similar_user_ratings)
        
        similar_credits = cosine_similarity(sample_sparse_matrix[:,credit].T, sample_sparse_matrix.T).ravel()
        similar_credits_indices = np.argsort(-similar_credits)[1:]
        similar_credits_ratings = sample_sparse_matrix[user, similar_credits_indices].toarray().ravel()
        top_similar_credit_ratings = list(similar_credits_ratings[similar_credits_ratings != 0][:5])
        top_similar_credit_ratings.extend([global_avg_users[user]] * (5-len(top_similar_credit_ratings)))
        similar_arr.extend(top_similar_credit_ratings)
        
        similar_arr.append(global_avg_users[user])
        similar_arr.append(global_avg_credits[credit])
        similar_arr.append(rating)
        
        new_features_csv_file.write(",".join(map(str, similar_arr)))
        new_features_csv_file.write("\n")
        
    new_features_csv_file.close()
    new_features_df = pd.read_csv('/content/credit_dataset/new_features.csv', names = ["user_id", "credit_id", "gloabl_average", "similar_user_rating1", 
                                                               "similar_user_rating2", "similar_user_rating3", 
                                                               "similar_user_rating4", "similar_user_rating5", 
                                                               "similar_credit_rating1", "similar_credit_rating2", 
                                                               "similar_credit_rating3", "similar_credit_rating4", 
                                                               "similar_credit_rating5", "user_average", 
                                                               "credit_average", "rating"])
    return new_features_df