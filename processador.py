import csv
from decimal import Decimal
from datetime import datetime
import os

class Processador:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.contas = {} #guardar o saldo de cad conta
        self.transacoes = []
        self.inconsistencias = []
        
        #totais
        self.total_creditos = Decimal('0.00')
        self.total_debitos = Decimal('0.00')
        self.total_registros = 0        

    def carregar_dados(self):
        if not os.path.exists(self.arquivo):
            print(f"Erro: O arquivo {self.arquivo} não foi encontrado.")
            return []

        dados = []
        try:
            with open(self.arquivo, mode='r', encoding='utf-8-sig') as file:
                
                #padroniza cabeçalho 
                leitor_bruto = csv.reader(file, delimiter=';')
                cabecalho = next(leitor_bruto)
                
                #tira espaço, letra maiúscula, Ç, acentuação
                cabecalho_novo = [col.strip().lower().replace('ç', 'c').replace('ã', 'a').replace('ó', 'o') for col in cabecalho]
                
                mapa_colunas = {}
                for i, col in enumerate(cabecalho_novo): #ajuda se mudar a ordem do cabeçalho, guarda cada info como um indice
                    mapa_colunas[col] = i

                file.seek(0) #volta p o início do arquivo
                next(file) # pula a linha do cabeçalho

                #lê os dados 
                leitor = csv.reader(file, delimiter=';')
                
                for linha in leitor:
                    if not linha: continue #linhas vazias
                    
                    # mapa_colunas pega o valor pelo índice
                    try:
                        # busca dinâmica, posição da coluna
                        idx_data = mapa_colunas.get('data')
                        idx_conta = mapa_colunas.get('conta')
                        idx_tipo = mapa_colunas.get('tipo')
                        idx_valor = mapa_colunas.get('valor')
                        
                        # acha descrição
                        idx_desc = mapa_colunas.get('descricao') 

                        # extrai os valores usando os índices do mapa_colunas
                        registro = {
                            'data': linha[idx_data],
                            'conta': linha[idx_conta].upper(),  
                            'tipo': linha[idx_tipo].upper().strip(),
                            'valor': Decimal(linha[idx_valor].replace(',', '.')), # vírgula tratada cm decimal se houver
                            'descricao': linha[idx_desc] if idx_desc is not None else "Sem descricao"
                        }
                        dados.append(registro)

                    except Exception as e:
                        print(f"Linha ignorada: {linha} \nErro: {e}")

        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            import traceback
            traceback.print_exc() #mostra erro
            return []
            
        return dados
    
    def processar(self):
        transacoes = self.carregar_dados()
        #print(transacoes)
        for texto in transacoes:
            conta = texto['conta']
            tipo = texto['tipo']
            valor = texto['valor']
            
            # inicia a conta
            if conta not in self.contas:
                self.contas[conta] = Decimal('0.00')
            
            saldo_atual = self.contas[conta]
            saldo_previsto = saldo_atual
            
            #cálculo saldo 
            if tipo == 'C':
                saldo_previsto += valor
                self.total_creditos += valor
            elif tipo == 'D':
                saldo_previsto -= valor
                self.total_debitos += valor
            
            # se deixar o saldo negativo, registra inconsistência
            if saldo_previsto < Decimal('0.00'):
                self.inconsistencias.append(
                    f"Incosistencia: Transação ignorada {conta}.\n"
                    f"Saldo atual: {saldo_atual}, Tentativa de débito: {valor}"
                )
                continue
            
            #efetiva a transação
            self.contas[conta] = saldo_previsto
            self.total_registros += 1
            self.transacoes.append(texto)

    def gerar_relatorio(self):
        print("--- RELATÓRIO DE PROCESSAMENTO -*--")
        print(f"Total de Registros Processados: {self.total_registros}")
        print(f"Total de Créditos: R$ {self.total_creditos}")
        print(f"Total de Débitos: R$ {self.total_debitos}")
        print("-" * 30)
        
        print("--- SALDOS FINAIS POR CONTA ---")
        for conta in sorted(self.contas.keys()):
            saldo = self.contas[conta]
            print(f"Conta: {conta} | Saldo: R$ {saldo:.2f}")
            
        print("-" * 30)
        print("\n--- AVISOS --")
        for aviso in self.inconsistencias:
            print(aviso) 

        