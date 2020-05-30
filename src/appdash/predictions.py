import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder

from appdash.constants import DATA_DIR

# load our data
mtcars = pd.read_csv(DATA_DIR / "mtcars_dummy.csv",
                    dtype={'cyl': str,
                          'am': np.float64})

# create and fit a one-hot encoder--we'll want to reuse this in the app as well
cyl_enc = OneHotEncoder(categories='auto', sparse=False)
cyl_enc.fit(mtcars['cyl'].values.reshape(-1,1))

y = mtcars['mpg']
# we need to concatenate the one-hot (dummy) encoded values with
# the values from mtcars
X = np.concatenate(
    (mtcars[['disp', 'qsec', 'am']].values,
     cyl_enc.transform(mtcars['cyl'].values.reshape(-1,1))),
     axis=1)

# fit our regression model
fit = LinearRegression()
fit.fit(X=X, y=y)

def preds(fit, cyl_enc, disp, qsec, am, cyl):
    # construct our matrix
    X = np.concatenate(
        (np.array([[disp, qsec, am]]),
         cyl_enc.transform([[cyl]])),
         axis=1)
    # find predicted value
    pred = fit.predict(X)[0]
    # return a rounded string for nice UI display
    return str(round(pred, 2))

print(preds(fit, cyl_enc, 3650.0, 69.0, 0, "12"))