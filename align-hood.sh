w=cow;
g=hood;

pocketsphinx_continuous \
	-infile $w.wav \
	-jsgf $g.jsgf \
	-dict phonemes.dict \
	-backtrace yes \
	-fsgusefiller no \
	-bestpath no \
	2>&1 | tee $g-align.txt ;
