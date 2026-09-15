def despachar(log: list[str]) -> list[str]:
    # Ponteiros da fila dupla usando dicionários (sentinelas HEAD e TAIL)
    prox = {'HEAD': 'TAIL'}
    ant = {'TAIL': 'HEAD'}

    pedidos_registrados = set()
    pedidos_na_fila = set()
    entregues = []
    pilha_desfazer = []

    for linha in log:
        # Remove comentários inline e espaços
        idx = linha.find('#')
        if idx != -1:
            linha = linha[:idx]
        tokens = linha.split()
        if not tokens:
            continue

        primeiro = tokens[0]

        # Normaliza os comandos das versões 1 (+, -, >, <) e 2
        if primeiro.startswith('+'):
            cmd = 'CHEGA'
            codigo = (tokens[1] if primeiro == '+' and len(tokens) > 1 else primeiro[1:]).upper()
        elif primeiro.startswith('-'):
            cmd = 'CANCELA'
            codigo = (tokens[1] if primeiro == '-' and len(tokens) > 1 else primeiro[1:]).upper()
        elif primeiro == '>':
            cmd = 'SAI'
            codigo = ''
        elif primeiro == '<':
            cmd = 'DESFAZ'
            codigo = ''
        else:
            cmd = primeiro.upper()
            codigo = tokens[1].upper() if len(tokens) > 1 else ''

        # Regra 1: Chegada
        if cmd == 'CHEGA':
            if not codigo or codigo in pedidos_registrados:
                continue
            pedidos_registrados.add(codigo)
            pedidos_na_fila.add(codigo)

            # Insere no fim da fila em O(1)
            ultimo = ant['TAIL']
            prox[ultimo] = codigo
            ant[codigo] = ultimo
            prox[codigo] = 'TAIL'
            ant['TAIL'] = codigo

            pilha_desfazer.append(('CHEGA', codigo))

        # Regra 2: Saída
        elif cmd == 'SAI':
            if prox['HEAD'] == 'TAIL':
                continue  # Fila vazia
            codigo = prox['HEAD']
            prox['HEAD'] = prox[codigo]
            ant[prox[codigo]] = 'HEAD'
            pedidos_na_fila.remove(codigo)

            entregues.append(codigo)
            pilha_desfazer.append(('SAI', codigo))

        # Regra 3: Cancelamento
        elif cmd == 'CANCELA':
            if codigo not in pedidos_na_fila:
                continue
            pedidos_na_fila.remove(codigo)
            # Remove da fila mantendo referências salvas em ant e prox
            prox[ant[codigo]] = prox[codigo]
            ant[prox[codigo]] = ant[codigo]

            pilha_desfazer.append(('CANCELA', codigo))

        # Regra 4: Desfazer
        elif cmd == 'DESFAZ':
            if not pilha_desfazer:
                continue
            acao, codigo = pilha_desfazer.pop()

            if acao == 'CHEGA':
                prox[ant[codigo]] = prox[codigo]
                ant[prox[codigo]] = ant[codigo]
                pedidos_na_fila.remove(codigo)
                pedidos_registrados.remove(codigo)

            elif acao == 'SAI':
                entregues.pop()
                # Devolve ao início da fila
                prox[codigo] = prox['HEAD']
                ant[codigo] = 'HEAD'
                ant[prox['HEAD']] = codigo
                prox['HEAD'] = codigo
                pedidos_na_fila.add(codigo)

            elif acao == 'CANCELA':
                # Reconecta na posição original
                prox[ant[codigo]] = codigo
                ant[prox[codigo]] = codigo
                pedidos_na_fila.add(codigo)

    return entregues
