#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para comparação dos textos originais vs processados
Mostra o antes e depois do pré-processamento
"""

def compare_texts():
    """Compara os textos originais com os processados"""
    
    print("="*80)
    print("COMPARAÇÃO: TEXTO ORIGINAL vs TEXTO PROCESSADO")
    print("="*80)
    
    # Carrega os arquivos
    files = [
        ("JORNAL A TRIBUNA", "jornal.txt", "jornal_processado.txt"),
        ("BULA DORIL", "bula_doril.txt", "bula_processada.txt")
    ]
    
    for title, original_file, processed_file in files:
        print(f"\n🔍 {title}")
        print("-" * 50)
        
        try:
            # Lê arquivo original
            with open(original_file, 'r', encoding='utf-8') as f:
                original_text = f.read()
            
            # Lê arquivo processado
            with open(processed_file, 'r', encoding='utf-8') as f:
                processed_text = f.read()
            
            # Estatísticas
            original_len = len(original_text)
            processed_len = len(processed_text)
            reduction = original_len - processed_len
            reduction_pct = (reduction / original_len) * 100
            
            print(f"📊 ESTATÍSTICAS:")
            print(f"   Tamanho original: {original_len:,} caracteres")
            print(f"   Tamanho processado: {processed_len:,} caracteres")
            print(f"   Redução: {reduction:,} caracteres ({reduction_pct:.1f}%)")
            
            # Contagem de palavras
            original_words = len(original_text.split())
            processed_words = len(processed_text.split())
            
            print(f"   Palavras originais: {original_words:,}")
            print(f"   Palavras processadas: {processed_words:,}")
            print(f"   Redução de palavras: {original_words - processed_words:,}")
            
            # Amostra do texto original (primeiras 200 caracteres)
            print(f"\n📝 TEXTO ORIGINAL (amostra):")
            print(f"   \"{original_text[:200]}...\"")
            
            # Amostra do texto processado (primeiras 200 caracteres)
            print(f"\n✨ TEXTO PROCESSADO (amostra):")
            print(f"   \"{processed_text[:200]}...\"")
            
            print("\n" + "="*50)
            
        except FileNotFoundError as e:
            print(f"❌ Erro: Arquivo não encontrado - {e}")
        except Exception as e:
            print(f"❌ Erro ao processar {title}: {e}")

if __name__ == "__main__":
    compare_texts()
