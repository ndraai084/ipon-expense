import pandas as pd  # sir paul library ng python
import matplotlib.pyplot as plt  # sir paul library ng python
import numpy as np  # sir paul library ng python
import os
from firebase_config import db
from datetime import datetime

# Transaction CRUD
def get_transactions(user_id):
    transactions_ref = db.collection("users").document(user_id).collection("transactions")
    docs = transactions_ref.stream()
    data = []
    for doc in docs:
        t = doc.to_dict()
        t['id'] = doc.id
        if 'date' not in t:
            t['date'] = datetime.now()
        data.append(t)

    def safe_date(transaction):

        date = transaction.get("date")

        if date is None:
            return datetime.min

        try:
            return date.replace(tzinfo=None)
        except:
            return datetime.min

    data.sort(
        key=safe_date,
        reverse=True
    )

    return data

def add_transaction(user_id, data):
    if "date" not in data:
        data["date"] = datetime.now()
    db.collection("users").document(user_id).collection("transactions").add(data)

def edit_transaction(user_id, trans_id, updated_data):
    if "date" not in updated_data:
        updated_data["date"] = datetime.now()
    db.collection("users").document(user_id).collection("transactions").document(trans_id).update(updated_data)

def delete_transaction(user_id, trans_id):
    db.collection("users").document(user_id).collection("transactions").document(trans_id).delete()

# Analytics
def calculate_balance(df):
    income = df[df["type"]=="income"]["amount"].sum()
    expense = df[df["type"]=="expense"]["amount"].sum()
    return income - expense

def calculate_total_income(df):
    return df[df["type"]=="income"]["amount"].sum()

def calculate_total_expense(df):
    return df[df["type"]=="expense"]["amount"].sum()

def compute_spending_by_category(df):
    if df.empty or "category" not in df.columns or "type" not in df.columns:
        return {}
    return df[df["type"]=="expense"].groupby("category")["amount"].sum().to_dict()

# Chart.js data preparation
def get_category_chart_data(df):
    if df.empty or "category" not in df.columns or "type" not in df.columns:
        return {"labels": [], "data": []}
    category_summary = df[df["type"]=="expense"].groupby("category")["amount"].sum()
    return {"labels": category_summary.index.tolist(), "data": category_summary.values.tolist()}

def get_income_expense_chart_data(df):
    if df.empty or "type" not in df.columns:
        return {"labels": ["Income","Expense"], "data":[0,0]}
    income = df[df["type"]=="income"]["amount"].sum()
    expense = df[df["type"]=="expense"]["amount"].sum()
    return {"labels":["Income","Expense"], "data":[float(income),float(expense)]}


def get_monthly_chart_data(df):

    if (
        df.empty
        or "date" not in df.columns
        or "type" not in df.columns
    ):
        return {
            "labels": [],
            "income": [],
            "expense": []
        }

    df = df.copy()

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["date"]
    )

    df["month_date"] = (
        df["date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    monthly = (
        df.groupby(
            ["month_date", "type"]
        )["amount"]
        .sum()
        .unstack(fill_value=0)
        .sort_index()
    )

    labels = [

        d.strftime("%b %Y")

        for d in monthly.index

    ]

    income = (
        monthly["income"].tolist()

        if "income" in monthly.columns

        else [0] * len(labels)
    )

    expense = (
        monthly["expense"].tolist()

        if "expense" in monthly.columns

        else [0] * len(labels)
    )

    return {

        "labels": labels,

        "income": income,

        "expense": expense

    }

# Default categories
DEFAULT_CATEGORIES = ["Food","Transportation","Utilities"]