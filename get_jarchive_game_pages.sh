python generate_game_page_urls.py > urls.lst

wget -i urls.lst --user-agent="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3" -w 0.1 -P pages -o logs/wget_log.log

find pages | xargs grep -l "ERROR: No game" | awk '{print "rm "$1}' > remove_ivalid.sh
chmod +x remove_ivalid.sh
./remove_ivalid.sh

parse.py > jeopardy_data.tsv

#removed $ signs using openoffice in col#6

TAB=`echo -e "\t"`

sort -k1,1 -k2,2 -k3,3  -k4,4 -k6n,6  jeopardy_data.tsv -t"$TAB"> jeopardy_data_sorted.tsv
