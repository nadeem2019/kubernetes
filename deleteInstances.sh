delete () {
    gcloud -q compute instances delete $1
}

for i in master node-0 node-1 node-2; do
    delete $i &
done

wait

echo done
