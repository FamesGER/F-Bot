class botgspread():
	def __init__(self,sheetName= 'F-Botsheet',sheetNumber= 0):
		self.sNumber = sheetNumber
		self.sName = sheetName	

	def getClient(self): #create the client
		import gspread
		from oauth2client.service_account import ServiceAccountCredentials
		scope = ['https://spreadsheets.google.com/feeds',
		         'https://www.googleapis.com/auth/drive']
		creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
		client = gspread.authorize(creds)
		return client
		
	def getSheet(self): #access the sheet
		import gspread
		from oauth2client.service_account import ServiceAccountCredentials#
		import pprint
		#get the sheet from the sheet name and number
		sheetTemp = self.getClient().open(self.sName)#open main sheet
		sheet= sheetTemp.get_worksheet(self.sNumber)#open the worksheet number with given index. 0->1->2...
		return sheet

	def delete_allrows(self):
		sheet = self.getSheet()
		for y in range(1,51):
			sheet.delete_row(1)		

	def delete_row(self,row=1):
		sheet = self.getSheet()
		sheet.delete_row(row)	

	def row_val(self, row = 1):
		sheet = self.getSheet()
		rowVal = sheet.row_values(row)
		return rowVal

	def col_val(self, col = 1):
		sheet = self.getSheet()
		colVal = sheet.col_values(col)
		return colVal

	def cell_val(self,row=1, col=1):
		sheet= self.getSheet()
		cellVal = sheet.cell(row,col).value
		return cellVal

	def cell_upd(self, row= 1, col= 1, val= "0"):
		sheet= self.getSheet()
		sheet.update_cell(row,col,val)

	def row_ins(self,val=[],row=1):
		sheet=self.getSheet()
		sheet.insert_row(val,row)


