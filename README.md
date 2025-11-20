# gerrit-selelium


```
sudo apt update
sudo apt install -y wget unzip
CHROME_DRIVER_VERSION=$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
sudo apt install libnss3
https://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.198-1_amd64.deb
sudo dpkg -i google-chrome-stable_114.0.5735.198-1_amd64.deb
sudo apt --fix-broken install
```