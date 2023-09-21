echo "Please provide the Mojeek API key"
read -s mojeek_api_key

kubectl delete secret recrawler-client-credentials
kubectl create secret generic recrawler-client-credentials \
  --from-literal=mojeek-api-key="${mojeek_api_key}"
