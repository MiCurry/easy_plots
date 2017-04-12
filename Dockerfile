# TODO: Consider seperating web2py into another docker contianer

FROM centos:latest

# Tools
RUN yum install -y bzip2

# Header files for Basemap, geos, and wgrib2
RUN yum install -y gcc
RUN yum install -y gcc-c++
RUN yum install -y make
RUN yum install -y cronie

RUN yum install -y epel-release
RUN yum install -y python-pip
RUN yum install -y python-devel
RUN yum install -y python-matplotlib
RUN yum install -y libpng-devel

# TODO: Move web2py to a new container
# Install web2py
RUN pip install web2py

# Install Scipy Stack
RUN pip install scipy
RUN pip install numpy
RUN pip install matplotlib

# Basemap
WORKDIR /
RUN curl -OL http://sourceforge.net/projects/matplotlib/files/matplotlib-toolkits/basemap-1.0.7/basemap-1.0.7.tar.gz
RUN tar -xvzf basemap-1.0.7.tar.gz
RUN rm -r basemap-1.0.7.tar.gz

# INSTALL GEOS 3.5.0
RUN curl -O http://download.osgeo.org/geos/geos-3.6.1.tar.bz2
RUN tar xvjf geos-3.6.1.tar.bz2
RUN rm -r geos-3.6.1.tar.bz2
WORKDIR geos-3.6.1
RUN ./configure --prefix=/usr/local
RUN make
USER root
RUN make install

WORKDIR /

# Finish Basemap
RUN ldconfig
WORKDIR basemap-1.0.7
RUN python setup.py install

WORKDIR /home
ADD functional_tests.py functional_tests.py
ADD NAMS .

# TODO: Get wgrib2 to work
# Wgrib2
#RUN curl -O ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/wgrib2.tgz
#RUN tar -xzvf wgrib2.tgz
#WORKDIR # grib2
#ENV CC CC=gcc && FC=gfortran
#RUN make && make lib
