echo "[1- Updating and upgrading ......]" &&
sudo apt -y update &&
sudo apt upgrade &&
sudo apt dist-upgrade &&
echo -e "\n[2- Cleaning Up ......]" &&
sudo apt -f install &&
sudo apt -y autoremove &&
sudo apt -y autoclean &&
sudo apt -y clean && 
echo -e "\n[3 - Done!!!!]"
