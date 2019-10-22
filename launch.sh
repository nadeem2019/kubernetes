gcloud config set compute/region us-central1
gcloud config set compute/zone  us-central1-a

gcloud compute instances create master --image-family ubuntu-1804-lts --image-project ubuntu-os-cloud --custom-cpu 2 --custom-memory 4

createNodes() {
    gcloud compute instances create node-$1 --image-family ubuntu-1804-lts --image-project ubuntu-os-cloud
}

for i in {0..2}; do
    createNodes $i &
done

wait

allInstances() {
    cat installDocker.sh | gcloud compute ssh $1
    cat addK8sRepos.sh | gcloud compute ssh $1
    cat installKubeadm.sh | gcloud compute ssh $1
}

for i in master node-0 node-1 node-2; do
    allInstances $i &
done

wait

nodes() {
    cat installKubelet.sh | gcloud compute ssh node-$1
}

for i in {0..2}; do
    nodes $i &
done

wait

cat installKubectl.sh | gcloud compute ssh master
cat initCluster.sh | gcloud compute ssh master > initOutput.sh
cat setupKubeconfig.sh | gcloud compute ssh master
cat podNetworking.sh | gcloud compute ssh master

echo 'sudo su' > joinNodes.sh
cat initOutput.sh | tail -2 >> joinNodes.sh

join() {
    cat joinNodes.sh | gcloud compute ssh node-$1
}

for i in {0..2}; do
    join $i
done

echo '````````````````````````````````````````````````````'
echo 'To access the master: gcloud compute ssh master'
echo 'Your cluster is ready, login to the master and enjoy'
