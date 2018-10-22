# To be run from the repo!
# Forwarding the 8888 port for jupyter
docker run -it --rm \
    --volume `pwd`:/workdir/pyvst/ \
    --user `id -u`:`id -g` \
    -p 8888:8888 \
    pyvst bash
