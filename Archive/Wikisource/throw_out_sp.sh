# throw_out_sp.sh
# postprocessing for wikisource files converted to TEI
# meant for ira's conversion scripts
# purpose: throwing out unwanted </sp> tags
# removes all </sp> not preceded by an opening <sp …>
# expects (one) filename as argument
# will leave original file untouched
# output written to new file "*.new.*"

# filename as parameter needed
if [ -z "$*" ]; then echo "Filename missing …"; exit; fi

READFILENAME=$1
printf "Processing $READFILENAME …\n"

WRITEFILENAME="${READFILENAME%.*}".new."${READFILENAME##*.}"
printf "Writing to $WRITEFILENAME …\n"

# read file into array
mapfile lines < "$READFILENAME"

# initialise vars
flag=0
counter=0

# initialise output file
if [ -f "$WRITEFILENAME" ] ; then
    rm "$WRITEFILENAME"
fi

# check all lines for unwanted </sp>
for i in "${lines[@]}"
do
    if [[ "$i" =~ ^"<sp " ]]
    	then
    	flag=1
	fi

    if [[ "$i" =~ ^"</sp" ]] && [ $flag -eq 1 ]
    	then
    	printf "$i" >> "$WRITEFILENAME"
    	flag=0
    elif [[ ! "$i" =~ ^"</sp" ]]
    	then
        printf "$i" >> "$WRITEFILENAME"
    else
    	(( counter += 1 ))
    fi
done

echo "RESULT: $counter unwanted </sp> thrown out!"
