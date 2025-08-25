#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para pré-processamento de textos: jornal A Tribuna e bula do medicamento Doril
Data: 2025-01-24
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import unicodedata
import html
from textblob import TextBlob
import inflect
import warnings
warnings.filterwarnings('ignore')

class TextPreprocessor:
    def __init__(self):
        """Inicializa o pré-processador de textos"""
        # Download de recursos necessários do NLTK
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        
        # Inicialização de ferramentas
        self.stop_words = set(stopwords.words('portuguese'))
        self.stemmer = SnowballStemmer('portuguese')
        self.lemmatizer = WordNetLemmatizer()
        self.inflect_engine = inflect.engine()
        
        # Dicionário de palavras de chat para formas normais
        self.chat_words = {
            'vc': 'você',
            'vcs': 'vocês',
            'q': 'que',
            'pq': 'porque',
            'n': 'não',
            'tb': 'também',
            'mt': 'muito',
            'kk': 'haha',
            'rsrs': 'haha',
            'blz': 'beleza',
            'vlw': 'valeu',
            'flw': 'falou',
            'cmg': 'comigo',
            'ctg': 'contigo',
            'hj': 'hoje',
            'ontem': 'ontem',
            'amanha': 'amanhã',
            'sdd': 'saudade',
            'bjs': 'beijos',
            'abraços': 'abraços'
        }
    
    def step_1_remove_html_tags(self, text):
        """1. Remove tags HTML"""
        clean_text = re.sub(r'<[^>]+>', '', text)
        clean_text = html.unescape(clean_text)
        return clean_text.strip()
    
    def step_2_remove_urls(self, text):
        """2. Remove URLs"""
        # Remove URLs HTTP/HTTPS
        clean_text = re.sub(r'https?://\S+', '', text)
        # Remove URLs www
        clean_text = re.sub(r'www\.\S+', '', text)
        # Remove URLs encurtadas (t.co, bit.ly, etc.)
        clean_text = re.sub(r't\.co/\S+', '', text)
        clean_text = re.sub(r'bit\.ly/\S+', '', text)
        return clean_text.strip()
    
    def step_3_remove_emojis(self, text):
        """3. Remove emojis"""
        # Remove emojis usando regex Unicode
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)
    
    def step_4_remove_stopwords(self, text):
        """4. Remove stopwords"""
        words = word_tokenize(text.lower())
        filtered_words = [word for word in words if word not in self.stop_words and len(word) > 2]
        return ' '.join(filtered_words)
    
    def step_5_remove_punctuation(self, text):
        """5. Remove sinais de pontuação"""
        # Remove pontuação, mantendo apenas letras, números e espaços
        clean_text = re.sub(r'[^\w\s]', ' ', text)
        return clean_text
    
    def step_6_remove_special_chars(self, text):
        """6. Remove caracteres especiais (exceto emojis)"""
        # Remove caracteres especiais mantendo letras, números, espaços e acentos
        clean_text = re.sub(r'[^a-zA-ZÀ-ÿ0-9\s]', ' ', text)
        return clean_text
    
    def step_7_remove_extra_whitespace(self, text):
        """7. Remove espaços em branco excedentes"""
        # Remove múltiplos espaços e quebras de linha
        clean_text = re.sub(r'\s+', ' ', text)
        return clean_text.strip()
    
    def step_8_replace_chat_words(self, text):
        """8. Substitui palavras usadas em chat por suas formas normais"""
        words = text.split()
        normalized_words = []
        for word in words:
            word_lower = word.lower()
            if word_lower in self.chat_words:
                normalized_words.append(self.chat_words[word_lower])
            else:
                normalized_words.append(word)
        return ' '.join(normalized_words)
    
    def step_9_convert_numbers_to_words(self, text):
        """9. Converte números em palavras"""
        def number_to_words(match):
            number = match.group()
            try:
                # Tenta converter para inteiro
                num = int(number)
                if num < 1000000:  # Limita números muito grandes
                    # Como o inflect é em inglês, fazemos uma conversão básica
                    return self._number_to_portuguese(num)
                return number
            except ValueError:
                return number

        text = re.sub(r'\b\d+\b', number_to_words, text)
        return text
    
    def _number_to_portuguese(self, num):
        """Converte números para palavras em português (básico)"""
        numbers_dict = {
            0: 'zero', 1: 'um', 2: 'dois', 3: 'três', 4: 'quatro', 5: 'cinco',
            6: 'seis', 7: 'sete', 8: 'oito', 9: 'nove', 10: 'dez',
            11: 'onze', 12: 'doze', 13: 'treze', 14: 'quatorze', 15: 'quinze',
            16: 'dezesseis', 17: 'dezessete', 18: 'dezoito', 19: 'dezenove', 20: 'vinte',
            30: 'trinta', 40: 'quarenta', 50: 'cinquenta', 60: 'sessenta',
            70: 'setenta', 80: 'oitenta', 90: 'noventa', 100: 'cem'
        }
        
        if num in numbers_dict:
            return numbers_dict[num]
        elif num < 100:
            dezena = (num // 10) * 10
            unidade = num % 10
            if dezena in numbers_dict and unidade in numbers_dict:
                return f"{numbers_dict[dezena]} e {numbers_dict[unidade]}"
        
        return str(num)  # Retorna o número original se não conseguir converter
    
    def step_10_convert_to_lowercase(self, text):
        """10. Converte todo o texto para letras minúsculas"""
        return text.lower()
    
    def step_11_spelling_correction(self, text):
        """11. Aplica correção ortográfica"""
        try:
            # Usa TextBlob para correção ortográfica 
            # Para português, fazemos correções básicas manuais
            corrected_text = self._basic_portuguese_corrections(text)
            return corrected_text
        except:
            return text
    
    def _basic_portuguese_corrections(self, text):
        """Correções ortográficas básicas em português"""
        corrections = {
            'nao': 'não',
            'voce': 'você',
            'tambem': 'também',
            'alem': 'além',
            'porem': 'porém',
            'atraves': 'através',
            'pos': 'pós',
            'pre': 'pré',
            'anti': 'anti',
            'sobre': 'sobre',
            'entre': 'entre'
        }
        
        words = text.split()
        corrected_words = []
        for word in words:
            if word in corrections:
                corrected_words.append(corrections[word])
            else:
                corrected_words.append(word)
        
        return ' '.join(corrected_words)
    
    def step_12_stemming(self, text):
        """12. Aplica stemização"""
        words = word_tokenize(text)
        stemmed_words = [self.stemmer.stem(word) for word in words if word.isalpha()]
        return ' '.join(stemmed_words)
    
    def step_13_lemmatization(self, text):
        """13. Aplica lematização"""
        words = word_tokenize(text)
        # Para português, usamos stemming como aproximação da lematização
        lemmatized_words = [self.stemmer.stem(word) for word in words if word.isalpha()]
        return ' '.join(lemmatized_words)
    
    def preprocess_text(self, text, text_name="Texto"):
        """Executa todas as etapas de pré-processamento"""
        print(f"\n{'='*80}")
        print(f"PRÉ-PROCESSAMENTO DO {text_name.upper()}")
        print(f"{'='*80}")
        
        # Texto original
        print(f"\n--- TEXTO ORIGINAL ---")
        print(f"Tamanho: {len(text)} caracteres")
        print(f"Primeiros 200 caracteres: {text[:200]}...")
        
        steps = [
            ("1. Remover tags HTML", self.step_1_remove_html_tags),
            ("2. Remover URLs", self.step_2_remove_urls),
            ("3. Remover emojis", self.step_3_remove_emojis),
            ("4. Remover stopwords", self.step_4_remove_stopwords),
            ("5. Remover sinais de pontuação", self.step_5_remove_punctuation),
            ("6. Remover caracteres especiais", self.step_6_remove_special_chars),
            ("7. Remover espaços excedentes", self.step_7_remove_extra_whitespace),
            ("8. Substituir palavras de chat", self.step_8_replace_chat_words),
            ("9. Converter números em palavras", self.step_9_convert_numbers_to_words),
            ("10. Converter para minúsculas", self.step_10_convert_to_lowercase),
            ("11. Correção ortográfica", self.step_11_spelling_correction),
            ("12. Stemização", self.step_12_stemming),
            ("13. Lematização", self.step_13_lemmatization)
        ]
        
        current_text = text
        
        for step_name, step_function in steps:
            print(f"\n--- {step_name.upper()} ---")
            previous_length = len(current_text)
            current_text = step_function(current_text)
            current_length = len(current_text)
            
            print(f"Tamanho antes: {previous_length} caracteres")
            print(f"Tamanho depois: {current_length} caracteres")
            print(f"Redução: {previous_length - current_length} caracteres")
            
            # Mostra amostra do resultado
            if len(current_text) > 0:
                sample_length = min(200, len(current_text))
                print(f"Amostra do resultado: {current_text[:sample_length]}...")
            else:
                print("Resultado: [texto vazio]")
        
        print(f"\n--- RESULTADO FINAL ---")
        print(f"Texto original: {len(text)} caracteres")
        print(f"Texto final: {len(current_text)} caracteres")
        print(f"Redução total: {len(text) - len(current_text)} caracteres ({((len(text) - len(current_text)) / len(text) * 100):.1f}%)")
        
        return current_text

def main():
    """Função principal"""
    print("Iniciando pré-processamento de textos...")
    
    # Inicializa o pré-processador
    preprocessor = TextPreprocessor()
    
    # Lê os arquivos
    try:
        with open('jornal.txt', 'r', encoding='utf-8') as file:
            jornal_text = file.read()
        
        with open('bula_doril.txt', 'r', encoding='utf-8') as file:
            bula_text = file.read()
        
        # Processa o texto do jornal
        jornal_processed = preprocessor.preprocess_text(jornal_text, "JORNAL A TRIBUNA")
        
        # Processa a bula do medicamento
        bula_processed = preprocessor.preprocess_text(bula_text, "BULA DORIL")
        
        # Salva os resultados processados
        with open('/home/eduardo/Desktop/IFES/Pre-processamento-de-dados-para-LLM/jornal_processado.txt', 'w', encoding='utf-8') as file:
            file.write(jornal_processed)
        
        with open('/home/eduardo/Desktop/IFES/Pre-processamento-de-dados-para-LLM/bula_processada.txt', 'w', encoding='utf-8') as file:
            file.write(bula_processed)
        
        # Comparação final
        print(f"\n{'='*80}")
        print("COMPARAÇÃO FINAL")
        print(f"{'='*80}")
        
        print(f"\nJORNAL A TRIBUNA:")
        print(f"Original: {len(jornal_text)} caracteres")
        print(f"Processado: {len(jornal_processed)} caracteres")
        print(f"Redução: {len(jornal_text) - len(jornal_processed)} caracteres ({((len(jornal_text) - len(jornal_processed)) / len(jornal_text) * 100):.1f}%)")
        
        print(f"\nBULA DORIL:")
        print(f"Original: {len(bula_text)} caracteres")
        print(f"Processado: {len(bula_processed)} caracteres")
        print(f"Redução: {len(bula_text) - len(bula_processed)} caracteres ({((len(bula_text) - len(bula_processed)) / len(bula_text) * 100):.1f}%)")
        
        print(f"\nArquivos processados salvos:")
        print("- jornal_processado.txt")
        print("- bula_processada.txt")
        
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
    except Exception as e:
        print(f"Erro durante o processamento: {e}")

if __name__ == "__main__":
    main()
