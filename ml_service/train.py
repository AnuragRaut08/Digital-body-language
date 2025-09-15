# ml_service/train.py
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# synthesize features that mimic plausible patterns
rng = np.random.RandomState(42)
n = 5000
typing_speed = rng.normal(loc=5.0, scale=2.0, size=n)   # chars/sec
avg_pause = rng.exponential(scale=300, size=n)           # ms
backspace_rate = rng.beta(1, 8, size=n)                  # proportion
scroll_depth = rng.uniform(10, 100, size=n)              # percent
click_rate = rng.normal(10, 4, size=n)                   # clicks/min

# label: higher typing speed, lower avg_pause, moderate backspace, high scroll_depth, high click_rate -> engaged
score = (typing_speed*0.4) - (avg_pause*0.002) - (backspace_rate*5) + (scroll_depth*0.03) + (click_rate*0.05)
y = (score + rng.normal(0,1,n) > np.percentile(score, 60)).astype(int)

X = np.vstack([typing_speed, avg_pause, backspace_rate, scroll_depth, click_rate]).T
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=200, random_state=42)
clf.fit(X_train, y_train)
probs = clf.predict_proba(X_test)[:,1]
print("AUC:", roc_auc_score(y_test, probs))

joblib.dump(clf, "model.pkl")
print("Saved model.pkl")

