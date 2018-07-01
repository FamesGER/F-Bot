class botgspread():
	def __init__(self,sheetName= 'F-Botsheet',jsonFile):
		self.sName = sheetName	
		self.jFile = jsonFile

	def getClient(self): #create the client
		import gspread
		from oauth2client.service_account import ServiceAccountCredentials
		scope = ['https://spreadsheets.google.com/feeds',
		         'https://www.googleapis.com/auth/drive']
		#creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
		creds = ServiceAccountCredentials.from_json('client_secret.json',scope)

		client = gspread.authorize(creds)
		return client
	def getSheet(self): #access the sheet
		import gspread
		from oauth2client.service_account import ServiceAccountCredentials#
		import pprint

		sheet = self.getClient().open(self.sName).sheet1
		return sheet

	def row_val(self, row = 1):
		sheet = self.getSheet()
		rowVal = sheet.row_values(row)
		return rowVal
	def cell_val(self,row=1, col=1):
		sheet= self.getSheet()
		cellVal = sheet.cell(row,col).value
		return cellVal