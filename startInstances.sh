start () {
    gcloud compute instances start $1
}

for i in ndm_master ndm_node-0 ndmm_node-1 ndm_node-2; do
    start $i &
done

wait

echo done
