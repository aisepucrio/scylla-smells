# **Code Smells Detection**

Este projeto tem como objetivo detectar *code smells* em arquivos Python, auxiliando desenvolvedores a melhorar a qualidade do código, reduzindo complexidade e facilitando a manutenção. O sistema identifica os seguintes *code smells*:

1. **Too Many Arguments**  
2. **Long Method**  
3. **Dead Code**  
4. **Large Class**  
5. **Lazy Class**  
6. **Parallel Inheritance Hierarchy**  

---

## **Ferramentas Utilizadas**

- **[Pylint](https://pylint.pycqa.org/en/latest/):** Ferramenta de análise estática usada para identificar problemas de conformidade com padrões de codificação e potenciais *code smells*.  
- **AST (Abstract Syntax Tree):** Biblioteca nativa do Python usada para analisar a estrutura do código e extrair informações relevantes, como classes, métodos e atributos.

---

## **Code Smells Detectados**

### 1. **Too Many Arguments**
- **Descrição:** Funções com muitos argumentos dificultam a legibilidade e a manutenção do código.  
- **Critério de Detecção:** Funções com mais de 5 argumentos.  
- **Como foi detectado:**  
  - Utilizamos o Pylint com o parâmetro `--max-args=5`.  
  - O script processa mensagens como **R0913: Too many arguments** e retorna a localização e o número de argumentos excedentes.

---

### 2. **Long Method**
- **Descrição:** Métodos com muitas linhas de código tornam-se difíceis de entender e manter.  
- **Critério de Detecção:** Métodos com mais de 30 linhas.  
- **Como foi detectado:**  
  - Implementamos uma análise personalizada que conta as linhas de cada método.  
  - Métodos com mais de 30 linhas são identificados como *Long Method*, e o total de linhas é exibido.

---

### 3. **Dead Code**
- **Descrição:** Código que não é utilizado ou referenciado, como variáveis, métodos, importações e classes que nunca são usados.  
- **Critério de Detecção:**  
  - Variáveis, métodos ou classes declarados, mas não utilizados.  
  - Importações não usadas.  
- **Como foi detectado:**  
  - O Pylint foi configurado para identificar padrões como:
    - **W0612:** Variáveis não usadas.
    - **W0613:** Argumentos de função não utilizados.
    - **W0611:** Importações não utilizadas.
  - Análise adicional identifica funções e classes declaradas, mas não referenciadas em nenhum lugar do código.

---

### 4. **Large Class**
- **Descrição:** Classes grandes com muitos métodos, atributos ou linhas de código podem ser difíceis de entender e manter.  
- **Critério de Detecção:**  
  - Classes com mais de 200 linhas.  
  - Soma de métodos e atributos maior que 40.  
- **Como foi detectado:**  
  - O Pylint foi usado para contar métodos e atributos públicos, emitindo mensagens como **R0902: Too many instance attributes** e **R0904: Too many public methods**.  
  - Também implementamos contadores personalizados para determinar o tamanho total da classe em linhas.

---

### 5. **Lazy Class**
- **Descrição:** Classes que possuem poucos métodos ou atributos, não justificando sua existência, podendo ser simplificadas ou integradas a outras classes.  
- **Critério de Detecção:**  
  - Número de métodos menor que 5 **OU** número de atributos menor que 5.  
  - Profundidade da herança menor que 2.  
- **Como foi detectado:**  
  - A análise utiliza a biblioteca `ast` para mapear métodos, atributos e hierarquias de herança.  
  - Classes que atendem a esses critérios são classificadas como *Lazy Class*, e os motivos são detalhados no relatório.

---

### 6. **Parallel Inheritance Hierarchy**
- **Descrição:** Ocorrência de hierarquias de herança paralelas, onde uma classe possui muitos filhos diretos ou está em um nível de herança muito profundo.  
- **Critério de Detecção:**  
  - Profundidade da herança maior que 3.  
  - Número de filhos diretos maior que 4.  
- **Como foi detectado:**  
  - A análise estrutural utiliza a biblioteca `ast` para mapear relações de herança.  
  - Classes problemáticas são marcadas com base nos critérios acima.

---

## **Como Utilizar**

1. **Instale as dependências:**  
   Certifique-se de que o Pylint está instalado no seu ambiente:  
   ```bash
   pip install pylint
   ```

2. **Prepare os arquivos para análise:**  
   Coloque os arquivos Python que você deseja verificar no diretório configurado no script.

3. **Execute o script principal:**  
   Rode o script para iniciar a análise:  
   ```bash
   python main.py
   ```

4. **Resultados:**  
   - O script gera um arquivo CSV no diretório raiz, contendo os resultados detalhados de cada *code smell*.  
   - Os campos no CSV incluem:
     - **Arquivo:** Caminho do arquivo onde o problema foi encontrado.  
     - **Linha Inicial:** Linha onde o problema começa.  
     - **Linha Final:** Linha onde o problema termina.  
     - **Code Smell:** Nome do *code smell*.  
     - **Descrição:** Detalhes adicionais sobre o problema.  

