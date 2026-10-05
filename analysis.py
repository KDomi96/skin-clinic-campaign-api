"""Response rate breakdowns for the skin clinic campaign."""
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).parent / "data" / "skin_clinic_campaign.csv"


def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    # 1/0 flag makes the response rate just a mean
    df["responded"] = (df["Response_to_Campaign"] == "Yes").astype(int)
    return df


def response_table(df, column, order=None):
    """Customers, responders and response rate (%) for each value of `column`."""
    out = (
        df.groupby(column, observed=True)["responded"]
        .agg(Customers="count", Responders="sum", mean="mean")
        .reset_index()
    )
    out["Response Rate (%)"] = (out.pop("mean") * 100).round(2)
    if order:
        out[column] = pd.Categorical(out[column], categories=order, ordered=True)
        out = out.sort_values(column)
        out[column] = out[column].astype(str)
    return out.reset_index(drop=True)


def build_tables(df):
    """The four tables from the assignment, keyed by title."""
    # raw product counts go from 1 to 15, so bucket them as the task says
    df = df.assign(
        Product_Usage=pd.cut(
            df["Unique_Products_Purchased"],
            bins=[0, 4, 8, float("inf")],
            labels=["1-4", "5-8", ">8"],
        )
    )

    t1 = response_table(df, "Gender")
    t2 = response_table(df, "AgeGroup", order=["<30", "30-50", ">50"]).rename(
        columns={"AgeGroup": "Age Group"}
    )
    t3 = response_table(df, "Purchase_Last_Quarter", order=["Yes", "No"]).rename(
        columns={"Purchase_Last_Quarter": "Purchase in Last Quarter"}
    )
    t4 = response_table(df, "Product_Usage", order=["1-4", "5-8", ">8"]).rename(
        columns={"Product_Usage": "Unique Products (Last Year)"}
    )

    return {
        "1. Gender vs Campaign Response": t1,
        "2. Age Group vs Campaign Response": t2,
        "3. Purchase in Last Quarter vs Campaign Response": t3,
        "4. Product Usage vs Campaign Response": t4,
    }


if __name__ == "__main__":
    data = load_data()
    print(f"Overall response rate: {data['responded'].mean() * 100:.2f}%\n")
    for title, table in build_tables(data).items():
        print(title)
        print(table.to_string(index=False))
        print()
