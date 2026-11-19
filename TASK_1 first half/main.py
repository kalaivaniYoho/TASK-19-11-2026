
import pandas as pd

# Load employee dataset
df = pd.read_csv("employee_data.csv")

# Before cleaning summary
before = {
    "Rows": len(df),
    "Missing Values": df.isnull().sum().sum(),
    "Duplicates": df.duplicated().sum()
}

# Remove duplicate records
df = df.drop_duplicates().copy()

# Fix data types
df["employee_id"] = pd.to_numeric(df["employee_id"], errors="coerce")
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
df["joining_date"] = pd.to_datetime(df["joining_date"], errors="coerce")

# Standardize text
for col in ["name", "department", "city"]:
    df[col] = df[col].astype("string").str.strip().str.title()

# Fill missing numeric values with median
for col in ["age", "salary"]:
    df[col] = df[col].fillna(df[col].median())

# Fill missing categorical values with mode
for col in ["name", "department", "city"]:
    if df[col].isna().any():
        df[col] = df[col].fillna(df[col].mode()[0])

# Drop records without essential IDs or dates
df = df.dropna(subset=["employee_id", "joining_date"])

# Detect salary outliers using IQR
q1 = df["salary"].quantile(0.25)
q3 = df["salary"].quantile(0.75)
iqr = q3 - q1

lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

outliers = df[
    (df["salary"] < lower) | (df["salary"] > upper)
]

print("Salary outliers detected:")
print(outliers[["employee_id", "salary"]])

# Decision: flag outliers instead of removing them
df["salary_outlier"] = (
    (df["salary"] < lower) | (df["salary"] > upper)
)

# After cleaning summary
after = {
    "Rows": len(df),
    "Missing Values": df.isnull().sum().sum(),
    "Duplicates": df.duplicated().sum()
}

summary = pd.DataFrame({
    "Before": before,
    "After": after
})

print("\nBefore / After Cleaning Summary:")
print(summary)

print("\nCleaning decisions:")
print("Age and salary: filled missing values with median.")
print("Text columns: trimmed and standardized to title case.")
print("Duplicate rows: removed.")
print("Invalid employee IDs or dates: rows removed.")
print("Salary outliers: flagged, not removed.")

# Save cleaned dataset
df.to_csv("clean_data.csv", index=False)

print("\nCleaned dataset saved as clean_data.csv")
