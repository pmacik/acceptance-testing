#!/bin/bash -e

function create_cluster(){
   kind create cluster --name $2 --image kindest/node:v$1
   wait_till_cluster_up $2
}

function delete_cluster() {
   kind delete cluster --name $2 
}

function get_cluster_auth() {
   echo "kubectl config set-context kind-$2"
}

function wait_till_cluster_up() {
   kubectl config set-context kind-$1 
   export STATUS=""
   while [ "${STATUS}" != "Ready" ]; do
      export STATUS=$(kubectl get nodes | tail -n1 | awk '{print $2}')
      sleep 10
   done
}
