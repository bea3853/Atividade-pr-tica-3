import random

linhas = 10   
colunas = 10  

def custo_do_caminho(linhas_caminho):
    custo = 0
    for i in range(colunas-1):
        custo += 1 + abs(linhas_caminho[i+1] - linhas_caminho[i])
    return custo

def aptidao(linhas_caminho):
    return 1.0 / (1.0 + custo_do_caminho(linhas_caminho))

def caminho_aleatorio_valido(inicio, fim):
    linhas_caminho = [None]*colunas
    linhas_caminho[0] = inicio
    linhas_caminho[-1] = fim
   
    for i in range(1, colunas-1):
        anterior = linhas_caminho[i-1]
        candidatos = [anterior]
        if anterior-1 >= 0: candidatos.append(anterior-1)
        if anterior+1 < linhas: candidatos.append(anterior+1)
        linhas_caminho[i] = random.choice(candidatos)

    for i in range(colunas-1):
        if abs(linhas_caminho[i+1]-linhas_caminho[i]) > 1:
            sinal = 1 if linhas_caminho[i+1] > linhas_caminho[i] else -1
            linhas_caminho[i+1] = linhas_caminho[i] + sinal
    return linhas_caminho

def reparar(linhas_caminho):
    for i in range(colunas-1):
        if linhas_caminho[i+1] is None:
            linhas_caminho[i+1] = linhas_caminho[i]
        if abs(linhas_caminho[i+1] - linhas_caminho[i]) > 1:
            sinal = 1 if linhas_caminho[i+1] > linhas_caminho[i] else -1
            linhas_caminho[i+1] = linhas_caminho[i] + sinal
    for i in range(colunas-2, -1, -1):
        if abs(linhas_caminho[i+1] - linhas_caminho[i]) > 1:
            sinal = 1 if linhas_caminho[i] > linhas_caminho[i+1] else -1
            linhas_caminho[i] = linhas_caminho[i+1] + sinal
    for i in range(colunas):
        linhas_caminho[i] = max(0, min(linhas-1, linhas_caminho[i]))
    return linhas_caminho

def cruzamento(pai_a, pai_b):
    ponto = random.randint(1, colunas-2)
    filho = pai_a[:ponto] + pai_b[ponto:]
    filho[0], filho[-1] = pai_a[0], pai_a[-1]
    filho = reparar(filho)
    return filho

def mutar(individuo, taxa_mutacao=0.05):
    filho = individuo[:]
    for i in range(1, colunas-1):
        if random.random() < taxa_mutacao:
            anterior, proximo = filho[i-1], filho[i+1]
            opcoes = []
            for candidato in (filho[i]-1, filho[i], filho[i]+1):
                if 0 <= candidato < linhas and abs(candidato - anterior) <= 1 and abs(proximo - candidato) <= 1:
                    opcoes.append(candidato)
            if opcoes:
                filho[i] = random.choice(opcoes)
            else:
                possibilidades = [anterior]
                if anterior-1 >= 0: possibilidades.append(anterior-1)
                if anterior+1 < linhas: possibilidades.append(anterior+1)
                filho[i] = random.choice(possibilidades)
    filho = reparar(filho)
    return filho

def algoritmo_genetico(linha_inicio, linha_fim, tamanho_populacao=100, geracoes=400, prob_cruzamento=0.8, taxa_mutacao=0.05):
    populacao = [caminho_aleatorio_valido(linha_inicio, linha_fim) for _ in range(tamanho_populacao)]

    for individuo in populacao:
        individuo[0], individuo[-1] = linha_inicio, linha_fim
    melhor = min(populacao, key=custo_do_caminho)
    melhor_custo = custo_do_caminho(melhor)
    
    for geracao in range(geracoes):
        nova_populacao = []
        nova_populacao.append(melhor[:])
        
        while len(nova_populacao) < tamanho_populacao:
            def torneio():
                a, b, c = random.sample(populacao, 3)
                return min([a, b, c], key=custo_do_caminho)
            
            a = torneio()
            b = torneio()
            
            if random.random() < prob_cruzamento:
                filho = cruzamento(a, b)
            else:
                filho = a[:]
            
            filho = mutar(filho, taxa_mutacao)
            filho[0], filho[-1] = linha_inicio, linha_fim
            nova_populacao.append(filho)
        
        populacao = nova_populacao
        melhor_atual = min(populacao, key=custo_do_caminho)
        custo_atual = custo_do_caminho(melhor_atual)
        
        if custo_atual < melhor_custo:
            melhor, melhor_custo = melhor_atual[:], custo_atual
      
        if geracao % 50 == 0:
            print(f"geração {geracao} melhor_custo = {melhor_custo}")
    
    return melhor, melhor_custo

if __name__ == "__main__":
    inicio, fim = 4, 0  
    solucao, custo = algoritmo_genetico(inicio, fim, tamanho_populacao=150, geracoes=400)
    print("custo:", custo)
    print("caminho:", solucao)
