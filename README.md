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
http://localhost:8080/api/docs/
```
É possível conferir todas as rotas da API e como utilizar cada uma

### Paginação

As rotas de get (para os rooms, reservas e usuários) pode ser acrescida dos parâmetros:

```url
?page=number&page_size=number
```
para aumentar o tamanho do retorno (padrão 10) e o número da página.

### OBS: Para usar a rota de delete reservation, você precisa passar o token do criador (da tabela app_user) que é igual ao do user_name que está na reserva

### Rotas e como utilizar
O projeto possui as seguintes rotas (todas começando com /api/)

### Rotas de usuário
a primeira retorna todos os usuários (pode ser paginada) e a segunda especifica um através do id
```
GET users 

GET users/<int:pk> 
```

A rota post cria um usuário, com o body necessitando de um email e um nome (gera um auth_token automáticamente, que é utilizado para cancelar a reserva)
Já a rota PUT apenas atualiza o usuário da requisição (id) com o novo email/nome no body

```
POST users/create

PUT users/update/<int:pk>
```
Essa rota apaga um usuário do banco
```
DELETE users/delete/<int:pk>
```

# Rotas de Room

A rota rooms retorna todos os Rooms e pode ser paginada

a rota post requer um body de um Room para criar um novo, devendo conter no body: name, location e capacity

a última rota post requer o id de um Room e uma data de início e fim, para verificar se há alguma outra reserva durante o período
```
GET rooms

POST rooms/create

GET rooms/<int:pk>/availability/start_time=<str:start_time>&end_time=<str:end_time> 
```

# Rotas de Reservation

A rota post cadastra uma nova Reservation, precisando de ter no body, um room (id), user_name, start_date e end_date
A rota de DELETE necessita do id da reserva a ser deletado e o token que corresponde ao user_name
Já a rota GET retorna todas as reservas de um Room
```
POST reservations/

DELETE reservations/<int:pk>/cancel/<str:token> 

GET rooms/<int:pk>/reservations/ 
```