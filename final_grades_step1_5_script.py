import pandas as pd

# Load the final grades file
final_grades_df = pd.read_csv(r"C:\Users\fstim\OneDrive\Investa Garden\Trade Block\tracking info\Step 5 Final Grades\final_grades.csv")

# Load the grade chart files for Step 2 and Step 4
step2_grade_travel_df = pd.read_csv(r"C:\Users\fstim\OneDrive\Investa Garden\Trade Block\Clean Format Data\Data Tables\Step2_Grade_Travel.csv")
step4_grade_chart_df = pd.read_csv(r"C:\Users\fstim\OneDrive\Investa Garden\Trade Block\Clean Format Data\Data Tables\Step4_total_days.csv")

# Process Step 1 and Step 3 for completeness
# Load the grade chart for Step 1 and 3
grade_chart_df = pd.read_csv(r"C:\Users\fstim\OneDrive\Investa Garden\Trade Block\Clean Format Data\Data Tables\Step1_3_grade_chart.csv")

# Load the grade chart for Step 5 (final grade lookup)
grade_chart_df = pd.read_excel(r"C:\Users\fstim\OneDrive\Investa Garden\Trade Block\Clean Format Data\Data Tables\Step5_fiale_grade.xlsx")



# Function to lookup points and grades from the grading chart for Steps 1 and 3
def lookup_points_and_grade(time_decimal, grade_chart_df):
    for idx, row in grade_chart_df.iterrows():
        if row['Step1_3_Hours_Start_HH:MM'] <= time_decimal <= row['Step1_3_Hours_End_HH:MM']:
            return row['Step1_3_Points_Start'], row['Step1_3_Grade']
    return None, None

# Function to format points and percentages
def format_points_and_percentage(points, total_points):
    if points is not None:
        formatted_points = round(points, 1)  # Round to 1 decimal
        percentage = round((formatted_points / total_points) * 100, 1)  # Calculate percentage
        return formatted_points, percentage
    return None, None

# Function to process Step 1 and Step 3 without overwriting existing columns
def process_tracking_numbers_correct(final_df, grade_chart_df, step1_column='Label to Arrive Hour/Minute Decimal', step3_column='Arrive to Delivery Hour/Minute Decimal'):
    # Initialize the columns for Step 1 if missing
    if 'Label to Arrive Points' not in final_df.columns:
        final_df['Label to Arrive Points'] = None
    if 'Label to Arrive Percentage' not in final_df.columns:
        final_df['Label to Arrive Percentage'] = None
    if 'Label to Arrive Grade' not in final_df.columns:
        final_df['Label to Arrive Grade'] = None

    # Initialize the columns for Step 3 if missing
    if 'Arrive to Delivery Points' not in final_df.columns:
        final_df['Arrive to Delivery Points'] = None
    if 'Arrive to Delivery Percent' not in final_df.columns:
        final_df['Arrive to Delivery Percent'] = None
    if 'Arrive to Delivery Grade' not in final_df.columns:
        final_df['Arrive to Delivery Grade'] = None

    for index, row in final_df.iterrows():
        # Process Step 1
        time_decimal_step1 = row[step1_column] if step1_column in row else None
        if pd.notna(time_decimal_step1):
            points, grade = lookup_points_and_grade(time_decimal_step1, grade_chart_df)
            if points is not None:
                formatted_points, percentage = format_points_and_percentage(points, 15)
                final_df.at[index, 'Label to Arrive Points'] = formatted_points
                final_df.at[index, 'Label to Arrive Percentage'] = percentage  # Fixing missing percentage
                final_df.at[index, 'Label to Arrive Grade'] = grade

        # Process Step 3
        time_decimal_step3 = row[step3_column] if step3_column in row else None
        if pd.notna(time_decimal_step3):
            points, grade = lookup_points_and_grade(time_decimal_step3, grade_chart_df)
            if points is not None:
                formatted_points, percentage = format_points_and_percentage(points, 15)
                final_df.at[index, 'Arrive to Delivery Points'] = formatted_points
                final_df.at[index, 'Arrive to Delivery Percent'] = percentage
                final_df.at[index, 'Arrive to Delivery Grade'] = grade

    return final_df

# Combined function for processing both Step 2 and Step 4
def process_step_correct(final_df, grade_chart_df, step_column, zone_column='Zone', step_hours_start_col=None, step_hours_end_col=None, points_col=None, grade_col=None, output_prefix=None):
    """
    Generic function to process steps (either Step 2 or Step 4) based on the column names provided.
    """
    # Initialize the columns for the step if missing
    points_col_name = f'{output_prefix} Points'
    percent_col_name = f'{output_prefix} Percent'
    grade_col_name = f'{output_prefix} Grade'

    if points_col_name not in final_df.columns:
        final_df[points_col_name] = None
    if percent_col_name not in final_df.columns:
        final_df[percent_col_name] = None
    if grade_col_name not in final_df.columns:
        final_df[grade_col_name] = None

    for index, row in final_df.iterrows():
        time_step = row[step_column] if step_column in row else None
        zone = row[zone_column] if zone_column in row else None
        if pd.notna(time_step) and pd.notna(zone):
            # Filter the grade chart data by zone
            zone_filtered_df = grade_chart_df[grade_chart_df['Zone'] == int(zone)]
            for _, zone_row in zone_filtered_df.iterrows():
                # Compare times and perform lookup
                if zone_row[step_hours_start_col] <= time_step <= zone_row[step_hours_end_col]:
                    points, grade = zone_row[points_col], zone_row[grade_col]
                    formatted_points, percentage = format_points_and_percentage(points, 25)
                    final_df.at[index, points_col_name] = formatted_points
                    final_df.at[index, percent_col_name] = percentage
                    final_df.at[index, grade_col_name] = grade
                    break

    return final_df

# Example of how to use this combined function for Step 2 and Step 4

# Load the final grades file
final_grades_df = pd.read_csv(r"C:\Users\fstim\OneDrive\Investa Garden\Trade Block\tracking info\Step 5 Final Grades\final_grades.csv")

# Load the grade chart files for Step 2 and Step 4
step2_grade_travel_df = pd.read_csv(r"C:\Users\fstim\OneDrive\Investa Garden\Trade Block\Clean Format Data\Data Tables\Step2_Grade_Travel.csv")
step4_grade_chart_df = pd.read_csv(r"C:\Users\fstim\OneDrive\Investa Garden\Trade Block\Clean Format Data\Data Tables\Step4_total_days.csv")

# Process Step 1 and Step 3 for completeness
# Load the grade chart for Step 1 and 3
grade_chart_df = pd.read_csv(r"C:\Users\fstim\OneDrive\Investa Garden\Trade Block\Clean Format Data\Data Tables\Step1_3_grade_chart.csv")

# Now you can use it in the processing step
final_grades_df_updated_step1_3 = process_tracking_numbers_correct(final_grades_df, grade_chart_df)

# Assuming this is your function definition
def process_step_correct(final_df, grade_chart_df, step_column, step_hours_start_col, step_hours_end_col, points_col, grade_col, output_prefix, total_points=None):
    # Your function logic here
    pass

# Process Step 2
final_grades_df = process_step_correct(
    final_df=final_grades_df_updated_step1_3, 
    grade_chart_df=step2_grade_travel_df, 
    step_column='Travel Hour/Minute Decimal', 
    step_hours_start_col='Step2_Hours_Start_HH:MM_Decimal', 
    step_hours_end_col='Step2_Hours_End_HH:MM_Decimal', 
    points_col='Step2_Points_Start', 
    grade_col='Step2_Grade', 
    output_prefix='Arrive to Arrived_at_Delivery_Facility'
)

# Process Step 4
final_grades_df = process_step_correct(
    final_df=final_grades_df, 
    grade_chart_df=step4_grade_chart_df, 
    step_column='Arrived_at_Facility to Delivered HH:MM Decimal', 
    step_hours_start_col='Step4_Hours_Start_HH:MM_Decimal', 
    step_hours_end_col='Step4_Hours_End_HH:MM_Decimal', 
    points_col='Step4_Points_Start', 
    grade_col='Step4_Grade', 
    output_prefix='Arrived to Delivered'
)

    
# Step 5 Combine all the points for each step for a final grade

# Ensure final_grades_df is correctly initialized and not None
if final_grades_df is None or not isinstance(final_grades_df, pd.DataFrame):
    raise ValueError("DataFrame final_grades_df is not properly defined.")

# Define the lookup function
def lookup_grade_by_percentage(percentage, grade_chart_df):
    for idx, row in grade_chart_df.iterrows():
        if row['Step1_3_Total_Start'] <= percentage <= row['Step1_3_Total_End']:
            return row['Step1_3_Grade']
    return None

# Add new columns for the grand totals if they don't exist
if 'Grand_Total_Points' not in final_grades_df.columns:
    final_grades_df['Grand_Total_Points'] = None
if 'Grand_Total_Percent' not in final_grades_df.columns:
    final_grades_df['Grand_Total_Percent'] = None
if 'Grand_Total_Grade' not in final_grades_df.columns:
    final_grades_df['Grand_Total_Grade'] = None

# Iterate over each row to calculate the totals and grades
for index, row in final_grades_df.iterrows():
    # Calculate Grand_Total_Points by summing up points from the steps
    total_points = (
        (row['Label to Arrive Points'] or 0) +
        (row['Arrive to Delivery Points'] or 0) +
        (row['Arrive to Arrived_at_Delivery_Facility Points'] or 0) +
        (row['Arrived to Delivered Points'] or 0)
    )
     # Calculate Grand_Total_Percent
    total_percent = (total_points / 90) * 100  # Max points is 90
    
    # Update the DataFrame with Grand_Total_Points and Grand_Total_Percent immediately
    final_grades_df.at[index, 'Grand_Total_Points'] = total_points
    final_grades_df.at[index, 'Grand_Total_Percent'] = total_percent
    
    # Now perform the grade lookup using the updated DataFrame
    total_grade = lookup_grade_by_percentage(total_percent, grade_chart_df)
    
    # Update the DataFrame with the grade
    final_grades_df.at[index, 'Grand_Total_Grade'] = total_grade

# Save the final result after processing all steps
final_grades_df.to_csv(r"C:\Users\fstim\OneDrive\Investa Garden\Trade Block\tracking info\Step 5 Final Grades\letter_grades_combined.csv", index=False)
print("Processing of Step 1, 2, 3, 4, and 5 completed and saved.")


















