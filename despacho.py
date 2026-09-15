class _Node:
    __slots__ = ('code', 'prev', 'next', 'in_queue')

    def __init__(self, code: str):
        self.code = code
        self.prev = None
        self.next = None
        self.in_queue = True


def despachar(log: list[str]) -> list[str]:
    head = _Node("")
    tail = _Node("")
    head.next = tail
    tail.prev = head

    nodes: dict[str, _Node] = {}
    entregues: list[str] = []
    undo_stack: list[tuple[str, _Node]] = []

    for raw_line in log:
        idx = raw_line.find('#')
        line = raw_line[:idx] if idx != -1 else raw_line
        s = line.strip()
        if not s:
            continue

        first_char = s[0]

        if first_char == '+':
            cmd = 'CHEGA'
            arg = s[1:].strip().upper()
        elif first_char == '-':
            cmd = 'CANCELA'
            arg = s[1:].strip().upper()
        elif first_char == '>':
            cmd = 'SAI'
            arg = ''
        elif first_char == '<':
            cmd = 'DESFAZ'
            arg = ''
        else:
            parts = s.split(None, 1)
            op = parts[0].upper()
            if op == 'CHEGA':
                cmd = 'CHEGA'
                arg = parts[1].strip().upper() if len(parts) > 1 else ''
            elif op == 'SAI':
                cmd = 'SAI'
                arg = ''
            elif op == 'CANCELA':
                cmd = 'CANCELA'
                arg = parts[1].strip().upper() if len(parts) > 1 else ''
            elif op == 'DESFAZ':
                cmd = 'DESFAZ'
                arg = ''
            else:
                continue

        # Regra 1: Chegada
        if cmd == 'CHEGA':
            if not arg or arg in nodes:
                continue
            node = _Node(arg)
            prev_node = tail.prev
            prev_node.next = node
            node.prev = prev_node
            node.next = tail
            tail.prev = node

            nodes[arg] = node
            undo_stack.append(('CHEGA', node))

        # Regra 2: Saída
        elif cmd == 'SAI':
            if head.next is tail:
                continue  # Fila vazia
            node = head.next
            head.next = node.next
            node.next.prev = head
            node.in_queue = False

            entregues.append(node.code)
            undo_stack.append(('SAI', node))

        # Regra 3: Cancelamento
        elif cmd == 'CANCELA':
            node = nodes.get(arg)
            if node is None or not node.in_queue:
                continue
            node.prev.next = node.next
            node.next.prev = node.prev
            node.in_queue = False

            undo_stack.append(('CANCELA', node))

        # Regra 4: Desfazer
        elif cmd == 'DESFAZ':
            if not undo_stack:
                continue
            last_cmd, node = undo_stack.pop()

            if last_cmd == 'CHEGA':
                node.prev.next = node.next
                node.next.prev = node.prev
                node.in_queue = False
                del nodes[node.code]

            elif last_cmd == 'SAI':
                entregues.pop()
                node.prev.next = node
                node.next.prev = node
                node.in_queue = True

            elif last_cmd == 'CANCELA':
                node.prev.next = node
                node.next.prev = node
                node.in_queue = True

    return entregues
