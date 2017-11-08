To build from source (Rather than prebuilt docker images):

First clone the code from the public repo:

`git clone --recursive https://gerrit.opencord.org/ngic && cd ngic`

Then, check out this specific commit for this demo:

`git checkout a9e05`

Copy the Dockerfiles from this repo to your newly cloned NGIC code:

`cp ../cordbuild2017/dockerfiles/Docker* .`

For this demo, we are using replayed traffic, so we must apply a patch to enable static ARP tables.

```shell
cp ../cordbuild2017/dockerfiles/static_arp.patch .
git apply static_arp.patch
```

Also for this demo, we are disabling the SDN Controller support.

`sed -i 's/CFLAGS/#CFLAGS/g'  config/ng-core_cfg.mk`


Now you can use the Dockerfiles to build the container images:

```shell
docker build -t ngiccorddemo/ngic-builder -f Dockerfile-builder .
docker build -t ngiccorddemo/ngic-cp -f Dockerfile-cp .
docker build -t ngiccorddemo/ngic-dp -f Dockerfile-dp .
docker build -t ngiccorddemo/ngic-traffic -f Dockerfile-traffic .
```

Once all of the images have built, go back and follow the instructions on the main readme starting at [Starting the Data Plane](https://github.com/ngiccorddemo/cordbuild2017#starting-the-data-plane)

