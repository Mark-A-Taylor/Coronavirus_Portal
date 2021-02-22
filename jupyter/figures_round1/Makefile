
# this will cause the 'make clean' to go into every subdirectory 
#	downside is it fails if any subdirectory does not have a Makefile
#SUBDIRS	:=	$(shell ls -d */)
#
# instead find target subdirectories for recursive 'make clean' that have Makefiles
# max depth is 1
# only applies to subdirectories with 'Makefile' present
FIND	=	/usr/bin/find
RM	=	/usr/bin/rm
MFILES	=	$(shell $(FIND) . -maxdepth 2 -type f -name Makefile)
SUBDIRS	=	$(filter-out ./,$(dir $(MFILES)))

default:

test:
	for dir in $(MFILES) ; do \
		echo $$dir ; \
	done

clean:
	$(RM) -rf __pycache__ out temp test .ipynb_checkpoints *.jpg *.JPG *.png *.PNG
	for dir in $(SUBDIRS) ; do \
		echo "cleaning directory: $$dir" ; \
		$(MAKE) -C $$dir $@ ; \
	done

