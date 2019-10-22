delete () {
    gcloud -q compute instances delete $1
}

for i in ndm_master ndm_node-0 ndm_node-1 ndm_node-2; do
    delete $i &
done

wait

echo done
