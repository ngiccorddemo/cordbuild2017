Steps to build from source (rather than using pre-built docker images):

Starting in the `cordbuild2017` directory, first clone the code from the public repo. The following command will check out the NGIC code at a specific commit and also pull the required DPDK submodule:

`git submodule update --init --recursive`

Change into the `ngic` directory:

`cd ngic`

Copy the Dockerfiles from demo repo to current (ngic) dir:

`cp ../dockerfiles/Docker* .`

For this demo, we are using replayed traffic, so we must apply a patch to enable static ARP tables.
**Note: If you are planning to run this with a traffic generator you supply, skip this step.**

`git apply ../dockerfiles/static_arp.patch`

Also for this demo, we are disabling the SDN Controller support.

`sed -i 's/CFLAGS/#CFLAGS/g' config/ng-core_cfg.mk`

Change back to the parent `cordbuild2017` dir. Now you can use the docker-compose to build the container images:

```shell
cd ..
docker-compose build
```

Once all of the images have built, go back and follow the instructions on the main readme starting at [Starting the Data Plane](https://github.com/ngiccorddemo/cordbuild2017#starting-the-data-plane)
