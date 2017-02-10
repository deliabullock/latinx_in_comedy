from pyparsing import nestedExpr

CATEGORY_WORDS = ["descent", "origin", "latin"]
MAIN_TEXT_WORDS = ["descent", "origin", "latin", "born", "raised", "mother", "father", "parent", "latino", "latina"]

def keep_category(category):
	for x in CATEGORY_WORDS:
		if x in category:
			return True
	return False

def get_birthplace(raw_text):
	index = raw_text.find("birth_place")
	if index > -1:
		raw_bp = raw_text[index + len("birth_place"):].split("\n", 1)[0] 
		raw_bp = raw_bp.strip().strip('=').strip()
		bp = clean_text(raw_bp)
		return bp
	return ""

def clean_text(txt):
	brackets_l = {"{{", "[["}
	brackets_r = {"}}", "]]"}
	
	str_out = "" 
	x_outer = 0
	while x_outer < len(txt):
		if txt[x_outer] == '|':
			str_out = ""
			x_outer += 1
			continue 
		if txt[x_outer:x_outer+2] in brackets_l: 
			x_inner = x_outer + 2
			counter = 1
			bar_idx = -1
			while x_inner < len(txt):
				if counter == 0:
					break
				if txt[x_inner : x_inner + 2] in brackets_l:
					counter += 1
					x_inner = x_inner + 2
					continue
				if txt[x_inner : x_inner + 2] in brackets_r:
					counter -= 1
					x_inner = x_inner + 2
					continue
				x_inner += 1
			if counter != 0:
				print "Error in parsing: mismatched brackets!"
				return ""
			if bar_idx > 0:
				str_out += clean_text(txt[bar_idx + 1 : x_inner - 2 ])
			else:
				str_out += clean_text(txt[x_outer + 2 :x_inner - 2])
			x_outer = x_inner
			continue
		str_out += txt[x_outer]
		x_outer += 1
	return str_out		

def get_sentences(text):
	#TODO: make sure this is necessary
	sentences = text.split(".")
	sentences_out = []
	for x in sentences:
		sentence_tmp = ""
		if keep_sentence(x) > -1:
			idx = 0
			while idx < len(x):
				if x[idx] == '<':
					idx += 1
					while True:
						if x[idx] == '>':
							idx += 1
							break
						idx += 1
				else:
					sentence_tmp += x[idx]
					idx += 1
			sentences_out.append(sentence_tmp)
	return sentences_out 

def keep_sentence(raw_sentence):
	for x in  MAIN_TEXT_WORDS:
		idx = raw_sentence.find(x)
		if idx > -1:
#			print "YES"
#			print raw_sentence
#			print idx
			return idx
	return -1
#return txt.rsplit('|', 1)[-1]
