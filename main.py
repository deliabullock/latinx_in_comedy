import wikipedia_utils as wiki
import pprint

def transform_names(raw_names):
	split_names = raw_names.split(", ")
	for x in range(len(split_names)):
		split_names[x] = split_names[x].strip()#.replace(" ", "_")
	return split_names

def main():
	actor_names = "Stephanie Beatriz, Elizabeth Rodriguez, Dascha Polanco"
	pages = wiki.WikiPages(transform_names(actor_names))
	actors = pages.get_all_info()
	for actor in actors:
		print actors[actor].birthplace
		for x in actors[actor].tags:
			print x		

if __name__ == '__main__':
      main()
