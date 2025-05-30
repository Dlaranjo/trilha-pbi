# Kubernetes: Uma Introdução Prática

## O que é Kubernetes?

Kubernetes (K8s) é um sistema de orquestração de containers que automatiza o deploy, scaling e gerenciamento de aplicações containerizadas.

## Conceitos Fundamentais

### 1. Pods
- **O que é?** A menor unidade de deploy no Kubernetes
- **Analogia:** Um Pod é como um "apartamento" onde containers "moram" juntos
- **Características:**
  - Compartilham recursos (rede, armazenamento)
  - São efêmeros (podem ser recriados)
  - São a unidade básica de deploy

### 2. Deployments
- **O que é?** Um gerenciador de Pods
- **Analogia:** Um "construtor" que mantém múltiplas cópias do mesmo "apartamento"
- **Funcionalidades:**
  - Mantém o número desejado de réplicas
  - Realiza atualizações sem downtime
  - Permite rollback de versões

### 3. Services
- **O que é?** Um ponto de acesso estável para os Pods
- **Analogia:** Um "porteiro" que direciona o tráfego para os "apartamentos" corretos
- **Tipos:**
  - ClusterIP (interno)
  - NodePort (acesso externo via porta)
  - LoadBalancer (balanceamento de carga)

## Demonstração Prática

### 1. Criando um Pod
```bash
kubectl apply -f manifests/pod.yaml
```

### 2. Criando um Deployment
```bash
kubectl apply -f manifests/deployment.yaml
```

### 3. Criando um Service
```bash
kubectl apply -f manifests/service.yaml
```

## Comandos Úteis

### Monitoramento
```bash
# Ver Pods
kubectl get pods -n k8s-demo

# Ver Deployments
kubectl get deployments -n k8s-demo

# Ver Services
kubectl get services -n k8s-demo
```

### Escalando Aplicação
```bash
# Aumentar número de réplicas
kubectl scale deployment app-simples -n k8s-demo --replicas=5
```

### Atualizando Aplicação
```bash
# Atualizar imagem
kubectl set image deployment/app-simples demo-container=python:3.9-slim -n k8s-demo
```

## Conceitos Avançados

### 1. ConfigMaps e Secrets
- Gerenciamento de configurações
- Armazenamento seguro de dados sensíveis

### 2. Volumes
- Persistência de dados
- Compartilhamento entre containers

### 3. Namespaces
- Isolamento de recursos
- Organização do cluster

### 4. Health Checks
- Liveness Probe (verifica se a aplicação está viva)
- Readiness Probe (verifica se a aplicação está pronta)

## Boas Práticas

1. **Sempre use Deployments**
   - Evite criar Pods diretamente
   - Aproveite o gerenciamento automático

2. **Defina limites de recursos**
   - Requests: recursos garantidos
   - Limits: recursos máximos

3. **Implemente Health Checks**
   - Monitore a saúde da aplicação
   - Permita recuperação automática

4. **Use Labels e Selectors**
   - Organize recursos
   - Facilite a descoberta de serviços

## Exercícios Práticos

1. **Escalando a Aplicação**
   ```bash
   kubectl scale deployment app-simples -n k8s-demo --replicas=3
   ```

2. **Atualizando a Aplicação**
   ```bash
   kubectl set image deployment/app-simples demo-container=python:3.9-slim -n k8s-demo
   ```

3. **Verificando Logs**
   ```bash
   kubectl logs <pod-name> -n k8s-demo
   ```

4. **Acessando a Aplicação**
   ```bash
   kubectl port-forward service/app-simples-service 8080:80 -n k8s-demo
   ``` 