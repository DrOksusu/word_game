#pywordgame@trans-shuttle-363505.iam.gserviceaccount.com

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# scope = ['https://spreadsheets.google.com/feeds',
#          'https://www.googleapis.com/auth/drive']
#
# creds = ServiceAccountCredentials.from_json_keyfile_name('trans-shuttle-363505-ee60605dd1de.json', scope)
# client = gspread.authorize(creds)
#
# sheet = client.open('word_game').sheet1

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]
json_file_name = './trans-shuttle-363505-620063c62c4d.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)

spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1KP5J9GgfNLOE2f8QaoyZIuTpzwdH3uO92cQK9VERxd8/edit#gid=0'
# 스프레스시트 문서 가져오기
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet('level2')
list_data = worksheet.get_all_values()

print(list_data)




# json_file_name = 'trans-shuttle-363505-ee60605dd1de.json'
# gc = gspread.service_account(filename=json_file_name)
#
# sh = gc.open("word_game").worksheet("시트1")
#
# doc = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KP5J9GgfNLOE2f8QaoyZIuTpzwdH3uO92cQK9VERxd8/edit?usp=sharing')
# worksheet = doc.worksheet('word_game')
# print(worksheet)

