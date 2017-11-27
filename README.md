Prerequisites
=============

This demo requires a Linux box with at least 4GB of free RAM.

Install [docker](https://docs.docker.com/engine/installation/) (at least version 1.13 to run only, 17.06-ce to build images locally) and [docker-compose](https://github.com/docker/compose/releases).

After Docker is setup, clone the source code in this repo:

`git clone https://github.com/ngiccorddemo/cordbuild2017.git`

Then open 2 additional terminals and change directory to the demo folder in all of them:

`cd cordbuild2017`

__NOTE:__ Do this only if you are running this demo in __virtualbox__ directly or indirectly:

```shell
sed -i 's/latest/vbox/g' .env
```


Pull the images
===============

Use Docker-Compose to pull the images:

`docker-compose pull cp dp traffic`

(Alternatively, if you wish to build the Docker images yourself, see the [readme](dockerfiles/README.md) inside the dockerfiles folder.)


Starting the Data Plane
=======================

In terminal #1: Bring up DP

`docker-compose -p epc up dp`

Wait until you see messages about `Unable to resolve cp.cpdp.ngic.`, which means that it is waiting for the control plane.


Starting the Control Plane
==========================

In terminal #2: Bring up CP after DP is ready

`docker-compose -p epc up cp`

Wait until you see messages about `Unable to resolve mme.s11.ngic.`, which means that it is waiting for the traffic container.


Starting the Traffic 
====================

In terminal #3: Bring up Traffic container in daemon mode (-d) with:

`docker-compose -p epc up -d traffic`

Then enter the Traffic container with:

`docker exec -it epc_traffic_1 /bin/bash`

We need to rewrite the pre-recorded traffic to have the correct IP addresses. This will generate 3 modified pcap files.

`./rewrite_pcaps.py spgw.s11.ngic spgw.s1u.ngic spgw.sgi.ngic`


Now that the address fields are updated, it's time to start the traffic.
First, get the interface names by running the following commands:

```shell 
S11_IFACE=$(ip route get $(dig +short spgw.s11.ngic) | head -1 | awk '{print $3}')
S1U_IFACE=$(ip route get $(dig +short spgw.s1u.ngic) | head -1 | awk '{print $3}')
SGI_IFACE=$(ip route get $(dig +short spgw.sgi.ngic) | head -1 | awk '{print $3}')
```

Play the S11 (control plane) traffic to set up the flows

`tcpreplay --pps=200 -i $S11_IFACE tosend-s11.pcap`

Look at the Control Plane (Screen #2) and make sure that the packets appear. There should be 2000 packets sent/2000 received (from the 1000 CreateSession and 1000 ModifyBearer packets.)

Now start the S1U (Data Plane uplink) traffic

`tcpreplay --pps=2000 -i $S1U_IFACE tosend-s1u.pcap`

Check the Data Plane  (Screen #1).  You should see ~6500 packets received on the S1U and ~6500 packets transmitted on the SGi.

Now start the SGi (Data Plane downlink) traffic

`tcpreplay --pps=2000 -i $SGI_IFACE tosend-sgi.pcap`

Check the Data Plane  (Screen #1).  You should see ~6500 packets received on the SGi and ~6500 packets transmitted on the S1U.


Tear Down
=========
From the Traffic terminal, type:

`exit` 

and then type:

`docker-compose -p epc down`
