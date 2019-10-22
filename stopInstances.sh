stop () {
    gcloud compute instances stop $1
}

for i in master node-0 node-1 node-2; do
    stop $i &
done

wait

echo done
