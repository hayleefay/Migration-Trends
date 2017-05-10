from sklearn import tree
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('migration_data.csv', low_memory=False)

X = df['fertility_1990_y']
X = X.values.reshape(-1, 1)
y = df['countryflow_1990']
clf = tree.DecisionTreeRegressor()
clf = clf.fit(X, y)
test_data = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]
test = clf.predict(test_data)

# plot results
plt.figure()
plt.scatter(X, y, c="darkorange", label="data")
plt.plot(test_data, test, color="cornflowerblue", label="max_depth=2", linewidth=2)
plt.xlabel("data")
plt.ylabel("target")
plt.title("Decision Tree Regression")
plt.legend()
plt.show()

# not able to handle NaN values
# need to first remove missing values before passing in

# need to split into training and test set
