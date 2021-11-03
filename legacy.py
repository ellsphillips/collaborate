# Importing packages for use
import pandas as pd
import random


# Import folder should have 2 excel files:
# - List of memebers
# - List of previous matches
Path_import = r'C:\Users\mcferr\OneDrive - Office for National Statistics\Docs\Monthly_Matches_New'
Path_export = r'C:\Users\mcferr\OneDrive - Office for National Statistics\Docs\Monthly_Matches_New'


# Load members data
collaborate_data = pd.read_excel(Path_import+ r'\1_Collaborate_Signup.xlsx')

# Load previous matches
previous_matches = pd.read_excel(Path_import + r'\2_Collaborate_previous_matches.xlsx', index_col=0)

# Merge previously matched emails to create unique identifier
previous_matches['check_string'] = previous_matches.apply(lambda row: ''.join(sorted([row['Email Address 1'], row['Email Address 2']])), axis=1)

# Save all emails to a list
emails = list(collaborate_data['Email address (please use your ONS account)'])

# Print and remove duplicates
if len(emails) != len(set(emails)):
    print(set([x for x in emails if emails.count(x) > 1]))
    emails = list(set(emails))

# Initialise empty list for new matches
matches=[]

# Check even email count, remove auther email if odd
if len(emails) % 2 == 1:
    emails.remove('richard.mcferran@ons.gov.uk')

# Select email without replacement, then a second email
# Check if this pair is in the previous cohort of matches, if so reselect
while len(emails) > 0:
    index1 = random.randint(0, len(emails) - 1)
    email1 = emails[index1]
    emails.pop(index1)

    unique = False
    while unique == False:
        index2 = random.randint(0,len(emails)-1)
        email2 = emails[index2]
        email_pair = [email1, email2]
        UI = ''.join(sorted(email_pair))
        unique = not any(n in UI for n in previous_matches.iloc[:, 2])
    
    emails.pop(index2)
    matches.append(email_pair)
    

matches1 = pd.DataFrame(matches, columns={'Email Address 1', 'Email Address 2'})
matches2 = matches1.copy()
matches2.rename(
    columns={
        'Email Address 2': 'Email Address 1',
        'Email Address 1': 'Email Address 2'
    },
    inplace=True
);

# Merge the 2 dataframes to create a version with both orderings of the matches
frames = [matches2, matches1]
matches = pd.concat(frames).copy()

# Lowercase all emails
matches['Email Address 1'] = matches['Email Address 1'].str.lower()

# Sort all emails in alphebetical order of 'Email Address 1'
matches.sort_values(by=['Email Address 1'],inplace=True)



# Check if particular matches have occurred in previous months
# (master collaborate matches spreadsheet)
matches['check_string'] = matches.apply(lambda row: ''.join(sorted([row['Email Address 1'], row['Email Address 2']])), axis=1)
already_matched = matches.merge(previous_matches, on='check_string', how='left')
already_matched = already_matched.dropna()



from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Output the new matches
Matches_table=load_workbook(Path_export+r'\5_Collaborate_Matches_Table.xlsx')
del Matches_table['Python Output New']
Output_sheet=Matches_table.create_sheet('Python Output New')
Output_sheet.title='Python Output New'
for r in dataframe_to_rows(matches, index=True, header=True):
    Output_sheet.append(r)

# Output the new collaborate list 
del Matches_table['Collaborate list']
Output_sheet=Matches_table.create_sheet('Collaborate list')
Output_sheet.title='Collaborate list'
for r in dataframe_to_rows(collaborate_data, index=True, header=True):
    Output_sheet.append(r)
Matches_table.save(filename=Path_export+r'\5_Collaborate_Matches_Table.xlsx')   

# Add the new matches onto previous_matches
previous_matches=pd.read_excel(Path_import+r'\2_Collaborate_previous_matches.xlsx')
previous_matches=pd.concat([previous_matches,matches1])
writer = pd.ExcelWriter(Path_export+r'\2_Collaborate_previous_matches.xlsx', engine='xlsxwriter')
previous_matches.to_excel(writer)
writer.save()
writer.close()
