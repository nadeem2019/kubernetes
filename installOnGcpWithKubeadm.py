print('Python code to launch an Ubuntu 1804 LTS based Kubernetes cluster on GCP with kubeadm')
print('Prerequisite: Run these commands on Google cloud shell or on a Linux machine with gcloud installed')

import os

r = input('Region: ')
z = input('Zone: ')

setDefaults = '''
gcloud config set compute/region {}
gcloud config set compute/zone  {}
''' .format(r, z)

#m = int(input('No. of masters: '))
m = 1
masters = ''
for i in range(0, m):
    masters += ' master-{} ' .format(i)

n = int(input('No. of nodes: '))
nodes = ''
for i in range(0, n):
    nodes += ' node-{} '.format(i)

instances = masters + nodes

createMasters = ''
for i in masters.strip().split():
    createMasters += '''
    gcloud compute instances create {} --image-family ubuntu-1804-lts --image-project ubuntu-os-cloud --custom-cpu 2 --custom-memory 4
    ''' .format(i)

createNodes = ''
for i in nodes.strip().split():
    createNodes += '''
    gcloud compute instances create {} --image-family ubuntu-1804-lts --image-project ubuntu-os-cloud
    ''' .format(i)

createInstances = createMasters + createNodes

installDocker = '''
    sudo apt-get update
    sudo apt-get install apt-transport-https ca-certificates curl software-properties-common -y 
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu \ $(lsb_release -cs) \ stable" 
    sudo apt-get update && sudo apt-get install docker-ce=18.06.2~ce~3-0~ubuntu -y
    sudo sh -c "cat > /etc/docker/daemon.json" <<EOF
    {
    "exec-opts": ["native.cgroupdriver=systemd"],
    "log-driver": "json-file",
    "log-opts": {
    "max-size": "100m"
    },
    "storage-driver": "overlay2"
    }
    EOF
    sudo mkdir -p /etc/systemd/system/docker.service.d
    sudo systemctl daemon-reload
    sudo systemctl restart docker
    '''

addK8sRepos = '''
    apt-get update && apt-get install -y apt-transport-https curl
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
    cat > /etc/apt/sources.list.d/kubernetes.list" <<EOF
    deb https://apt.kubernetes.io/ kubernetes-xenial main
    EOF
    apt-get update
    '''    

installKubeadm = '''
    apt-get install -y kubeadm
    apt-mark hold kubeadm
    '''

installKubectl = '''
    apt-get install -y kubectl
    apt-mark hold kubectl
    '''

installKubelet = '''
    apt-get install -y kubelet
    apt-mark hold kubelet
'''

initClusterWithNetworking = '''
    kubeadm init --pod-network-cidr=192.168.0.0/16
    kubectl apply -f https://docs.projectcalico.org/v3.3/getting-started/kubernetes/installation/hosted/rbac-kdd.yaml
    kubectl apply -f https://docs.projectcalico.org/v3.3/getting-started/kubernetes/installation/hosted/kubernetes-datastore/calico-networking/1.7/calico.yaml
    '''

cmdLocal = setDefaults + createInstances
os.system(cmdLocal)

cmdRemote = installDocker + addK8sRepos
cmdRemoteMasters = installKubeadm + installKubectl + initClusterWithNetworking
cmdRemoteNodes = installKubeadm + installKubelet

#os.system('sudo su')

for i in masters.strip().splitlines():
    os.system('cat > cmdRemoteMaters.sh <<EOF\n{}\nEOF' .format())gcloud compute ssh {} --command {}'. format(i, cmdRemote + cmdRemoteMasters))

for i in nodes.strip().splitlines():
    os.system('echo {} | gcloud compute ssh {}'. format(cmdRemote + cmdRemoteNodes, i))
    os.system('gcloud compute ssh {} -- echo $USER; sudo usermod -aG docker $USER' .format(i)) 

#for i in instances.strip().splitlines():
 #   os.system('exit')
  #  os.system('gcloud compute ssh {} --command "echo $USER; sudo usermod -aG docker $USER"' .format(i)) 
