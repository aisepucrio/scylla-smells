

# **Code Smells Detection**

Este projeto tem como objetivo detectar *code smells* em arquivos Python para ajudar a melhorar a qualidade do código. Ele identifica os seguintes *code smells*:

1. **Too Many Arguments**  
2. **Long Method**  
3. **Dead Code (EM ANDAMENTO)**  
4. **Large Class**

## **Ferramentas Utilizadas**

Para a análise de *code smells*, utilizamos o [Pylint](https://pylint.pycqa.org/en/latest/), uma ferramenta poderosa para análise estática de código Python. As verificações foram implementadas em um conjunto de scripts que processam a saída do Pylint e aplicam regras adicionais para cada *code smell*.

---

## **Code Smells Detectados**

### 1. **Too Many Arguments**
- **Descrição:** Este *code smell* ocorre quando uma função tem muitos argumentos, o que dificulta a legibilidade e manutenção do código.  
- **Critério de Detecção:** Funções com mais de 5 argumentos.  
- **Como foi detectado:** 
  - Utilizamos o Pylint para identificar funções com argumentos excessivos, configurando o parâmetro `--max-args=5`.  
  - O Pylint emite a mensagem **R0913: Too many arguments** para funções que atendem a este critério.  
  - O script processa esta mensagem e retorna a localização do problema.

---

### 2. **Long Method**
- **Descrição:** Um método é considerado longo quando possui muitas linhas de código, dificultando sua compreensão e manutenção.  
- **Critério de Detecção:** Métodos com mais de 30 linhas.  
- **Como foi detectado:** 
  - Implementamos um analisador personalizado que varre os arquivos Python e conta o número de linhas de cada método.  
  - Se um método ultrapassar 30 linhas, ele é marcado como *Long Method*.  

---

### 3. **Dead Code**
- **Descrição:** Código que não é utilizado ou referenciado no programa. Isso pode incluir variáveis, métodos ou classes que nunca são usados.  
- **Critério de Detecção:** Variáveis, métodos ou classes declarados, mas não utilizados em nenhum lugar.  
- **Como foi detectado:** 
  - (EM ANDAMENTO)

---

### 4. **Large Class**
- **Descrição:** Classes que possuem muitos métodos e atributos ou um número excessivo de linhas de código, tornando-as difíceis de manter.  
- **Critério de Detecção:**
  - Classes com 200 ou mais linhas, ou  
  - A soma de métodos e atributos maior que 40.  
- **Como foi detectado:** 
  - Utilizamos o Pylint para calcular o número de métodos e atributos, configurando o parâmetro `--max-attributes`.  
  - O Pylint emite mensagens como **R0902: Too many instance attributes** e **R0904: Too many public methods**, que foram processadas para determinar se uma classe é grande.  
  - Implementamos uma verificação personalizada para também contar o número de linhas de cada classe.

---

## **Como Utilizar**

1. **Instale as dependências:**
   Certifique-se de que você tem o Pylint instalado:
   ```bash
   pip install pylint
   ```

2. **Organize os arquivos:**
   Coloque os arquivos Python que você deseja analisar no diretório configurado no script (`directory_path`).

3. **Execute o script:**
   Rode o script principal para realizar a análise:
   ```bash
   python main.py
   ```

4. **Confira os resultados:**
   Os *code smells* encontrados serão exibidos no console no formato:
   ```
   (nome_do_arquivo, linha_inicial, linha_final, "Nome do Code Smell")
   ```



