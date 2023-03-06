import gspread
from datetime import datetime
from flask import Flask, request, jsonify
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("Badge_reader-898ab444a8eb.json", scope)
client = gspread.authorize(creds)

@app.route('/submit_data', methods=['POST'])
def submit_data():

    data = request.json

    month = datetime.now().strftime("%B")
    sheet = client.open("Pointage adab 2022/2023").worksheet(month)

    list_mail = sheet.col_values(1)
    mail = data['email']
    index = list_mail.index(mail)+1
    
    sheet.update_cell(index, 2, data['nom'])
    sheet.update_cell(index, 3, data['prenom'])
    sheet.update_cell(index, 4, data['tel'])
    sheet.update_cell(index, 5, data['dateR'])
    
    if (sheet.cell(index,6).value=="0"):
        sheet.update_cell(index, 6, data['Heure'])
        sheet.update_cell(index, 7, data['Commentaire'])
        sheet.update_cell(index, 8, "1")
    else:
        nbr = int(sheet.cell(index, 8).value)
        sheet.update_cell(index, (7+2*nbr), data['Heure'])
        sheet.update_cell(index, (8+2*nbr), data['Commentaire'])
        sheet.update_cell(index, 8, str(nbr+1))
        
    return jsonify({'message': 'Emargement effectué'}), 200    
    
if __name__=='__main__':
    app.run(threaded=True, port=5000)
