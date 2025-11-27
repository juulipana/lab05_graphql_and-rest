# GraphQL vs REST — Experimento Controlado  

## Introdução
O objetivo deste trabalho é avaliar, de forma quantitativa, se GraphQL realmente traz benefícios práticos quando comparado ao tradicional REST.

### Alunos
* Juliana Parreiras Guimarães da Cunha
* Pedro Henrique Marques de Oliveira

### Professor
* Danilo de Quadros Maia Filho

Nós investigamos duas perguntas principais:

- **RQ1:** Respostas GraphQL são mais rápidas que REST?  
- **RQ2:** Respostas GraphQL têm tamanho menor que REST?  

A seguir pode-se encontrar o desenho do experimento.

---

# 1. Desenho do Experimento

## A. Hipóteses Nula e Alternativa

| RQ | Hipótese Nula (H₀) | Hipótese Alternativa (H₁) |
|----|----------------------|----------------------------|
| **RQ1** | O tempo de resposta das requisições GraphQL **não é diferente** do tempo das requisições REST. | O tempo de resposta das requisições GraphQL é **menor** que o de REST. |
| **RQ2** | O tamanho das respostas GraphQL **não é diferente** do tamanho das respostas REST. | O tamanho das respostas GraphQL é **menor** que o de REST. |

---

## B. Variáveis Dependentes  
As variáveis que queremos **medir**:

- **Tempo de resposta (ms)**  
- **Tamanho da resposta (bytes ou KB)**  

---

## C. Variáveis Independentes  
As variáveis que **alteramos** no experimento:

- **Tipo de API**: REST vs GraphQL  
- **Tipo de consulta/teste** (ex.: consulta simples, consulta aninhada)

---

## D. Tratamentos  
Conjunto de condições experimentais:

- **T1 — REST**: Chamadas usando endpoints tradicionais.  
- **T2 — GraphQL**: Chamadas usando queries GraphQL equivalentes.  

---

## E. Objetos Experimentais  
O que será testado:
 
- Cenários reais de consulta;
- Comparar tempo de resposta;
- Comparar tamanho das respostas;

---

## F. Tipo de Projeto Experimental  
// TO-DO
---

## G. Quantidade de Medições  
Para cada tratamento:

- **N ≥ 30 medições por consulta** 
- Cada cenário será repetido exatamente da mesma forma para REST e GraphQL

---

## H. Ameaças à Validade

### **Interna**
- Cache do servidor pode enviesar resultados  
- Variações de rede durante os testes  
- Diferenças não intencionais entre implementações REST e GraphQL  

### **Externa**
- Resultados podem não representar outras APIs ou domínios  
- Implementações específicas podem favorecer um lado  

### **De Construção**
- Métricas podem não capturar toda a complexidade de "performance"  
- Definição das consultas REST e GraphQL pode não ser totalmente equivalente

## 2. Ambiente e Ferramentas

O experimento é executado localmente em uma máquina com as seguintes ferramentss principais: Requisições são feitas via requests e os dados armazenados e processados com pandas.

## 3. Coleta e Registro das Métricas

As medições são coletadas automaticamente e registradas em um arquivo CSV. Cada registro contém: nome do cenário, tratamento (REST ou GraphQL), índice da iteração, tempo de resposta em ms e tamanho da resposta em bytes. Logs estruturados são produzidos por structlog para rastreabilidade.

## 5. Análise Estatística Planejada

Os resultados são avaliados com testes de hipótese apropriados para experimentos pareados:

* Para RQ1 (tempo): teste t pareado ou Wilcoxon Signed‑Rank Test caso a normalidade não seja atendida.
* Para RQ2 (tamanho): teste t pareado ou teste de Wilcoxon.
* Normalidade verificada pelo teste de Shapiro‑Wilk.
* Tamanho de efeito calculado via Cohen’s d para interpretação prática.
