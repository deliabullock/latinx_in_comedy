CATEGORY_WORDS = ["descent", "origin", "latin"]
MAIN_TEXT_WORDS = ["descent", "origin", "Latin", "born", "raised", "mother", "father", "parent", "latino", "latina"]

def keep_category(category):
	for x in CATEGORY_WORDS:
		if x in category:
			return True
	return False

def get_birthplace(raw_text):
	#info_box = raw_text.split("'''")[0]
	index = raw_text.find("birth_place")
	print index
	if index > -1:
		#TODO: account for | existing earlier with [[
		bp = raw_text[index + len("birth_place"):].split("|", 1)[0] 
		return bp
	return ""
