import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

from sklearn import model_selection

from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
import sklearn.metrics
import pydotplus
from sklearn.externals.six import StringIO

#
# usage parameters
#

# do we want to scale the data so that all predictors are between 0 and 1
std_center_data = False
minmax_scale_data = True

#
# Data Manipulation
#
pop_struct = pd.read_csv('../data/pop_structure.csv')
datafile = pd.read_csv('../data/all_data.csv')

min_max = MinMaxScaler(feature_range=(0,1))
scale = StandardScaler(copy=True, with_mean=True, with_std=True)
joined = pd.merge(datafile, pop_struct, on='Entry')
joined.dropna(inplace=True)
joined.drop(['Entry','Line','Name'], axis=1, inplace=True)

dummy_locations = pd.get_dummies(joined['Location']).reset_index(drop=True)
dummy_years = pd.get_dummies(joined['Year']).reset_index(drop=True)
pred = joined[['Precipitation','Day Length','Seedwt','Temperate','South Asia','Middle East','Mediterranean']].reset_index(drop=True)

predict = joined['GDD']
pred_cols = pd.concat([pred, dummy_locations, dummy_years], axis=1)
pred_col_names = pred_cols.columns.tolist()

X_tr,  X_te, y_train, y_test = model_selection.train_test_split(pred_cols, predict, test_size=0.30)

if std_center_data == True:
    predictor_cols = pd.DataFrame(scale.fit_transform(pred_cols), columns=pred_col_names)
    X_train = pd.DataFrame(scale.fit_transform(X_tr), columns=pred_col_names)
    X_test = pd.DataFrame(scale.transform(X_te), columns=pred_col_names)
elif minmax_scale_data == True:
    print('true')
    predictor_cols = pd.DataFrame(min_max.fit_transform(pred_cols), columns=pred_col_names)
    X_train = pd.DataFrame(min_max.fit_transform(X_tr), columns=pred_col_names)
    X_test = pd.DataFrame(min_max.transform(X_te), columns=pred_col_names)
else:
    X_train = X_tr
    X_test = X_te
    predictor_cols = pred_cols

#
# plot the distribution of all the input variables
#
plt.rcParams.update({'font.size': 14})
X_train[X_train.dtypes[(X_train.dtypes == "float64") | (X_train.dtypes == "int64")]
    .index.values].hist(figsize=[11, 11])
plt.savefig('feature-dist.png')
#plt.show()
plt.clf()


plt.rcParams.update({'font.size': 18})
y_train.hist()
plt.title('Distribution of GDD (predicted variable) in training set')
plt.xlabel('GDD')
plt.ylabel('Frequency')
plt.savefig('gdd-dist.png')
##plt.show()
plt.clf()

plt.rcParams.update({'font.size': 12})
residual_df = pd.DataFrame()

#
# Ridge and Lasso Regression
#
models = [Ridge(), Lasso()]
model_names = ['Ridge','Lasso']
alphas = 10**np.linspace(10,-2,100)*0.5
results = {}
for index, model in enumerate(models):
    for alph in alphas:
        mod = model.set_params(alpha = alph, max_iter=100000)
        scores = model_selection.cross_val_score(mod, predictor_cols, predict, cv=10)
        results[alph] = scores.mean()
    best_alpha = max(results, key=lambda k:results[k])
    selected_mod = model.set_params(alpha = best_alpha)
    selected_mod.fit(X_train, y_train)
    score = selected_mod.score(X_test, y_test)
    mod_pred = selected_mod.predict(X_test)

    print(mod, 'accuracy', score)
    residuals = y_test - mod_pred
    residual_df[model_names[index]] = residuals
    print(type(y_test), type(mod_pred))

    plt.scatter(X_test['Seedwt'], residuals)
    plt.title('{:s} Regression Residual Scatter Plot'.format(model_names[index]))
    plt.xlabel('Seedwt (Predictor)')
    plt.ylabel('Residual')
    plt.savefig('{:s}-res-scatter.png'.format(model_names[index]))
    ##plt.show()
    plt.clf()

    plt.scatter(y_test, mod_pred)
    plt.plot(np.arange(8, 500), np.arange(8, 500), c="r", label=score)
    plt.legend(loc="lower right")
    plt.xlabel('Actual GDD')
    plt.ylabel('Predicted GDD')
    title = '{:s} Regression Prediction Accuracy'.format(model_names[index])
    plt.title(title)
    plt.savefig('{:s}-accuracy.png'.format(model_names[index]))
    #plt.show()
    plt.clf()

    plt.scatter(mod_pred, residuals)
    plt.title('{:s} Regression Residuals Against Predicted'.format(model_names[index]))
    plt.xlabel('Predictions')
    plt.ylabel('Residuals')
    plt.savefig('{:s}-res-pred.png'.format(model_names[index]))
    #plt.show()
    plt.clf()

#
# Random Forest Regression
# n_jobs = -1 runs on all available processors on your computer
#
#
estimators = [1,2,3,4,5,6,7,8,9,10,20,30,40,50]
results = {}
for est in estimators:
    rf = RandomForestRegressor(n_estimators=est, n_jobs=-1)
    scores = model_selection.cross_val_score(rf, predictor_cols, predict, cv=10)
    print('random forest accuracy for est', est, ':', scores.mean(), ' with std deviation:', scores.std()*2)
    results[est] = scores.mean()
highest_est = max(results, key=lambda k:results[k])

# The purpose of cross validation is model checking, not model building
# when using the model_selection.cross_val_scores, you can put in the whole data
# the cross validation is testing how well the model can get trained by some data and then predict data it hasn't seen.
# We test some different models with cross validation and then use the highest performing one as the model we want to use.
# We can use all of the data to train that final model.
rf_final = RandomForestRegressor(n_estimators=highest_est, n_jobs=-1)
cv = model_selection.ShuffleSplit(n_splits=30, test_size=0.3, random_state=0)
cross_val_scores = np.mean(model_selection.cross_val_score(rf_final, X_train, y_train, cv=cv))
print('cross val scores', cross_val_scores)

rf_results = rf_final.fit(X_train, y_train)
scores = rf_final.score(X_test, y_test)
print('Random Forest Score Accuracy on Test Set', scores)
rf_pred = rf_final.predict(X_test)

residuals = y_test - rf_pred
residual_df['Random Forest'] = residuals
plt.scatter(X_test['Seedwt'], residuals)
plt.title('Random Forest Residual Scatter Plot')
plt.xlabel('Seedwt (Predictor)')
plt.ylabel('Residual')
plt.savefig('RF-resid-scatter.png')
#plt.show()
plt.clf()



plt.scatter(y_test, rf_final.predict(X_test))
plt.plot(np.arange(8, 500), np.arange(8, 500), c="r", label=scores)
plt.legend(loc="lower right")
plt.title("RandomForest Regression Prediction Accuracy")
plt.xlabel('Actual GDD')
plt.ylabel('Predicted GDD')
plt.savefig('RF-accuracy.png')
#plt.show()
plt.clf()


plt.scatter(rf_pred, residuals)
plt.title('Random Forest Regression Residuals Against Predicted')
plt.xlabel('Predictions')
plt.ylabel('Residuals')
plt.savefig('RF-resid-pred.png')
#plt.show()
plt.clf()


# decision tree
dtree = DecisionTreeRegressor(max_depth=9, min_samples_leaf=40)
cv = model_selection.ShuffleSplit(n_splits=30, test_size=0.3, random_state=0)
cross_val_scores = np.mean(model_selection.cross_val_score(dtree, X_train, y_train, cv=cv))
print('cross val scores', cross_val_scores)


dtree_results = dtree.fit(X_train, y_train)
scores = dtree.score(X_test, y_test)
print('Decision Tree Score Accuracy on Test Set', scores)
dt_pred = dtree.predict(X_test)

# draw the tree and save as a pdf!
dotfile = StringIO()
sklearn.tree.export_graphviz(dtree, out_file=dotfile, feature_names=X_test.columns)
graph = pydotplus.graph_from_dot_data(dotfile.getvalue())
graph.write_pdf("decision_tree.pdf")

residuals = y_test - dt_pred
residual_df['Decision Tree'] = residuals
plt.scatter(X_test['Seedwt'], residuals)
plt.title('Decision Tree Residual Scatter Plot')
plt.xlabel('Seedwt (Predictor)')
plt.ylabel('Residual')
plt.savefig('DT-resid-scatter.png')
#plt.show()
plt.clf()

plt.scatter(y_test, dtree.predict(X_test))
plt.plot(np.arange(8, 500), np.arange(8, 500), c="r", label=scores)
plt.legend(loc="lower right")
plt.title("Decision Tree Regression Prediction Accuracy")
plt.xlabel('Actual GDD')
plt.ylabel('Predicted GDD')
plt.savefig('DT-accuracy.png')
#plt.show()
plt.clf()

plt.scatter(dt_pred, residuals)
plt.title('Decision Tree Regression Residuals Against Predicted')
plt.xlabel('Predictions')
plt.ylabel('Residuals')
plt.savefig('DT-resid-pred.png')
#plt.show()
plt.clf()

#boxplot of residuals of models used
ax = residual_df.boxplot()
plt.title('Boxplot of Regression Residuals')
plt.xlabel('Type of Regression')
plt.ylabel('Residual')
plt.savefig('boxplot.png')
#plt.show()
plt.clf()

