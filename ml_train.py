import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def gen(n=2000):
    X=[]; y=[]
    for i in range(n):
        cases = np.random.poisson(1)
        turbidity = np.random.exponential(1)
        bacterial = np.random.rand()
        season = np.random.choice([0,1])
        score = 0.3*cases + 0.4*(turbidity>3) + 0.5*(bacterial>0.4) + 0.6*season
        risk = 1 if score > 0.8 else 0
        X.append([cases, turbidity, bacterial, season]); y.append(risk)
    return pd.DataFrame(X, columns=["cases","turbidity","bacterial","season"]), pd.Series(y)

X,y = gen()
clf = RandomForestClassifier(n_estimators=50)
clf.fit(X,y)
joblib.dump(clf, "outbreak_model.joblib")
print("Saved model")