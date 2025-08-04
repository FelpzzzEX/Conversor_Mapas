# 🧠 Conversor de Mapas - Buscas

## 📌 Descrição

Este projeto realiza a conversão de mapas em imagem (`.png`) para arquivos de texto, por meio de um algoritmo de classificação de terrenos baseado em cores. O sistema reconhece diferentes tipos de terrenos e estruturas, transformando as imagens em representações textuais que podem ser utilizadas em ambientes de jogos, simulações ou projetos acadêmicos.

Uma interface gráfica foi desenvolvida com `Tkinter` para permitir a visualização dos mapas processados, facilitando a validação dos dados convertidos.

---

## 🖼️ Como Funciona

1. O programa analisa imagens pixel a pixel e determina o tipo de terreno com base na cor.
2. Um algoritmo de votação (com amostragem local) é usado para determinar o terreno dominante em cada célula de uma grade definida.
3. As imagens são convertidas para mapas textuais que representam o layout do mapa.
4. A interface gráfica exibe os mapas convertidos, colorindo cada célula de acordo com o tipo de terreno.

---

## 📂 Estrutura de Pastas

- `mapas_brutos/`  
  Pasta onde você deve colocar os arquivos de imagem `.png` a serem processados.

- `mapas_processados/`  
  Pasta onde os arquivos `.txt` com os mapas convertidos serão salvos automaticamente.

---

## ▶️ Como Usar

1. **Pré-requisitos**  
   Certifique-se de ter o Python 3.x e as bibliotecas a seguir instaladas:

   ```bash
   pip install pillow
   sudo apt-get install python3-tk # Somente Linux

2. **Adicionar Mapas:**
   Coloque os arquivos `.png` desejados na pasta `mapas_brutos/`.

3. **Executar o Programa:**

   A execução pode ser feita pela IDE escolhida (Visual Studio Code, por exemplo) ou através do terminal, com:  
   ```bash
   python main.py
   ```
   ou
   ```bash
   python3 main.py # Linux
   ```

5. **Interface Gráfica**

   * Clique em **"(Re)Gerar Mapas"** para processar ou atualizar os arquivos.
   * Use os botões como **"Ver Hyrule"**, **"Ver Masmorra 1"**, etc., para visualizar os mapas.

---

## 🧱 Terrenos Reconhecidos

### Terrenos do Mapa Externo (Hyrule)

| Cor RGB         | Terreno     | Símbolo | Visualização   |
| --------------- | ----------- | ------- | -------------- |
| (34, 177, 76)   | Grama       | G       | darkgreen      |
| (127, 211, 118) | Grama Clara | g       | limegreen      |
| (99, 155, 255)  | Água        | A       | royalblue      |
| (185, 122, 87)  | Montanha    | M       | sienna         |
| (234, 210, 163) | Areia       | S       | khaki          |
| (0, 100, 0)     | Floresta    | F       | darkolivegreen |

### Terrenos das Masmorras

| Cor RGB         | Tipo    | Símbolo | Visualização |
| --------------- | ------- | ------- | ------------ |
| (230, 230, 230) | Caminho | C       | lightgray    |
| (177, 177, 177) | Parede  | #       | dimgray      |

---

## 🧪 Exemplos de Mapas Processados

* `hyrule.txt` - Mapa externo grande (42x42)
* `masmorra1.txt` - Primeira dungeon (28x28)
* `masmorra2.txt` - Segunda dungeon (28x28)
* `masmorra3.txt` - Terceira dungeon (28x28)

---

## 🧑‍💻 Autor

**Felipe Fialho** - Projeto desenvolvido como parte do trabalho prático de Inteligência Artificial.

---

## 📃 Licença

Este projeto é de uso acadêmico e educacional. Modificações e melhorias são bem-vindas com os devidos créditos.

---

## 🔧 Ferramentas utilizadas

O desenvolvimento deste projeto contou com apoio de ferramentas de inteligência artificial, incluindo o **Google Gemini**, especialmente na solução de problemas relacionados à detecção de cores e na escolha e uso de bibliotecas adequadas para o processamento de imagem.
