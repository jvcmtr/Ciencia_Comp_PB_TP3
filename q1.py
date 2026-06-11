class Node:
    def __init__(self, key, val):
        self.key = key
        self.value = val
        self.l = None
        self.r = None
        self.altura = 1 


class ArvoreBusca:
    def __init__(self):
        self.raiz = None
        self.total_itens = 0

    # Questao 1.6 : Altura
    def height(self):
        return self._height(self.raiz)

    # Questao 1.1 : Inserir
    def insert(self, key, valor):
        key = key.lower()
        if not self._find(self.raiz, key):
            self.total_itens += 1
        self.raiz = self._insert(self.raiz, key, valor)

    # Questao 1.2 : Busca
    def find(self, key):
        node = self._find(self.raiz, key.lower())
        return node.value if node else None

    # Questao 1.3 : Listagem
    def list_all(self):
        return  self._list(self.raiz)

    # Questao 1.4
    def remove(self, key):
        key = key.lower()
        if self._find(self.raiz, key):
            self.raiz = self._remove(self.raiz, key)
            self.total_itens -= 1
        else:
            raise ValueError(f"Chave {key} não encontrada")

    # PRIVATE IMPLEMENTATIONS:

    def _insert(self, node, key, valor):
        
        if not node:
            return Node(key, valor)

        if key < node.key:
            node.l = self._insert(node.l, key, valor)
        elif key > node.key:
            node.r = self._insert(node.r, key, valor)
        else:
            node.value = valor
            return node

        node.altura = max(self._height(node.l), self._height(node.r)) + 1
        balanceamento = self._fator_balanceamento(node)

        if balanceamento > 1 and key < node.l.key:
            return self._rotacao_direita(node)

        if balanceamento < -1 and key > node.r.key:
            return self._rotacao_esquerda(node)

        if balanceamento > 1 and key > node.l.key:
            node.l = self._rotacao_esquerda(node.l)
            return self._rotacao_direita(node)

        if balanceamento < -1 and key < node.r.key:
            node.r = self._rotacao_direita(node.r)
            return self._rotacao_esquerda(node)

        return node

    def _find(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._find(node.l, key)
        return self._find(node.r, key)

    def _list(self, node):
        if not node:
            return [] 
        return [
            *self._list(node.l),
            f"{node.key.capitalize()}\t:\t{node.value}",
            *self._list(node.r)
        ]

    def _get_valor_minimo(self, node):
        atual = node
        while atual.l is not None:
            atual = atual.l
        return atual

    def _remove(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.l = self._remove(node.l, key)
        elif key > node.key:
            node.r = self._remove(node.r, key)
        else:
            if node.l is None:
                temp = node.r
                node = None
                return temp
            elif node.r is None:
                temp = node.l
                node = None
                return temp

            temp = self._get_valor_minimo(node.r)
            node.key = temp.key
            node.value = temp.value

            node.r = self._remove(node.r, temp.key)

        if not node:
            return node

        node.altura = max(self._height(node.l), self._height(node.r)) + 1

        balanceamento = self._fator_balanceamento(node)


        if balanceamento > 1 and self._fator_balanceamento(node.l) >= 0:
            return self._rotacao_direita(node)

 
        if balanceamento > 1 and self._fator_balanceamento(node.l) < 0:
            node.l = self._rotacao_esquerda(node.l)
            return self._rotacao_direita(node)


        if balanceamento < -1 and self._fator_balanceamento(node.r) <= 0:
            return self._rotacao_esquerda(node)


        if balanceamento < -1 and self._fator_balanceamento(node.r) > 0:
            node.r = self._rotacao_direita(node.r)
            return self._rotacao_esquerda(node)

        return node


   
    def _height(self, node):
        return node.altura if node else 0

    def _fator_balanceamento(self, node):
        return self._height(node.l) - self._height(node.r) if node else 0

    def _rotacao_direita(self, node ):
        foo = node.l
        foo.r, node.l = node, foo.r

        node.altura = max(self._height(node.l), self._height(node.r)) + 1
        foo.altura = max(self._height(foo.l), self._height(foo.r)) + 1
        return foo

    def _rotacao_esquerda(self, node):
        foo = node.r
        foo.l, node.r = node, foo.l

        node.altura = max(self._height(node.l), self._height(node.r)) + 1
        foo.altura = max(self._height(foo.l), self._height(foo.r)) + 1
        return foo
    
     # questão 1.6
    def __len__(self):
        return self.total_itens



if __name__ == "__main__":
    dict = {
        "Joao Victor Cicero" : "Quem está fazendo o trabalho", 
        "Ciência da Computação" : "Nome do bloco",
        "Teste de Performance 3" : "Trabalho a ser entregue",
    }

    t = ArvoreBusca()

    print("\n_____________________________________")
    print("\t + Inserindo itens")
    for k, v in dict.items():
        t.insert(k, v)
    print("\t + Lendo itens inseridos")
    for i in t.list_all():
        print(i)

    print("\n_____________________________________")
    print(f"\t + Total de itens armazenados: {len(t)}")
    print(f"\t + Altura atual da árvore: {t.height()}")  #


    print("\n_____________________________________")
    k, v = "Projeto de Bloco" , "Nome da disciplina"
    print(f"\t + Inserindo novo item : '{k}' : '{v}'")
    t.insert(k, v)

    print("\t + Lendo itens inseridos novamente")
    for i in t.list_all():
        print(i)