Prerequisites
=============

This demo requires a Linux box with at least 4GB of free RAM.

Install `docker` (at least version 1.13) and `docker-compose`.  Docker Compose will automatically pull the docker images, or you can pre-pull them using:


```shell 
docker pull ngiccorddemo/ngic-cp
docker pull ngiccorddemo/ngic-dp
docker pull ngiccorddemo/ngic-traffic
```

(Alternatively, if you wish to build the Docker images yourself, see the [readme](dockerfiles/README.md) inside the dockerfiles folder.)


After Docker is setup, clone the source code in this repo:

`git clone https://github.com/ngiccorddemo/cordbuild2017.git`

Then open 3 terminals and change directory to the demo folder.


Starting the Data Plane
=======================

In terminal #1: Bring up DP

`docker-compose -p epc up dp`


Wait for DP to print stats

You will shortly see some additional stats printing as well.


# Starting the Control Plane
In terminal #2: Bring up CP after DP is ready

`docker-compose -p epc up cp`

You will see a large table of stats printing periodically


Starting the traffic 
=======================

In terminal #3: Bring up traffic container in daemon mode (-d)

`docker-compose -p epc up -d traffic`

Enter the container

`docker exec -it epc_traffic_1 /bin/bash`

It's time to start the traffic.

First, get the interface names by running the following commands:

```shell 
S11_IFACE=$( netstat -ie | grep -B1 10.1.10 | head -n1 | awk '{print $1}' | tr --d : )
S1U_IFACE=$( netstat -ie | grep -B1 11.1.1  | head -n1 | awk '{print $1}' | tr --d : )
SGI_IFACE=$( netstat -ie | grep -B1 13.1.1  | head -n1 | awk '{print $1}' | tr --d : )
```

Play the S11 (control plane) traffic to set up the flows

`tcpreplay  --pps=200 -i $S11_IFACE s11.pcap`

Look at the Control Plane (Screen #2) and make sure that the packets
appear. There should be 2000 packets sent/2000 received (from
the 1000 CreateSession and 1000 ModifyBearer packets.)

Now start the S1U (Data Plane uplink) traffic

`tcpreplay  -i $S1U_IFACE s1u.pcap`

Check the Data Plane  (Screen #1).  You should see ~6500 packets received on the S1U and ~6500 packets transmitted on the SGi.

Now start the SGi (Data Plane downlink) traffic

`tcpreplay  -i $SGI_IFACE sgi.pcap`

Check the Data Plane  (Screen #1).  You should see ~6500 packets received on the SGi and ~6500 packets transmitted on the S1U.


TEAR DOWN
=======================
From the traffic terminal, type `exit` and then type:

`docker-compose -p epc down`
