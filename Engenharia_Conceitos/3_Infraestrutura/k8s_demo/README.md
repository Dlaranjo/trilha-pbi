# Demonstração Prática de Kubernetes 🚀

Este projeto demonstra os conceitos básicos do Kubernetes de forma prática e interativa. Vamos aprender Kubernetes construindo uma aplicação real!

## 🎯 Objetivos de Aprendizado

1. Entender os componentes básicos do Kubernetes
2. Criar e gerenciar containers em um cluster
3. Implementar alta disponibilidade
4. Gerenciar configurações e atualizações

## 📁 Estrutura do Projeto

```
k8s_demo/
├── app/                    # Nossa aplicação Python
│   ├── app.py             # Aplicação Flask
│   ├── Dockerfile         # Instruções para criar a imagem
│   └── requirements.txt   # Dependências Python
├── manifests/             # Arquivos de configuração do Kubernetes
│   ├── deployment.yaml    # Configuração do Deployment
│   └── service.yaml       # Configuração do Service
└── README.md             # Este arquivo
```

## 🚀 Como Executar

### 1. Pré-requisitos
- Docker Desktop com Kubernetes habilitado
- kubectl instalado
- Python 3.9+

### 2. Construir a Imagem Docker
```bash
cd app
docker build -t k8s-demo-app:1.0 .
```

### 3. Aplicar as Configurações do Kubernetes
```bash
# Criar namespace
kubectl create namespace k8s-demo

# Aplicar configurações
kubectl apply -f manifests/deployment.yaml
kubectl apply -f manifests/service.yaml
```

### 4. Verificar o Status
```bash
# Ver pods
kubectl get pods -n k8s-demo

# Ver serviços
kubectl get svc -n k8s-demo
```

### 5. Acessar a Aplicação
```bash
# Criar port-forward
kubectl port-forward svc/demo-service 8080:80 -n k8s-demo
```

Acesse no navegador: http://localhost:8080

## 📚 Conceitos Demonstrados

### 1. Pods
- Unidade básica de deploy
- Container isolado
- Compartilhamento de recursos

### 2. Deployments
- Gerenciamento de réplicas
- Atualizações sem downtime
- Rollback de versões

### 3. Services
- Exposição de aplicações
- Balanceamento de carga
- Descoberta de serviços

## 🎮 Comandos Úteis para Experimentar

```bash
# Escalar a aplicação
kubectl scale deployment demo-deployment --replicas=5 -n k8s-demo

# Ver logs de um pod
kubectl logs <nome-do-pod> -n k8s-demo

# Ver detalhes de um pod
kubectl describe pod <nome-do-pod> -n k8s-demo

# Atualizar a aplicação
kubectl set image deployment/demo-deployment demo-container=k8s-demo-app:2.0 -n k8s-demo
```

## 🔍 O que Aprendemos?

1. **Pods**: Como containers são executados no Kubernetes
2. **Deployments**: Como manter aplicações disponíveis
3. **Services**: Como expor aplicações para acesso
4. **Namespaces**: Como organizar recursos
5. **Health Checks**: Como monitorar a saúde da aplicação

## 🎯 Exercícios Sugeridos

1. Aumente o número de réplicas para 5
2. Atualize a versão da aplicação
3. Verifique os logs dos pods
4. Teste o endpoint de saúde
5. Faça um rollback da atualização

## 🛠️ Troubleshooting

Se encontrar problemas:

1. Verifique os logs dos pods:
```bash
kubectl logs <nome-do-pod> -n k8s-demo
```

2. Verifique o status dos pods:
```bash
kubectl get pods -n k8s-demo
```

3. Verifique os detalhes do deployment:
```bash
kubectl describe deployment demo-deployment -n k8s-demo
```

## 📝 Notas para o Professor

- Este projeto é ideal para demonstração em sala de aula
- Permite mostrar conceitos práticos do Kubernetes
- Fácil de modificar e expandir
- Inclui exemplos de troubleshooting 