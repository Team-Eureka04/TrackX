from browser_history import get_history

his = get_history()

for link in his.histories:
	print(link)
	print("----------------------")
