FILES	=	\
			Makefile \
			app.py \
			main.py \
			calcs.py \
			assets\downLeftArrow.JPG \
			assets\downRightArrow.JPG \
			assets\triarrow.png \
			pages\clustering.py \
			pages\timeseries.py \
			pages\pca.py \
			pages\methods.py \
			pages\datatable.py \
			pages\timeseries.py

clean:
	\rm -rf __pycac*
	\rm -rf pages/__pycac*

cleaner: clean
	\rm -rf cachestore/*

cleanest: cleaner
	\rm -rf backup/*
	\rm -rf backup2/*

backup: $(FILES)
	\rm -rf backup/*
	\cp -r *.py Makefile pages backup/.
	
backup2: $(FILES)
	\rm -rf backup2/*
	\cp -r *.py Makefile pages backup2/.
