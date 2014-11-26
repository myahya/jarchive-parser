initial_page_id=1
last_page_id=5000


for i in range(initial_page_id, last_page_id):
	print "http://www.j-archive.com/showgame.php?game_id="+str(i)
	i+=1
