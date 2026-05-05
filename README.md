# Tracker+

## Grupo: Ana Luiza Macêdo dos Santos e Guilherme Mota Bromonschenkel Lima


## Explicação do Sistema

Sistema Web de Controle de Hábitos

O sistema consiste em um rastreador de hábitos (Habit Tracker) desenvolvido como uma aplicação web simples, permitindo ao usuário cadastrar hábitos diários e acompanhar sua execução ao longo do tempo por meio de uma interface interativa. O usuário poderá marcar hábitos como concluídos em cada dia, visualizar sua lista de hábitos e acompanhar o progresso individual.

O sistema também inclui o cálculo de sequência de dias consecutivos (streak), permitindo medir a consistência do usuário. O projeto tem como principal objetivo evidenciar a importância dos testes de software na validação das regras de negócio e na manutenção do sistema.

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

- Python (backend com Flask)
- HTML (estrutura da interface)
- CSS (estilização da interface)
- JavaScript (interação com o usuário)
- Pytest (framework de teste)
