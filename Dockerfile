FROM debian:jessie-slim
MAINTAINER Daniele Dalla Torre <dallatorre.daniele@gmail.com>
# install necessary packages
RUN 	apt-get -y update \
	&& apt-get install --no-install-recommends -y \
	ca-certificates \
	make \
	cmake \
	gcc \
	g++ \
	git \
	libgomp1 \
	&& mkdir data \
	&& git clone https://github.com/geoframecomponents/Stormwater-Management-Model.git \
	&& cd Stormwater-Management-Model/src/ \
	&& make \
	&& cp ./swmm5 /
# launch the engine of swmm5	
ENTRYPOINT ["/bin/bash", "-c", "./swmm5 data/$0.inp data/$0.rpt data/$0.out"]
# purge not needed stuff
RUN	apt-get -y remove --purge \
	ca-certificates \
	make \
	cmake \
	gcc \
	g++ \
	git \
	&& apt-get -y autoremove --purge \
	&& cd / \
	&& rm -r Stormwater-Management-Model
