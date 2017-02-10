import requests
import pprint
import json
import actor
import page_parser as pp

API_URL = 'http://en.wikipedia.org/w/api.php'
HEADERS = {
    'User-Agent': "Latinos in Comedy Research Project (dmb2238@columbia.edu)"
}

class WikiPages(object):

	def __init__(self, actor_titles):
		self.actors = {}
		title_string = ""
		for a in actor_titles:
			title_string = title_string + a.replace(" ", "_") + "|"
			self.actors[a] = actor.Actor(a)
		self.titles = title_string
	
	def get_all_info(self):
		self.get_plain_text()
		y = self.get_categories()
		y = self.get_birthplace()
		return y
			
	def get_birthplace(self):
		for elem in self.get_infobox():
			for page_id, content in elem['pages'].iteritems():
				if 'revisions' in content:
					bp = pp.get_birthplace(content['revisions'][0]['*'])
					if bp != "":
						self.actors[str(content['title'])].birthplace = bp
		return self.actors

	def get_plain_text(self):
		dump = self._wiki_query({ 'prop': 'extracts', 'titles': self.titles})
		for elem in dump:
			for page_id, content in elem['pages'].iteritems():
				if 'extract' in content:
					self.actors[str((content['title']))].self_info += pp.get_sentences(content['extract'])
		#sentences = text.split('.')
		#for x in sentences:
		#	if pp.keep_sentence(x) > -1:
		#		self.actors
		return True
		
	def get_infobox(self):
		info = self._wiki_query({
			'prop': 'revisions',
			'rvprop': 'content',
			'rvsection': 0,
			'titles': self.titles
		})
		return info

	def get_categories(self):
		dump = self._wiki_query({ 'prop': 'categories', 'titles': self.titles})
		for elem in dump:
			for page_id, content in elem['pages'].iteritems():
				if 'categories' in content:
					actor_tags = self.actors[str(content['title'])].tags
					for x in content['categories']:
						c = x['title'].split(':')[1].lower()
						if pp.keep_category(c):
							actor_tags.append(c)
					self.actors[str(content['title'])].tags = actor_tags
		return self.actors

	def get_full_page(self):
		text = self._wiki_query({ 
			'prop': 'revisions', 
			'rvprop':'content', 
			'titles': self.titles
		})
		return true
	
	def _wiki_query(self, params):
		params['format'] = 'json'
		params['action'] = 'query'
 	       
 	       	last_continue = {'continue': ''}
 	       	p = params.copy()
 	       	out = []
 	       	while True:
			p.update(last_continue)
 	       		result = requests.get(API_URL, params=p, headers = HEADERS).json()
 	       		if 'error' in result:
 	        	   		raise Error(result['error'])
        		if 'warnings' in result:
            			print(result['warnings'])
        		if 'query' in result:
            			out.append(result['query'])
        		if 'continue' not in result:
            			break
       			last_continue = result['continue']
		return out
