.PHONY: build run

build:
	docker build . -t pyvst

# To be run from the repo!
run:
	docker run -it --rm \
		--volume `pwd`:/workdir/pyvst/ \
		--user `id -u`:`id -g` \
		pyvst bash
