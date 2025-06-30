import pandas as pd

df1 = pd.read_excel("Excel_Queries.xlsx", sheet_name="T_DocLog")

df1.drop(columns=['Column3', 'DOCR'], inplace=True)

# Example: Remove duplicate rows in df1
df1=df1.drop_duplicates()

# Convert date columns to datetime format in df1_cleaned
# Use errors='coerce' to turn unparseable dates into NaT (Not a Time)
# Based on the column list, the correct column names are used below
df1['STD0'] = pd.to_datetime(df1['STD0'], errors='coerce')
df1['STD1']=pd.to_datetime(df1['STD1'], errors='coerce')
df1['STD2']=pd.to_datetime(df1['STD2'], errors='coerce')
df1['STD3'] = pd.to_datetime(df1['STD3'], errors='coerce')
df1['STD4'] = pd.to_datetime(df1['STD4'], errors='coerce')
df1['STD5']=pd.to_datetime(df1['STD5'], errors='coerce')
df1['STD12']=pd.to_datetime(df1['STD12'], errors='coerce')
df1['STD13']=pd.to_datetime(df1['STD13'], errors='coerce')
df1['ST22']=pd.to_datetime(df1['ST22'], errors='coerce')
df1['ST23']=pd.to_datetime(df1['ST23'], errors='coerce') # Corrected column name from ST23 to STD23
df1['STD02']=pd.to_datetime(df1['STD02'], errors='coerce')
df1['STD03']=pd.to_datetime(df1['STD03'], errors='coerce')
df1['REVIEW_C']=pd.to_datetime(df1['REVIEW_C'], errors='coerce')

# Rename columns in df1
new_column_names = {
    'SN': 'SN',
    'DOCTYPE': 'DOCUMENT TYPE',
    'DISC': 'DISCIPLINE',
    'Column2': 'CATEGORIES',
    'DOC_SUB': 'DOCUMENT NAME',
    'Vender Name': 'VENDOR',
    'System Action': 'SYSTEM',
    'SD_C': 'ATLAS SUBMISSION REFERENCE',
    'REV_C': 'CURRENT REV',
    # 'SUB DATE': 'SUB DATE', # 'SUB DATE' is not in the actual columns
    # 'REPLY REF': 'REPLY REF', # 'REPLY REF' is not in the actual columns
    # 'REPLY DATE': 'REPLY DATE', # 'REPLY DATE' is not in the actual columns
    # 'STATUS': 'DOCUMENT STATUS', # This will be overwritten later
    # 'STATUS CODE': 'STATUS CODE', # 'STATUS CODE' is not in the actual columns
    # 'REVIEW PERIOD': 'REVIEW PERIOD', # 'REVIEW PERIOD' is not in the actual columns
    # 'OVERDUE': 'OVERDUE', # 'OVERDUE' is not in the actual columns
    # 'ATLAS SUBMISSION REFERENCE.1': 'ATLAS SUBMISSION REFERENCE.1', # 'ATLAS SUBMISSION REFERENCE.1' is not in the actual columns
    # 'SUBMISSION DATE': 'SUBMISSION DATE', # 'SUBMISSION DATE' is not in the actual columns
    # 'DAR REFERENCE': 'DAR REFERENCE', # 'DAR REFERENCE' is not in the actual columns
    # 'DAR SUBMISSION DATE': 'DAR SUBMISSION DATE', # 'DAR SUBMISSION DATE' is not in the actual columns
    'REPLY REF.1': 'REPLY REF.1',
    'REPLY DATE.1': 'REPLY DATE.1',
    'STATUS CODE.1': 'STATUS CODE.1',
    'REVIEW PERIOD.1': 'REVIEW PERIOD.1',
    # 'ATLAS SUBMISSION REFERENCE.2': 'ATLAS SUBMISSION REFERENCE.2', # 'ATLAS SUBMISSION REFERENCE.2' is not in the actual columns
    'SUBMISSION DATE.1': 'SUBMISSION DATE.1',
    'DAR REERENCE NUMBER': 'DAR REERENCE NUMBER',
    'DAR SUBMISSION DATE.1': 'DAR SUBMISSION DATE.1',
    'REPLY REF.2': 'REPLY REF.2',
    'REPLY DATE.2': 'REPLY DATE.2',
    'STATUS CODE.2': 'STATUS CODE.2',
    'REVIEW PERIOD.2': 'REVIEW PERIOD.2',
    # 'ATLAS SUBMISSION REFERENCE.3': 'ATLAS SUBMISSION REFERENCE.3', # 'ATLAS SUBMISSION REFERENCE.3' is not in the actual columns
    'SUBMISSION DATE.2 ': 'SUBMISSION DATE.2',
    'DAR REERENCE NUMBER.1': 'DAR REERENCE NUMBER.1',
    'DAR SUBMISSION DATE.2': 'DAR SUBMISSION DATE.2',
    'REPLY REF.3': 'REPLY REF.3',
    'REPLY DATE.3 ': 'REPLY DATE.3',
    'STATUS CODE.3': 'STATUS CODE.3',
    'REVIEW PERIOD.3': 'REVIEW PERIOD.3',
    # 'ATLAS SUBMISSION REFERENCE.4': 'ATLAS SUBMISSION REFERENCE.4', # 'ATLAS SUBMISSION REFERENCE.4' is not in the actual columns
    'CURRENT REV.1': 'CURRENT REV.1',
    'REPLY REF.4': 'REPLY REF.4',
    'REPLY DATE.4': 'REPLY DATE.4',
    'STATUS CODE.4': 'STATUS CODE.4',
    'REVIEW PERIOD.4': 'REVIEW PERIOD.4',
    # 'ATLAS SUBMISSION REFERENCE.5': 'ATLAS SUBMISSION REFERENCE.5', # 'ATLAS SUBMISSION REFERENCE.5' is not in the actual columns
    'CURRENT REV.2': 'CURRENT REV.2',
    'REPLY REF.5': 'REPLY REF.5',
    'REPLY DATE.5': 'REPLY DATE.5',
    'STATUS CODE.5': 'STATUS CODE.5',
    'REVIEW PERIOD.5': 'REVIEW PERIOD.5',
    # 'ATLAS SUBMISSION REFERENCE.6': 'ATLAS SUBMISSION REFERENCE.6', # 'ATLAS SUBMISSION REFERENCE.6' is not in the actual columns
    'CURRENT REV.3': 'CURRENT REV.3',
    'REPLY REF.6': 'REPLY REF.6',
    'REPLY DATE.6': 'REPLY DATE.6',
    'STATUS CODE.6': 'STATUS CODE.6',
    'REVIEW PERIOD.6': 'REVIEW PERIOD.6',
    'Action': 'FORECAST  / ACTION BY' # Assuming 'Action' is the correct column for this
}

# Filter out columns that are not in df1's current columns
new_column_names = {k: v for k, v in new_column_names.items() if k in df1.columns}

df1 = df1.rename(columns=new_column_names)

# Create the 'DOCUMENT STATUS' column
# Define the conditions for 'SUBMITTED' based on STATUS_C column using the actual unique values
submitted_conditions = (df1['STATUS_C'].isin(['Code 1', 'Code 2', 'UR (ATJV)', 'AR (ATJV)', 'UR (DAR)', 'Code 3']))

df1['DOCUMENT STATUS'] = 'PENDING' # Default to PENDING
df1.loc[submitted_conditions, 'DOCUMENT STATUS'] = 'SUBMITTED' # Set to SUBMITTED based on conditions


df1_cleaned=df1

df2_cleaned = pd.read_excel("Excel_Queries.xlsx",sheet_name="T_SDLog")

# Convert date columns to datetime format in df2_cleaned
# Use errors='coerce' to turn unparseable dates into NaT (Not a Time)
# Based on the column list, the correct column names are used below
df2_cleaned['S_DATE'] = pd.to_datetime(df2_cleaned['S_DATE'], errors='coerce')
df2_cleaned['C_DATE'] = pd.to_datetime(df2_cleaned['C_DATE'], errors='coerce')
df2_cleaned['ASUB_0'] = pd.to_datetime(df2_cleaned['ASUB_0'], errors='coerce')
df2_cleaned['ASUB_1'] = pd.to_datetime(df2_cleaned['ASUB_1'], errors='coerce')
df2_cleaned['ASUB_2'] = pd.to_datetime(df2_cleaned['ASUB_2'], errors='coerce')
df2_cleaned['ASUB_3'] = pd.to_datetime(df2_cleaned['ASUB_3'], errors='coerce')
df2_cleaned['ASUB_4'] = pd.to_datetime(df2_cleaned['ASUB_4'], errors='coerce')
df2_cleaned['ASUB_5'] = pd.to_datetime(df2_cleaned['ASUB_5'], errors='coerce')
df2_cleaned['ASUB_6'] = pd.to_datetime(df2_cleaned['ASUB_6'], errors='coerce')
df2_cleaned['ASUB_7'] = pd.to_datetime(df2_cleaned['ASUB_7'], errors='coerce')
df2_cleaned['ASUB_02'] = pd.to_datetime(df2_cleaned['ASUB_02'], errors='coerce')
df2_cleaned['ASUB_03'] = pd.to_datetime(df2_cleaned['ASUB_03'], errors='coerce')
df2_cleaned['REV_TIME'] = pd.to_datetime(df2_cleaned['REV_TIME'], errors='coerce')
df2_cleaned['REV_OD'] = pd.to_datetime(df2_cleaned['REV_OD'], errors='coerce')
df2_cleaned['JVCD_0'] = pd.to_datetime(df2_cleaned['JVCD_0'], errors='coerce')
df2_cleaned['JVCD_1'] = pd.to_datetime(df2_cleaned['JVCD_1'], errors='coerce')
df2_cleaned['JVCD_2'] = pd.to_datetime(df2_cleaned['JVCD_2'], errors='coerce')


# Example: Remove duplicate rows in df2
df2_cleaned = df2_cleaned.drop_duplicates()

# Rename columns in df2_cleaned
new_column_names_df2 = {
    'SN': 'Sn',
    'Sys': 'System',
    'Sub Sys': 'Sub System',
    'PN': 'Project Number',
    'Sub Con': 'Sub Contract',
    'BN': 'Building Number',
    'FL': 'Floor',
    'DZ': 'Drawing Zone',
    'Dec': 'Discipline',
    'Sub-Dec': 'Sub Discipline',
    'DS': 'Drawing Stage',
    'D_SEQ': 'Drawing Sequence',
    'DRW NO': 'Drawing Number',
    'ZONE': 'Zone',
    'FC_DATE ': 'Forecast Date',
    'REV_TIME': 'Review Time Days',
    'REV_OD': 'Review Time Overdue',
    '25': '25', # Assuming '25' is meant to be a column name
    'S_DATE': 'S_Date',
    '27': '27', # Assuming '27' is meant to be a column name
    '28': '28', # Assuming '28' is meant to be a column name
    'C_DATE': 'C_Date',
    '292': '292', # Assuming '292' is meant to be a column name
    'C_STATUS': 'Drawing Submission Status', # Use the correct column for the status
    'BY2': 'By2', # Assuming 'By2' is meant to be a column name
    'AREF_0': 'Aref_0',
    'ASUB_0': 'Asub_0',
    'ASUB_02': 'Asub_02',
    'ASUB_03': 'Asub_03',
    'JVREF_0': 'Jvref_0',
    'JVC_0': 'Jvc_0',
    'JVCD_0': 'Jvcd_0',
    'CMAC_0': 'Cmac_0',
    'AREF_1': 'Aref_1',
    'ASUB_1': 'Asub_1',
    'JVREF_1': 'Jvref_1',
    'JVC_1': 'Jvc_1',
    'JVCD_1': 'Jvcd_1',
    'CMAC_1': 'Cmac_1',
    'AREF_2': 'Aref_2',
    'ASUB_2': 'Asub_2',
    'JVREF_2': 'Jvref_2',
    'JVC_2': 'Jvc_2',
    'JVCD_2': 'Jvcd_2',
    'CMAC_2': 'Cmac_2',
    'AREF_3': 'Aref_3',
    'ASUB_3': 'Asub_3',
    'JVREF_3': 'Jvref_3',
    'JVC_3': 'Jvc_3',
    'JVCD_3': 'Jvcd_3',
    'CMAC_3': 'Cmac_3',
    'AREF_4': 'Aref_4',
    'ASUB_4': 'Asub_4',
    'JVREF_4': 'Jvref_4',
    'JVC_4': 'Jvc_4',
    'JVCD_4': 'Jvcd_4',
    'CMAC_4': 'Cmac_4',
    'AREF_5': 'Aref_5',
    'ASUB_5': 'Asub_5',
    'JVREF_5': 'Jvref_5',
    'JVC_5': 'Jvc_5',
    'JVCD_5': 'Jvcd_5',
    'CMAC_5': 'Cmac_5',
    'AREF_6': 'Aref_6',
    'ASUB_6': 'Asub_6',
    'JVREF_6': 'Jvref_6',
    'JVC_6': 'Jvc_6',
    'JVCD_6': 'Jvcd_6',
    'CMAC_6': 'Cmac_6',
    'AREF_7': 'Aref_7',
    'ASUB_7': 'Asub_7',
    'JVREF_7': 'Jvref_7',
    'JVC_7': 'Jvc_7',
    'JVCD_7': 'Jvcd_7',
    'CMAC_7': 'Cmac_7',
    'C_STATUS': 'Drawing Submission Status', # Use the correct column for the status
    'Current Status': 'Current Status'
}

# Define the conditions for 'PENDING' based on '28' column being '---' after stripping whitespace
pending_condition_df2 = (df2_cleaned['28'].astype(str).str.strip() == '---')


# Filter out columns that are not in df2_cleaned's current columns
new_column_names_df2 = {k: v for k, v in new_column_names_df2.items() if k in df2_cleaned.columns}

df2_cleaned = df2_cleaned.rename(columns=new_column_names_df2)

# Create the 'Drawing Submission Status' column
df2_cleaned['Drawing Submission Status'] = 'SUBMITTED' # Default to SUBMITTED
df2_cleaned.loc[pending_condition_df2, 'Drawing Submission Status'] = 'PENDING' # Set to PENDING based on condition


df1_cleaned=df1


# Convert df1_cleaned to a CSV file
df1_cleaned.to_csv('df1_cleaned.csv', index=False)

# Convert df2_cleaned to a CSV file
df2_cleaned.to_csv('df2_cleaned.csv', index=False)