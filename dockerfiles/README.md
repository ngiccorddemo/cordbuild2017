Steps to build from source (rather than using pre-built docker images)-

Starting in `cordbuild2017` dir, first clone the code from the public repo:

`git clone --recursive https://gerrit.opencord.org/ngic && cd ngic`

Then, check out this specific commit for this demo:

`git checkout a9e05`

Copy the Dockerfiles from demo repo to current (ngic) dir:

`cp ../dockerfiles/Docker* .`

For this demo, we are using replayed traffic, so we must apply a patch to enable static ARP tables.

`git apply ../dockerfiles/static_arp.patch`

Also for this demo, we are disabling the SDN Controller support.

`sed -i 's/CFLAGS/#CFLAGS/g' config/ng-core_cfg.mk`

Change back to the parent `cordbuild2017` dir. Now you can use the docker-compose to build the container images:

```shell
cd ..
docker-compose build
```

Once all of the images have built, go back and follow the instructions on the main readme starting at [Starting the Data Plane](https://github.com/ngiccorddemo/cordbuild2017#starting-the-data-plane)

