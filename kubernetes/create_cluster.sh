#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]
then
    echo "Usage: create_cluster REGISTRY CLUSTER"
    exit 1
fi

REGISTRY=$1
CLUSTER=$2

echo "registry: $REGISTRY"
echo "cluster: $CLUSTER"

az group create --name cluster --location westeurope
az aks create --resource-group cluster --name cluster --node-count 1 --node-vm-size Standard_D8s_v4 --generate-ssh-keys
az aks update --resource-group cluster --name cluster --attach-acr $REGISTRY 
az aks get-credentials --resource-group cluster --name cluster --overwrite-existing

az network public-ip create \
  --resource-group mc_cluster_cluster_westeurope \
  --name ip \
  --sku Standard \
  --allocation-method static \
  --query publicIp.ipAddress -o tsv

STATIC_IP=$(az network public-ip show --name ip \
  --resource-group mc_cluster_cluster_westeurope \
  -o tsv --query ipAddress)
echo "static ip: $STATIC_IP"

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-basic --create-namespace \
  --set controller.service.loadBalancerIP=$STATIC_IP \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-dns-label-name"=$CLUSTER \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-health-probe-request-path"=/healthz

export KUBEVIRT_VERSION=v0.59.0
echo "kubevirt version: $KUBEVIRT_VERSION"

kubectl create namespace kubevirt
kubectl apply -f https://github.com/kubevirt/kubevirt/releases/download/$KUBEVIRT_VERSION/kubevirt-operator.yaml
kubectl apply -f https://github.com/kubevirt/kubevirt/releases/download/$KUBEVIRT_VERSION/kubevirt-cr.yaml
