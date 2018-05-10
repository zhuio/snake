sudo add-apt-repository ppa:webupd8team/java -y && apt-get update
sudo apt-get install -y gcc g++ perl python automake make \
                                       wget git curl libdb-dev \
                                       zlib1g-dev bzip2 libncurses5-dev \
                                       texlive-latex-base \
                                       default-jre \
                                       python-pip python-dev \
                                       gfortran \
                                       build-essential libghc-zlib-dev  libbz2-dev liblzma-dev libpcre3-dev libxml2-dev \
                                       libblas-dev gfortran git unzip ftp libzmq3-dev nano ftp fort77 libreadline-dev \
                                       libcurl4-openssl-dev libx11-dev libxt-dev \
                                       x11-common libcairo2-dev   libjpeg8-dev pkg-config libtbb-dev \
                                       sqlite lighttpd libgd-tools mysql-server mysql-client libmysqlclient-dev htop \
                                       vim screen openssh-server tree libgtk2.0-dev \
                                       libboost-iostreams-dev install zlib1g-dev libmysql++-dev libgsl-dev libsqlite3-dev \
                                       libboost-graph-dev libsuitesparse-dev liblpsolve55-dev bamtools





sudo apt-get install oracle-java8-installer

# conda install gcc_linux-64 gxx_linux-64 gfortran_linux-64
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/menpo/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
