# Tracker+

## Grupo: Ana Luiza Macêdo dos Santos e Guilherme Mota Bromonschenkel Lima

## Explicação do Sistema

Sistema Web de Controle de Hábitos

O sistema consiste em um rastreador de hábitos (Habit Tracker) desenvolvido como uma aplicação web simples, permitindo ao usuário cadastrar hábitos diários e acompanhar sua execução ao longo do tempo por meio de uma interface interativa. O usuário poderá marcar hábitos como concluídos em cada dia, visualizar sua lista de hábitos e acompanhar o progresso individual.

Além disso, o sistema conta as seguintes funcionalidades adicionais:
- Cálculo de sequência de dias consecutivos (streak), permitindo medir a consistência do usuário.
- Sistema de pontuação gamificado estilo Gymrats para envolver interações entre usuários.
- Histórico de estatísticas, com premiações visuais.

## Testes Possíveis

Alguns testes que podem ser implementados neste projeto:

### Testes Unitários

- Verificar se um hábito é criado corretamente.
- Verificar se o nome do hábito não pode ser vazio.
- Verificar se o cálculo de *streak* está correto.
- Verificar se o *streak* é reiniciado quando há falha em um dia.
- Verificar se um hábito pode ser marcado como concluído.
- Verificar se um hábito não deve ser concluído duas vezes no mesmo dia.

### Testes de Integração

- Verificar se o cadastro de hábito é salvo corretamente pelo backend.
- Verificar se a listagem de hábitos retorna os dados cadastrados.

### Testes End-to-End

- Simular o fluxo completo: criar hábito → marcar como concluído → visualizar progresso.
- Verificar se o usuário consegue interagir com a interface sem erros.

## Tecnologias Utilizadas

- Back-end: Python (Flask)
- Front-end: ReactJS
- Pytest (framework de teste)

## Uso de IA

O desenvolvimento dessa aplicação contou com o auxílio de IA como recurso de apoio ao processo de análise, planejamento, implementação e revisão. A utilização da IA seguiu práticas para garantir qualidade, rastreabilidade e validação das decisões tomadas durante o desenvolvimento.

A abordagem adotada foi baseada em **Spec-Driven Design**, na qual o desenvolvimento foi dividido em especificações menores e bem definidas. Essas especificações serviram como direcionamento para a implementação das funcionalidades, permitindo que cada etapa fosse desenvolvida, revisada e validada individualmente.

As especificações utilizadas foram:

- **[SPEC-01](./.specs/spec-1.md):** Preparação da estrutura inicial do projeto, organização dos arquivos e configuração dos ambientes necessários para execução da aplicação.

- **[SPEC-02](./.specs/spec-2.md):** Criação da base de dados da aplicação, incluindo a definição das principais entidades do sistema e suas regras de funcionamento.

- **[SPEC-03](./.specs/spec-3.md):** Desenvolvimento das principais regras de negócio da aplicação, como cálculos, validações e comportamentos relacionados ao uso do sistema.

- **[SPEC-04](./.specs/spec-4.md):** Implementação das funcionalidades de gerenciamento dos dados, permitindo criar, visualizar, atualizar e remover informações da aplicação, juntamente com seus testes.

- **[SPEC-05](./.specs/spec-5.md):** Desenvolvimento da interface visual do sistema, incluindo as telas principais, componentes e elementos de interação com o usuário.

- **[SPEC-06](./.specs/spec-6.md):** Integração entre as funcionalidades do sistema, conectando as regras de negócio, armazenamento de dados e recursos apresentados ao usuário.

- **[SPEC-07](./.specs/spec-7.md):** Criação dos testes automatizados para validar o funcionamento completo da aplicação simulando a utilização real por um usuário.

Além da criação inicial das especificações, houve validação humana de todos os artefatos gerados pela IA, permitindo corrigir inconsistências, melhorar requisitos e ajustar decisões técnicas conforme as necessidades do projeto.

A implementação foi realizada de forma incremental e supervisionada, executando cada especificação individualmente e validando as alterações realizadas pela IA, tanto em relação ao código desenvolvido quanto ao atendimento dos requisitos definidos.

Dessa forma, a IA foi utilizada como ferramenta de apoio à produtividade e organização do desenvolvimento, mantendo a análise crítica, revisão e tomada de decisões sob responsabilidade humana.
