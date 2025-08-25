# Pré-processamento de Dados para LLM

Este projeto realiza o pré-processamento completo de textos em português para preparação de dados destinados a Large Language Models (LLM).

## 📋 Funcionalidades

O sistema executa 13 etapas sequenciais de pré-processamento:

1. **Remover tags HTML** - Remove tags e decodifica entidades HTML
2. **Remover URLs** - Remove links HTTP/HTTPS, www, e URLs encurtadas
3. **Remover emojis** - Remove emojis e símbolos Unicode
4. **Remover stopwords** - Remove palavras irrelevantes em português
5. **Remover sinais de pontuação** - Remove pontuação mantendo letras e números
6. **Remover caracteres especiais** - Remove caracteres especiais (exceto acentos)
7. **Remover espaços excedentes** - Remove múltiplos espaços e quebras de linha
8. **Substituir palavras de chat** - Normaliza abreviações (vc → você, pq → porque)
9. **Converter números em palavras** - Transforma dígitos em texto (3 → três)
10. **Converter para minúsculas** - Padroniza todo o texto em caixa baixa
11. **Correção ortográfica** - Aplica correções básicas de ortografia
12. **Stemização** - Reduz palavras ao seu radical
13. **Lematização** - Reduz palavras à sua forma canônica

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **NLTK** - Natural Language Toolkit para processamento de linguagem natural
- **TextBlob** - Biblioteca para processamento de texto
- **Inflect** - Conversão de números para palavras

## 📁 Estrutura do Projeto

```
Pre-processamento-de-dados-para-LLM/
├── preprocessamento_textos.py    # Script principal
├── jornal.txt                    # Texto do jornal A Tribuna
├── bula_doril.txt               # Bula do medicamento Doril
├── requirements.txt             # Dependências Python
├── setup_venv.sh               # Script de configuração do ambiente virtual
├── venv/                       # Ambiente virtual Python
├── jornal_processado.txt       # Resultado do pré-processamento do jornal
├── bula_processada.txt         # Resultado do pré-processamento da bula
└── README.md                   # Este arquivo

```

## 🚀 Como Usar



### Opção 2: Configuração manual

```bash
# 1. Cria o ambiente virtual
python3 -m venv venv

# 2. Ativa o ambiente virtual
source venv/bin/activate

# 3. Instala as dependências
pip install -r requirements.txt

# 4. Executa o script
python preprocessamento_textos.py

# 5. Para desativar o ambiente virtual
deactivate
```

## 📊 Exemplo de Execução

O script processa dois textos distintos:

### Jornal A Tribuna
- **Texto original**: 2.634 caracteres
- **Texto processado**: 1.598 caracteres  
- **Redução**: 39.3%

### Bula Doril
- **Texto original**: 13.742 caracteres
- **Texto processado**: 8.348 caracteres
- **Redução**: 39.3%

## 📈 Resultados

Após cada etapa, o sistema exibe:
- Tamanho do texto antes e depois
- Quantidade de caracteres removidos
- Amostra do resultado parcial
- Estatísticas de redução total

## 🎯 Casos de Uso

- Preparação de dados para treinamento de LLMs
- Limpeza de textos para análise de sentimentos
- Normalização de conteúdo web
- Processamento de documentos médicos
- Análise de conteúdo jornalístico

## 🔧 Personalização

Para adaptar o script aos seus dados:

1. **Substitua os arquivos de entrada**:
   - `jornal.txt` e `bula_doril.txt` pelos seus textos
   
2. **Modifique as stopwords**:
   - Edite `self.stop_words` na classe `TextPreprocessor`
   
3. **Ajuste palavras de chat**:
   - Modifique `self.chat_words` conforme necessário
   
4. **Configure correções ortográficas**:
   - Atualize `_basic_portuguese_corrections()` com suas correções específicas


## 📝 Notas Importantes

- O script foi otimizado para textos em **português brasileiro**
- A stemização e lematização usam o algoritmo Snowball para português
- A correção ortográfica é básica - para casos complexos, considere usar ferramentas especializadas
- Os arquivos processados são salvos automaticamente no diretório do projeto

