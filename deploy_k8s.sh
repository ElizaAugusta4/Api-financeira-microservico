#!/bin/bash
set -e

# Instala kubectl se não existir
if ! command -v kubectl &> /dev/null; then
  echo "Instalando kubectl..."
  curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
  chmod +x ./kubectl
  sudo mv ./kubectl /usr/local/bin/kubectl
fi

# Configura kubeconfig
if [ -z "$KUBE_CONFIG_DATA" ]; then
  echo "KUBE_CONFIG_DATA não definido!"
  exit 1
fi

echo "$KUBE_CONFIG_DATA" | base64 --decode > kubeconfig
export KUBECONFIG=$(pwd)/kubeconfig

# Aplica todos os manifests do diretório k8s
kubectl apply -f k8s/

# Valida rollout do deployment
kubectl rollout status deployment/api-financeira-microservico

# Aguarda alguns segundos para o serviço subir
sleep 10

# Faz um curl para o endpoint de health
APP_SERVICE=$(kubectl get svc api-financeira-microservico -o jsonpath='{.spec.clusterIP}')
APP_PORT=$(kubectl get svc api-financeira-microservico -o jsonpath='{.spec.ports[0].port}')

curl --fail http://$APP_SERVICE:$APP_PORT/health || {
  echo "Health check falhou!"
  exit 1
}

echo "Deploy validado com sucesso!"
