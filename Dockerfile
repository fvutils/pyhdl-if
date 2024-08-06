# Use the official Python image as the base
FROM python

# Set the working directory inside the container
WORKDIR /work/

# Clone the Verilator repository
RUN git clone https://github.com/verilator/verilator.git

# Change the working directory to the Verilator repository
WORKDIR /work/

RUN apt-get update && \
	apt-get install -y help2man flex bison ccache && \
	apt-get install -y libgoogle-perftools-dev numactl perl-doc && \
	cd verilator && \
	git checkout 37a400209809d389eb8eae0a6b6bee47fd4008c7 && \
	# Build and install Verilator
	autoconf && ./configure && make && make install

# Add Verilator to the environment variables
ENV PATH="${PATH}:/work/verilator/bin"
