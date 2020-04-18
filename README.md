sudo apt-get install python3.6  
sudo apt-get install python3-pip  
sudo python3.6 -m pip install flask  
sudo python3.6 -m pip install flask_api  
sudo python3.6 -m pip install mysql-connector-python  


upload folders to ec2:  
scp -i E0383718Key.pem -r app_server ubuntu@[public-ip]:~/app_server  

(kill the service running on port 80 if there is any --> sudo lsof -i:80)  
sduo python3 ~/app_server/run.py  