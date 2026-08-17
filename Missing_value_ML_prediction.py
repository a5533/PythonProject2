import os
import pandas as pd
from sklearn.linear_model import LinearRegression

# --- HARDCODE YOUR EXACT EXCEL FILE PATH HERE ---
# (Keep the 'r' before the string so Windows backslashes don't cause errors)
file_path = r"C:\Users\91770\Downloads\Student_Grade_Management_1.xlsx"

print(f"Attempting to modify file at: {file_path}")

# Load data specifying both openpyxl engine and sheet name
df = pd.read_excel(
    file_path, sheet_name="Student_Grade_Management", engine="openpyxl"
)

# Define subject columns
subjects = ["Sub1", "Sub2", "Sub3", "Sub4", "Sub5"]

# 2. Fill missing subject values with row-wise mean of available subjects
df[subjects] = df[subjects].apply(lambda row: row.fillna(row.mean()), axis=1)

# Round scores to 1 decimal place
df[subjects] = df[subjects].round(1)

# 3. Recalculate Total, Average, and Grade
df["Total"] = df[subjects].sum(axis=1)
df["Average"] = (df["Total"] / len(subjects)).round(1)


def assign_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"


df["Grade"] = df["Average"].apply(assign_grade)

# --- SAVE UPDATED DATA BACK TO EXCEL ---
try:
    df.to_excel(
        file_path, sheet_name="Student_Grade_Management", index=False, engine="openpyxl"
    )
    print(
        "--- Success: Updated values and recalculated fields saved back to Excel file! ---\n"
    )
except PermissionError:
    print(
        "\n[ERROR] Permission Denied: Please close 'Student_Grade_Management_1.xlsx' in Excel and run the script again."
    )
    exit()

print("=== CLEANED STUDENT DATA ===")
print(df[["Roll No", "Name"] + subjects + ["Total", "Average", "Grade"]])

# ---------------------------------------------------------
# 4. MACHINE LEARNING: PREDICT NEXT STUDENT'S PERFORMANCE
# ---------------------------------------------------------
X = df[["Sub1", "Sub2", "Sub3", "Sub4"]]
y = df["Sub5"]

# Split data: 80% for training, 20% for testing
# (If your dataset is very small, adjust test_size or set a fixed random_state)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, random_state=42
)

# Initialize and train the model on the training set
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model on the test set
y_pred_test = model.predict(X_test)

print("===score method is used on the trained data to know the accuracy===")
accuracy=model.score(X_train, y_train)
print(f"Accuracy of the prediction: {accuracy}")
mse = mean_squared_error(y_test, y_pred_test)
r2 = r2_score(y_test, y_pred_test)

print("\n=== MODEL PERFORMANCE ON TEST DATA ===")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"R² Score: {r2:.2f}")

# Predict performance for 11th student (Amit Sharma)
new_student_initial_marks = pd.DataFrame(
    [[80.0, 82.0, 85.0, 81.0]], columns=["Sub1", "Sub2", "Sub3", "Sub4"]
)

predicted_sub5 = round(model.predict(new_student_initial_marks)[0], 1)

all_marks = [80.0, 82.0, 85.0, 81.0, predicted_sub5]
predicted_total = round(sum(all_marks), 1)
predicted_avg = round(predicted_total / 5, 1)

print("\n--- Predicted Record for Student 11 (Amit Sharma) ---")
print("Sub1: 80.0 | Sub2: 82.0 | Sub3: 85.0 | Sub4: 81.0")
print(f"Predicted Sub5 (via ML Linear Regression): {predicted_sub5}")
print(f"Predicted Total: {predicted_total}")
print(f"Predicted Average: {predicted_avg}%")
print(f"Predicted Grade: {assign_grade(predicted_avg)}")
