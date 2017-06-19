# small script for BASH to test which of the raw Wikisource files
# use specific templates, can be easily adjusted

for f in wikisource_raws/*.txt
do
	if grep -q "{{Re|" "${f}" || grep -q "{{Реплика|" "${f}"; then
		echo $f
	fi
done
