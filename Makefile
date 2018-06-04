test:
	nosetests -sv --with-xunit --xunit-file=nosetests-ut.xml --exclude-dir=tests/functional/consumer/ --exclude-dir=tests/functional/provider/ tests/
