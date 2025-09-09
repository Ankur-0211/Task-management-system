import pandas as pd
import random
from datetime import datetime, timedelta

# Load your synthetic dataset
df = pd.read_csv("synthetic_task.csv")  # 👉 change to your file name

# Make sure dates are real datetimes
df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')

# If your End Dates are missing, randomly generate them to be 1-30 days after Start Date
missing_end_dates = df['End Date'].isnull()
df.loc[missing_end_dates, 'End Date'] = df.loc[missing_end_dates, 'Start Date'] + pd.to_timedelta(
    [random.randint(1, 30) for _ in range(missing_end_dates.sum())], unit='D'
)

# Compute Days Left
df['Days_Left'] = (df['End Date'] - df['Start Date']).dt.days

# 📌 1️⃣ Fix Priority based on Days Left
def map_priority(days_left):
    if days_left <= 3:
        return 'High'
    elif days_left <= 7:
        return 'Medium'
    else:
        return 'Low'

df['Priority'] = df['Days_Left'].apply(map_priority)

# 📌 2️⃣ Fix Task Type based on Description
def assign_task_type(description):
    text = str(description).lower()
    if any(word in text for word in ['bug', 'fix', 'error', 'issue']):
        return 'Bug Fix'
    elif any(word in text for word in ['add', 'implement', 'develop', 'feature']):
        return 'Feature Development'
    elif any(word in text for word in ['review', 'approve', 'merge']):
        return 'Code Review'
    elif any(word in text for word in ['client', 'request', 'support']):
        return 'Client Request'
    elif any(word in text for word in ['deploy', 'release']):
        return 'Deployment'
    elif any(word in text for word in ['test', 'qa', 'validate']):
        return 'Testing'
    elif any(word in text for word in ['doc', 'documentation', 'write']):
        return 'Documentation'
    elif any(word in text for word in ['refactor', 'clean']):
        return 'Refactoring'
    elif any(word in text for word in ['research', 'investigate']):
        return 'Research'
    else:
        return 'General Task'

df['Task Type'] = df['Description'].apply(assign_task_type)

# Drop helper if you want
df = df.drop(columns=['Days_Left'])

# Save
df.to_csv("tasks_fixed.csv", index=False)
print("✅ Fixed: Priority and Task Type now logically linked! File saved as 'tasks_fixed.csv'.")
