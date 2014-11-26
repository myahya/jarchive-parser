jarchive-parser
===============

This package contains scripts to download Jeopardy! episodes from J! Archive, and parse them into a structured format for further analysis.

## Use
Simply run the script `get_jarchive_game_pages.sh`.

This will do the following:
1. Generate a list of the URLs to download.
2. Download the HTML pages for all the episodes offline.
3. Parse each HTML file to produce a structured output.


## Output
The output has the following format (columns are tab-separated):
* Show#
* Episode date
* Round name
* Clue
* Monetary value
* Correct response
* A comma separated list, where each entry has the form: Contestant(right/wrong)
* Triple Stumper?

## Contributors:
Dominic Seyler
Mohamed Yahya

