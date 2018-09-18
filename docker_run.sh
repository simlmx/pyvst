# To be run from the repo!
docker run -it --rm \
    --volume `pwd`:/workdir/pyvst/ \
    --user `id -u`:`id -g` \
    pyvst bash
