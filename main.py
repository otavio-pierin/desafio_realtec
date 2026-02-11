from processador import Processador

if __name__ == "__main__":
    arquivo = 'exemplo.csv'
    
    app = Processador(arquivo)
    app.processar() 
    app.gerar_relatorio()

