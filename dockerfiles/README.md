Steps to build from source (rather than using pre-built docker images):

Starting in the `cordbuild2017` directory, run the following command to clone the NGIC code at a specific commit and also pull the required DPDK submodule:

`git submodule update --init --recursive`

Copy the Dockerfiles from demo repo to ngic directory:

`cp dockerfiles/Docker* ngic/`

To move away from hardcoded IP address configs and test DNS apply the below patch

```shell
cp dockerfiles/use_dns.patch ngic/
git -C ngic apply use_dns.patch
```

Also for this demo, we are disabling the SDN Controller support.

`sed -i 's/CFLAGS/#CFLAGS/g' ngic/config/ng-core_cfg.mk`

Now you can use the docker-compose to build the container images:

`docker-compose build`

**Note:** If you are behind a proxy, append `--build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy`

Once all of the images have built, go back and follow the instructions on the main readme starting at [Starting the Data Plane](https://github.com/ngiccorddemo/cordbuild2017#starting-the-data-plane)
