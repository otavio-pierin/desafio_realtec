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
                #guarda uma lista de listas com cada uma das linhas
                #[["data1","conta1","tipo","valor","desc1"] --> leitor_bruto[0]
                #["data2","conta2","tipo","valor","desc2"]] --> leitor_bruto[1]
                leitor_bruto = list(csv.reader(file, delimiter=';'))
                
                if not leitor_bruto:
                    return []

                #detecta se tem um cabeçalho
                primeira_linha = leitor_bruto[0]
                try:
                    Decimal(primeira_linha[3].strip().replace(',', '.'))
                    inicio_leitura = 0
                except: #se não conseguir transformar em decimal, então é um texto (cabrçalho)
                    inicio_leitura = 1 

                #iteração das linhas
                for i in range(inicio_leitura, len(leitor_bruto)):
                    linha = leitor_bruto[i]
                    
                    #testa se tem todos os dados p gerar uma transação(data;conta;tipo;valor;)
                    if len(linha) < 4:
                        continue

                    try:
                        registro = {
                            'data': linha[0].strip(),
                            'conta': linha[1].strip().upper(),
                            'tipo': linha[2].strip().upper(),
                            'valor': Decimal(linha[3].strip().replace(',', '.')),
                            'descricao': linha[4].strip() if len(linha) > 4 else "sem descrição"
                        }
                        dados.append(registro)
                    except Exception as e_linha:
                        print(f"Aviso: Linha {i+1} ignorada por falta de informaçoes")

        except Exception as e:
            print(f"Erro ao processar o arquivo: {e}")
            return []
            
        return dados

    def processar(self):
        transacoes = self.carregar_dados()
        #print(transacoes)
        #iteração entre todos os registros guardados em dados[]
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
            print(f"Movimentação: {conta} {"Débito" if tipo=='D' else "Credito"}, saldo R${self.contas[conta]}")
            print("-"*30)

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

        # Salvar TXT
        caminho_arquivo = os.path.join('.','relatorio.txt')
        os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
        
        with open(caminho_arquivo, 'w') as f:
            f.write(f"Total de Registros Processados: {self.total_registros}\n")
            f.write("--- RELATORIO ---\n")
            f.write(f"Total de Registros Processados: {self.total_registros}\n")
            f.write(f"Total de Creditos: R$ {self.total_creditos}\n")
            f.write(f"Total de Debitos: R$ {self.total_debitos}\n")
            f.write("-" * 30)
            
            f.write("--- SALDOS FINAIS POR CONTA ---\n")
            for conta in sorted(self.contas.keys()):
                saldo = self.contas[conta]
                f.write(f"Conta: {conta} | Saldo: R$ {saldo:.2f}\n")
                
            f.write("-" * 30)
            f.write("\n--- AVISOS ---\n")
            for aviso in self.inconsistencias:
                f.write(f"{aviso}\n") 