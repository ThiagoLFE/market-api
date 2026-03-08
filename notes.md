
## O que cada pasta faz

### schemas
- validação de dados da API (Pydantic)

### models
- estrutura da tabela do banco

### services
- lógica de negócio / queries SQL

### database
- conexão com banco

### main
- rotas da API


# Documentação do Banco de Dados – Sistema de Usuários e Compras

## 1. Tabela `usuarios`
Armazena os dados do usuário.

| Campo       | Tipo           | Descrição                               | Observações                      |
|------------|----------------|----------------------------------------|---------------------------------|
| id         | SERIAL / ObjectId | Identificador único do usuário         | Chave primária                  |
| nome       | VARCHAR(100)   | Nome completo do usuário               | Obrigatório                     |
| email      | VARCHAR(100)   | Email do usuário                        | Único, obrigatório              |
| senhaHash  | VARCHAR(255)   | Hash da senha                            | Nunca salvar a senha em texto  |

---

## 2. Tabela `produtos`
Armazena os produtos do catálogo.

| Campo       | Tipo           | Descrição                               | Observações                        |
|------------|----------------|----------------------------------------|-----------------------------------|
| id         | SERIAL / ObjectId | Identificador único do produto          | Chave primária                    |
| nome       | VARCHAR(100)   | Nome do produto                          | Obrigatório                       |
| preco      | DECIMAL(10,2)  | Preço do produto                         | Obrigatório                       |
| estoque    | INT            | Quantidade em estoque                     | Atualizado a cada venda           |
| imagem     | VARCHAR(255)   | URL ou caminho da imagem                 | Opcional                          |
| descricao  | TEXT           | Descrição do produto                     | Opcional                          |

---

## 3. Tabela `carrinho`
Relaciona usuários com produtos que ainda não foram finalizados em pedidos.

| Campo       | Tipo           | Descrição                               | Observações                         |
|------------|----------------|----------------------------------------|------------------------------------|
| id         | SERIAL / ObjectId | Identificador do item do carrinho       | Chave primária                     |
| usuario_id | INT / ObjectId | FK para `usuarios.id`                   | Cada usuário pode ter vários itens |
| produto_id | INT / ObjectId | FK para `produtos.id`                   | Cada produto pode estar em vários carrinhos |
| quantidade | INT            | Quantidade do produto no carrinho       | Obrigatório                         |

**Relação:**  
- `usuario_id` → 1 usuário pode ter N produtos no carrinho (1:N)  
- `produto_id` → N produtos podem estar em vários carrinhos (N:N conceitual)

---

## 4. Tabela `pedidos`
Armazena pedidos finalizados dos usuários.

| Campo       | Tipo           | Descrição                               | Observações                       |
|------------|----------------|----------------------------------------|----------------------------------|
| id         | SERIAL / ObjectId | Identificador do pedido                 | Chave primária                   |
| usuario_id | INT / ObjectId | FK para `usuarios.id`                   | Um usuário pode ter N pedidos    |
| data       | DATETIME       | Data de criação do pedido               | Automático                        |
| status     | VARCHAR(50)    | Status do pedido (ex: “pendente”, “pago”) |                                   |

---

## 5. Tabela `pedido_itens`
Relaciona produtos a pedidos, armazenando detalhes de cada item.

| Campo        | Tipo           | Descrição                               | Observações                       |
|-------------|----------------|----------------------------------------|----------------------------------|
| id          | SERIAL / ObjectId | Identificador do item                   | Chave primária                   |
| pedido_id   | INT / ObjectId | FK para `pedidos.id`                     | 1 pedido tem N produtos          |
| produto_id  | INT / ObjectId | FK para `produtos.id`                    | Produto comprado                 |
| quantidade  | INT            | Quantidade comprada                      | Obrigatório                       |
| preco_unitario | DECIMAL(10,2)| Preço do produto na compra               | Fixado no momento do pedido       |

**Relação:**  
- `pedido_id` → 1 pedido pode ter N produtos  
- `produto_id` → N pedidos podem ter o mesmo produto  

---

## 6. Diagrama conceitual de relações
usuarios (1) ──< (N) carrinho (N) >── produtos
usuarios (1) ──< (N) pedidos (1) ──< (N) pedido_itens (N) >── produtos

**Explicação:**
- Um usuário pode ter vários produtos no carrinho.
- Um usuário pode ter vários pedidos, cada pedido com vários produtos.
- Cada produto pode aparecer em múltiplos carrinhos e pedidos.