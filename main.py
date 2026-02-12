from processador import Processador

if __name__ == "__main__":
    arquivo = 'exemplo.csv' #alterar esta variável c/ o caminho do arquivo csv
    
    app = Processador(arquivo)
    app.processar() 
    app.gerar_relatorio()

