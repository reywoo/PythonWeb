import boto.ec2
import time
import os
import subprocess
import sys



DRY=False
#sec_group="csc326_group_g326-2-010"
sec_group="testinggroup"
f=open("keyfile.txt","r")
gen=(line for line in f)
line1=gen.next()
keyID=line1.split("=")[1]
keyID=str(keyID.replace("\n",""))
line2=gen.next()
access_key=line2.split("=")[1]
access_key=str(access_key.replace("\n",""))


#establish a connection
conn=boto.ec2.connection.EC2Connection(aws_access_key_id=str(keyID), aws_secret_access_key=str(access_key))
#conn=boto.ec2.connection.EC2Connection()

#create Key-Pair
MyKey=conn.create_key_pair(key_name="Key",dry_run=DRY)
time.sleep(10)
#save Key-Pair
mydirectory=os.getcwd()
MyKey.save(mydirectory)
print "creating key pair..."


#create a security group
MyGroup=conn.create_security_group(name=sec_group, description="This is a new group", dry_run=DRY)
time.sleep(3)
#authorize security group
if not conn.authorize_security_group(group_name=sec_group, src_security_group_name=sec_group, ip_protocol="icmp", from_port=-1, to_port=-1, cidr_ip="0.0.0.0/0", dry_run=DRY):
	print("Unable to authorize ping access!")
else:
	print("Ping authorized!")

if not conn.authorize_security_group(group_name=sec_group, src_security_group_name=sec_group, ip_protocol="TCP", from_port=22, to_port=22, cidr_ip="0.0.0.0/0", dry_run=DRY):
	print("Unable to authorize SSH access!")
else:
	print("SSH authorized!")

if not conn.authorize_security_group(group_name=sec_group, src_security_group_name=sec_group, ip_protocol="TCP", from_port=80, to_port=80, cidr_ip="0.0.0.0/0", dry_run=DRY):
	print("Unable to authorize HTTP access!")
else:
	print("HTTP authorized!")



#Run instance
#The instance will be running on 64bit EBS service
im_ID="ami-8caa1ce4"
security_group_list=[sec_group]
Instance_List=conn.run_instances(image_id=im_ID, key_name="Key", security_groups=security_group_list, instance_type="t1.micro",dry_run=DRY)

print "Please wait for at least 3 minutes, AWS is starting your instance..."
time.sleep(15)



reservations=conn.get_all_instances()
time.sleep(5)
#get address of new created instances public ip address
public_ip = str(reservations[0].instances[0].ip_address)
public_DNS = str(reservations[0].instances[0].public_dns_name)
instance_id = str(reservations[0].instances[0])
print "Public IP of the instance is ",public_ip
print "Public DNS of the instance is ",public_DNS
print "Instance ID is ",instance_id
f=open("temp.txt","w")
f.write(public_ip+"\n")
f.write(public_DNS+"\n")
f.write(instance_id+"\n")


proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
print "program output:", out

#check if db exists

from os.path import exists
cwd=os.getcwd()
if not exists(cwd+"/Frontend/dbFile.db"):
    os.chdir(cwd+"/Backend")
    cmd="python crawler.py"
    os.system(cmd)
    os.chdir(cwd)
#-----




install="sudo apt-get update;sudo apt-get install python-httplib2;sudo apt-get install python-setuptools -y;sudo easy_install --upgrade google-api-python-client;sudo apt-get install python-pip -y;sudo pip install beaker"


cmd = "ssh -i Key.pem ubuntu@" + public_ip + " -o StrictHostKeyChecking=no "+ "\'"+install+"\'"
os.system(cmd)

print "Please wait, configuring your server..."
time.sleep(80)


cmd = "sed -i.bak s/localhost:8080/"+public_DNS+"/g Frontend/Final_Front.py"
os.system(cmd)

cmd = "tar -zcvf Frontend.tar.gz Frontend"
os.system(cmd)

cmd = "tar -zcvf Backend.tar.gz Backend"
os.system(cmd)


#upload Frontend.tar.gz
cmd = "scp -i Key.pem "+ out[:len(out)-1] +"/Frontend.tar.gz ubuntu@"+public_ip+":~/"
os.system(cmd)

#upload Backend.tar.gz
cmd = "scp -i Key.pem "+ out[:len(out)-1] +"/Backend.tar.gz ubuntu@"+public_ip+":~/"
os.system(cmd)

unzip = 'tar -xzvf Frontend.tar.gz; tar -xzvf Backend.tar.gz; rm Frontend.tar.gz; rm Backend.tar.gz; cd Frontend; sudo python Final_Front.py'

cmd = "ssh -i Key.pem ubuntu@" + public_ip + " -o StrictHostKeyChecking=no "+ "\'"+unzip+"\'"

os.system(cmd)








