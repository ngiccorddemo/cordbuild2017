Steps to build from source (rather than using pre-built docker images):

Starting in the `cordbuild2017` directory, run the following command to clone the NGIC code at a specific commit and also pull the required DPDK submodule:

`git submodule update --init --recursive`

Copy the Dockerfiles from demo repo to ngic directory:

`cp dockerfiles/Docker* ngic/`

For this demo, we are using replayed traffic, so we must apply a patch to enable static ARP tables.  
**Note: If you are planning to run this with a traffic generator you supply, skip this step.**

```shell
cp dockerfiles/static_arp.patch ngic/
git -C ngic apply static_arp.patch
```

Also for this demo, we are disabling the SDN Controller support.

`sed -i 's/CFLAGS/#CFLAGS/g' ngic/config/ng-core_cfg.mk`

Now you can use the docker-compose to build the container images:

`docker-compose build`

Once all of the images have built, go back and follow the instructions on the main readme starting at [Starting the Data Plane](https://github.com/ngiccorddemo/cordbuild2017#starting-the-data-plane)
