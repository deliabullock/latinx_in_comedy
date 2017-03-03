import requests
import pprint
import json
import page_parser as pp
import xml.etree.ElementTree as et

FILE_NAME = '../oldcsv/orig_2.xml'
FILE_NAME_2 = '../oldcsv/orig_2.xml'

class XMLfile(object):

	def __init__(self, actors, movie_title):
		self.actors = {}
		self.title = movie_title
		for a in actors:
			self.actors[a.name] = a

	def find_actors(self):
		et.register_namespace('o', 'urn:schemas-microsoft-com:office:office')
		et.register_namespace('x', 'urn:schemas-microsoft-com:office:excel')
		et.register_namespace('ss', 'urn:schemas-microsoft-com:office:spreadsheet')
		et.register_namespace('html', 'http://www.w3.org/TR/REC-html40')

		tree = 0
		try:
			tree = et.parse(FILE_NAME)
		except Exception as e:
			print("Could not open " + FILE_NAME + ": " + str(e))
			return e

		r = tree.getroot()
		worksheets = r.findall('{urn:schemas-microsoft-com:office:spreadsheet}Worksheet')
		for worksheet in worksheets:
			name = worksheet.attrib['{urn:schemas-microsoft-com:office:spreadsheet}Name']
			if (name == 'Master List' or name == "1920's"):
				print (name)
				continue
			table = worksheet.find('{urn:schemas-microsoft-com:office:spreadsheet}Table')
			rows = table.findall('{urn:schemas-microsoft-com:office:spreadsheet}Row')
			for r in rows[3:]:
				count = 0
				name  = ""
				for cell in r.findall('{urn:schemas-microsoft-com:office:spreadsheet}Cell'):
					indx = get_index(cell)
					name2 = get_text(cell)
					print ("Name: " + name2)
					print ("Indx: " + indx)
					if name != "":
						if indx == "" or indx == "5":
							txt = get_text(cell)
							if txt == "Y":
								actors[name].on_file = 1
							else:
								actors[name].on_file = 0
						break
					if count == 3 or indx == '4':
						name = get_text(cell)
						if name != "" and name not in self.actors:
							name = ""
							break
					if indx != "":
						count = int(indx) - 1 
					else:
						count += 1
					if count > 3:
						break
			self.final_table = table
			self.tree = tree

	def write_new_movie(self):
		for name, actor in self.actors.iteritems():
			row = et.Element('ss:Row', attrib={'ss:AutoFitHeight': '0'})
			cell = et.Element('ss:Cell', attrib={'ss:Index': '4'})
			data = et.Element('ss:Data', attrib={'ss:Type': 'String'})
			data.text = name
			cell.append(data)
			row.append(cell)
			self.final_table.append(row)
		self.tree.write(FILE_NAME_2)

def get_index(cell):
	if ('{urn:schemas-microsoft-com:office:spreadsheet}Index' in cell.attrib):
		return cell.attrib['{urn:schemas-microsoft-com:office:spreadsheet}Index']				
	return ""	

def get_text(cell):
	datas = cell.findall('{urn:schemas-microsoft-com:office:spreadsheet}Data')
	if len(datas) > 0:
		data = datas[0] 
		t = data.text
		t.strip()
		return t
	return ""
									
