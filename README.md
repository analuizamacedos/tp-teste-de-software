# Tracker+

## Grupo

Ana Luiza Macêdo dos Santos e Guilherme Mota Bromonschenkel Lima

## Visão geral

Tracker+ é um sistema web de controle de hábitos. O usuário pode cadastrar hábitos diários, marcar conclusão e acompanhar o progresso por meio de uma interface simples.

O sistema oferece:

- criação e listagem de hábitos
- marcação de conclusão diária
- cálculo de streaks (dias consecutivos)
- pontuação baseada em streaks
- leaderboard de hábitos concluídos

## Tecnologias utilizadas

- Back-end: Python, Flask
- Front-end: ReactJS, Vite
- Banco de dados: SQLite
- Testes: Pytest, Playwright

## Estrutura do projeto

- `tracker-plus/backend/` - código do servidor Flask e testes backend
- `tracker-plus/frontend/` - aplicação React e testes E2E com Playwright
- `.specs/` - especificações de desenvolvimento do projeto

## Instalação

### Back-end

```bash
cd tracker-plus/backend
pip install -r requirements.txt
```

### Front-end

```bash
cd tracker-plus/frontend
npm install
npx playwright install chromium
```

## Execução

### Rodar o backend

```bash
cd tracker-plus/backend
python run.py
```

O backend ficará disponível em `http://localhost:5000`.

### Rodar o frontend

```bash
cd tracker-plus/frontend
npm run dev
```

O frontend ficará disponível em `http://localhost:5173`.

## Testes

### Testes backend

```bash
cd tracker-plus/backend
python -m pytest tests/
```

### Testes E2E

```bash
cd tracker-plus/frontend
npm run test:e2e
```

### Cobertura de testes

Para gerar um relatório de cobertura do backend, execute:

```bash
cd tracker-plus/backend
python -m pytest --cov=app --cov-report=term tests/
```

O comando mostra o percentual de cobertura no terminal e permite gerar um relatório HTML adicional com `--cov-report=html`.

## Uso de IA

O desenvolvimento dessa aplicação contou com o auxílio de IA como recurso de apoio ao processo de análise, planejamento, implementação e revisão. A utilização da IA seguiu práticas para garantir qualidade, rastreabilidade e validação das decisões tomadas durante o desenvolvimento.

A abordagem adotada foi baseada em **Spec-Driven Development**, na qual o desenvolvimento foi dividido em especificações menores e bem definidas. Essas especificações serviram como direcionamento para a implementação das funcionalidades, permitindo que cada etapa fosse desenvolvida, revisada e validada individualmente.

As especificações utilizadas foram:

- **[SPEC-01](./.specs/spec-1.md):** Preparação da estrutura inicial do projeto, organização dos arquivos e configuração dos ambientes necessários para execução da aplicação.

- **[SPEC-02](./.specs/spec-2.md):** Criação da base de dados da aplicação, incluindo a definição das principais entidades do sistema e suas regras de funcionamento.

- **[SPEC-03](./.specs/spec-3.md):** Desenvolvimento das principais regras de negócio da aplicação, como cálculos, validações e comportamentos relacionados ao uso do sistema.

- **[SPEC-04](./.specs/spec-4.md):** Implementação das funcionalidades de gerenciamento dos dados, permitindo criar, visualizar, atualizar e remover informações da aplicação, juntamente com seus testes.

- **[SPEC-05](./.specs/spec-5.md):** Desenvolvimento da interface visual do sistema, incluindo as telas principais, componentes e elementos de interação com o usuário.

- **[SPEC-06](./.specs/spec-6.md):** Integração entre as funcionalidades do sistema, conectando as regras de negócio, armazenamento de dados e recursos apresentados ao usuário.

- **[SPEC-07](./.specs/spec-7.md):** Criação dos testes automatizados para validar o funcionamento completo da aplicação simulando a utilização real por um usuário.

A implementação foi realizada de forma incremental e supervisionada, executando cada especificação individualmente. Durante esse processo, os artefatos gerados pela IA foram revisados e validados humanamente, com atenção especial aos testes automatizados, que foram analisados conforme as boas práticas de testes abordadas em sala de aula.
