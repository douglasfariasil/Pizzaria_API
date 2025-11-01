# Documento de Requisitos de Produto (PRD) - API da Pizzaria

**Versão:** 1.0

**Data:** 2023-10-27

## 1. Visão Geral

Este documento descreve os requisitos para a API da Pizzaria. O objetivo do projeto é fornecer um backend robusto e seguro para um sistema de pedidos de pizza, permitindo o gerenciamento de usuários, autenticação e o ciclo de vida completo de um pedido, desde a sua criação até a finalização.

## 2. Objetivos do Produto

- Fornecer um sistema de cadastro e autenticação seguro para clientes.
- Permitir que clientes criem e gerenciem seus próprios pedidos de pizza.
- Oferecer funcionalidades administrativas para visualização e gerenciamento de todos os pedidos do sistema.
- Garantir a integridade e o status correto dos pedidos durante todo o processo.

## 3. Personas de Usuário

### 3.1. Cliente

- **Descrição:** Um usuário final que deseja pedir uma pizza.
- **Necessidades:**
  - Criar uma conta no sistema.
  - Fazer login de forma segura.
  - Criar um novo pedido.
  - Adicionar e remover itens (pizzas) do seu pedido.
  - Visualizar os detalhes e o status dos seus pedidos.
  - Finalizar um pedido para que ele seja preparado.
  - Cancelar um pedido que ainda não foi finalizado.

### 3.2. Administrador

- **Descrição:** Um funcionário da pizzaria responsável por gerenciar as operações.
- **Necessidades:**
  - Todas as permissões de um **Cliente**.
  - Acessar uma lista de **todos** os pedidos feitos no sistema.
  - Visualizar, cancelar, ou modificar qualquer pedido, independentemente do cliente que o criou.

## 4. Requisitos Funcionais

A API será dividida em dois módulos principais: **Autenticação** e **Pedidos**.

### 4.1. Módulo de Autenticação (`/auth`)

| Recurso           | Método | Endpoint              | Descrição                                                                                   | Nível de Acesso |
| :---------------- | :----- | :-------------------- | :------------------------------------------------------------------------------------------ | :-------------- |
| **Criar Conta**   | `POST` | `/auth/criar_conta`   | Registra um novo usuário no sistema. O e-mail deve ser único.                               | Público         |
| **Login (JSON)**  | `POST` | `/auth/login`         | Autentica um usuário com e-mail e senha, retornando um `access_token` e um `refresh_token`. | Público         |
| **Login (Form)**  | `POST` | `/auth/login-form`    | Autentica um usuário via formulário (OAuth2), retornando um `access_token`.                 | Público         |
| **Renovar Token** | `GET`  | `/auth/refresh_token` | Gera um novo `access_token` a partir de um `refresh_token` válido.                          | Autenticado     |

### 4.2. Módulo de Pedidos (`/orders`)

**Observação:** Todas as rotas deste módulo exigem um token de autenticação válido.

| Recurso                       | Método | Endpoint                                       | Descrição                                                                                 | Nível de Acesso         |
| :---------------------------- | :----- | :--------------------------------------------- | :---------------------------------------------------------------------------------------- | :---------------------- |
| **Criar Pedido**              | `POST` | `/orders/criar_pedido`                         | Cria um novo pedido vazio associado ao usuário.                                           | Autenticado             |
| **Cancelar Pedido**           | `POST` | `/orders/pedido/cancelar/{id_pedido}`          | Altera o status de um pedido para "CANCELADO".                                            | Dono do Pedido ou Admin |
| **Listar Todos os Pedidos**   | `GET`  | `/orders/listar`                               | Retorna uma lista com todos os pedidos registrados no sistema.                            | Admin                   |
| **Listar Pedidos do Usuário** | `GET`  | `/orders/listar/pedidos_usuario`               | Retorna uma lista de todos os pedidos feitos pelo usuário autenticado.                    | Autenticado             |
| **Visualizar Pedido**         | `GET`  | `/orders/pedido/{id_pedido}`                   | Exibe os detalhes completos de um pedido específico, incluindo seus itens.                | Dono do Pedido ou Admin |
| **Adicionar Item**            | `POST` | `/orders/pedido/adicionar_item/{id_pedido}`    | Adiciona um item (pizza) a um pedido existente. O preço total do pedido é recalculado.    | Dono do Pedido ou Admin |
| **Remover Item**              | `POST` | `/orders/pedido/remover_item/{id_item_pedido}` | Remove um item de um pedido. O preço total do pedido é recalculado.                       | Dono do Pedido ou Admin |
| **Finalizar Pedido**          | `POST` | `/orders/pedido/finalizar/{id_pedido}`         | Altera o status de "PENDENTE" para "FINALIZADO". O pedido deve conter pelo menos um item. | Dono do Pedido ou Admin |

## 5. Modelos de Dados Principais

### 5.1. Usuário

- `id`: Identificador único.
- `nome`: Nome do usuário.
- `email`: E-mail para login (único).
- `senha`: Senha criptografada.
- `ativo`: Status do usuário (booleano).
- `admin`: Indica se o usuário tem privilégios de administrador (booleano).

### 5.2. Pedido

- `id`: Identificador único.
- `usuario_id`: Chave estrangeira para o usuário que fez o pedido.
- `status`: Status atual do pedido (ex: PENDENTE, FINALIZADO, CANCELADO).
- `preco`: Preço total do pedido, calculado com base nos itens.
- `itens`: Lista de itens associados ao pedido.

### 5.3. ItemPedido

- `id`: Identificador único.
- `pedido_id`: Chave estrangeira para o pedido ao qual o item pertence.
- `quantidade`: Quantidade do item.
- `sabor`: Sabor da pizza.
- `tamanho`: Tamanho da pizza.
- `preco_unitario`: Preço da unidade do item.

## 6. Requisitos Não-Funcionais

- **Segurança:**
  - As senhas dos usuários devem ser armazenadas de forma criptografada (usando bcrypt).
  - O acesso às rotas de pedidos deve ser protegido por tokens JWT (JSON Web Tokens).
  - A validação de permissão (dono do pedido vs. administrador) deve ser aplicada em rotas sensíveis.
- **Desempenho:**
  - As consultas ao banco de dados devem ser otimizadas para garantir respostas rápidas.
- **Usabilidade:**
  - As mensagens de erro da API devem ser claras e informativas, indicando o motivo da falha (ex: "Pedido não encontrado", "Apenas administradores podem...").
