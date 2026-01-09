# Terraform конфигурация для SpillBillService

1. **Скопируйте пример файла переменных**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Заполните `terraform.tfvars`**:
   - `yandex_token` - OAuth токен Yandex Cloud
   - `cloud_id` - ID вашего облака
   - `folder_id` - ID каталога
   - `ssh_public_key_path` - путь к SSH публичному ключу

3. **Разверните инфраструктуру**:
   ```bash
   terraform apply
   ```

