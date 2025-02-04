# Room Reservation API

## Setup e uso

### Rode a aplicação utilizando o código
```sh
docker compose up -d
```

### Preencha a database utilizando o código algumas vezes
```sh
python manage.py seed
```

### Rodar os testes
```sh
python manage.py test
```

## Documentação da API 

### Swagger UI
Para acessar a documentação pelo Swagger acesse:
```
http://localhost:8000/api/docs/
```
É possível conferir todas as rotas da API e como utilizar cada uma

### Paginação

As rotas de get (para os rooms, reservas e usuários) pode ser acrescida dos parâmetros:

```url
?page=number&page_size=number
```
para aumentar o tamanho do retorno (padrão 10) e o número da página.

### OBS: Para usar a rota de delete reservation, você precisa passar o token do criador (da tabela app_user) que é igual ao do user_name que está na reserva