echo "Pakiety dla Ubuntu 20.04" &&
sudo add-apt-repository -y "deb http://security.ubuntu.com/ubuntu xenial-security main"
sudo apt -y update &&
sudo apt -y upgrade &&
sudo apt -y install build-essential checkinstall cmake pkg-config yasm &&
sudo apt -y install git gfortran &&
sudo apt -y install libjpeg8-dev libjasper-dev libpng-dev &&
sudo apt -y install libtiff5-dev && 
sudo apt -y install libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev &&
sudo apt -y install libxine2-dev libv4l-dev &&
sudo apt -y install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev &&
sudo apt -y install qt5-default libgtk2.0-dev libtbb-dev &&
sudo apt -y install libatlas-base-dev ant &&
sudo apt -y install libfaac-dev libmp3lame-dev libtheora-dev &&
sudo apt -y install libvorbis-dev libxvidcore-dev &&
sudo apt -y install libopencore-amrnb-dev libopencore-amrwb-dev &&
sudo apt -y install x264 v4l-utils libopenblas-dev&& 
sudo apt -y install libprotobuf-dev protobuf-compiler &&
sudo apt -y install libgoogle-glog-dev libgflags-dev &&
sudo apt -y install libblas-dev libavresample-dev &&
sudo apt -y install libgphoto2-dev libeigen3-dev libhdf5-dev doxygen &&
sudo apt -y install python3-dev python3-pip &&
sudo apt -y install libboost-all-dev &&
sudo apt -y install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libboost-all-dev libhdf5-serial-dev &&
sudo apt -y install libgflags-dev libgoogle-glog-dev liblmdb-dev protobuf-compiler &&
sudo apt -y install tesseract-ocr &&
sudo apt -y install libtesseract-dev &&
echo export PATH=/home/ubuntu/.local/bin:$PATH >> ~/.bashrc
pip3 install -U pip --user &&
pip3 install numpy --user &&
sudo apt -y  autoremove
