import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class TitanicFeatureEngineer(
    BaseEstimator,
    TransformerMixin
):

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        df = X.copy()

        # Family size
        df["FamilySize"] = (
            df["SibSp"] +
            df["Parch"] +
            1
        )

        # Alone
        df["IsAlone"] = (
            df["FamilySize"] == 1
        ).astype(int)

        # Title
        df["Title"] = (
            df["Name"]
            .str.extract(r",\s*([^.]*)\.")[0]
            .str.strip()
        )

        common_titles = [
            "Mr",
            "Miss",
            "Mrs",
            "Master"
        ]

        df["Title"] = df["Title"].where(
            df["Title"].isin(common_titles),
            "Rare"
        )

        # Cabin
        df["HasCabin"] = (
            df["Cabin"]
            .notna()
            .astype(int)
        )

        df["Deck"] = (
            df["Cabin"]
            .str[0]
            .fillna("Unknown")
        )

        # Drop high-cardinality/raw columns
        df = df.drop(
            columns=[
                "PassengerId",
                "Name",
                "Ticket",
                "Cabin"
            ],
            errors="ignore"
        )

        return df