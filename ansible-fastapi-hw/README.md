# Ansible FastAPI Deployment

## Создание хоста через Terraform

```bash
cd terraform
terraform init
terraform apply
```

## Настройка inventory

Получите IP адрес из output Terraform:

```bash
terraform output vm_external_ip
```

Обновите файл `inventory`:

```ini
[servers]
server1 ansible_host=<IP_ИЗ_TERRAFORM_OUTPUT> ansible_user=ubuntu
```

## Запуск плейбука

```bash
ansible-playbook -i inventory playbook.yml
```
