#!/bin/sh
# Helps in renaming hrml filenames with timestamp only into the format that shows number of changes
# Copy the file into the data_* directories and run it.
# You can execute the printed 'mv' commands one by one or once for all if it seems ok.

for ff in `ls *.html | grep -v full`; do
	all=`grep -c item-header $ff`
	new=`grep -c "item-header new" $ff`
	chg=`grep -c "item-header changed" $ff`
	del=`grep -c "item-header deleted" $ff`
	basnam="${ff%.html}"
	echo "mv ${basnam}.html ${basnam}_a${all}_n${new}_c${chg}_d${del}.html"
	echo "mv ${basnam}.full.html ${basnam}_a${all}_n${new}_c${chg}_d${del}.full.html"
done

