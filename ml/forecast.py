import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def forecast_cpu(df):

    if len(df) < 20:
        return None

    df["lag1"] = df["cpu"].shift(1)
    df["lag2"] = df["cpu"].shift(2)

    df = df.dropna()

    X = df[["lag1", "lag2"]]
    y = df["cpu"]

    model = RandomForestRegressor()

    model.fit(X, y)

    latest = X.iloc[-1:]

    prediction = model.predict(latest)

    return prediction[0]