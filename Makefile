compile:
	export PYTHONPATH=`pwd`
	/home/bplank/epd-7.3-2-rh5-x86_64/bin/python setup.py build_ext --inplace

clean:
	/home/bplank/epd-7.3-2-rh5-x86_64/bin/python setup.py clean