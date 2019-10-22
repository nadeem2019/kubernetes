start () {
    gcloud compute instances start $1
}

for i in master node-0 node-1 node-2; do
    start $i &
done

wait

echo done
