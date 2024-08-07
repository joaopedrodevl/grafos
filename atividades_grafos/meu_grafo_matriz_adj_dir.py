from bibgrafo.grafo_matriz_adj_dir import *
from bibgrafo.grafo_exceptions import *
import heapq

class MeuGrafo(GrafoMatrizAdjacenciaDirecionado):
    def vertices_nao_adjacentes(self):
        '''
        Provê uma lista de vértices não adjacentes no grafo. A lista terá o seguinte formato: [X-Z, X-W, ...]
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Uma lista com os pares de vértices não adjacentes
        '''

        vertices = set()

        for i in range(len(self.arestas)):
            for j in range(len(self.arestas)):
                if i != j and len(self.arestas[i][j]) == 0:
                    vertices.add(self.vertices[i].rotulo + '-' + self.vertices[j].rotulo)

        return vertices


    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''

        for i in range(len(self.arestas)):
            if len(self.arestas[i][i]) != 0:
                return True

        return False


    def grau(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''

        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError(f'O vértice {V} não existe no grafo')

        grau = 0

        for i in range(len(self.vertices)):
            if self.vertices[i].rotulo == V:
                for j in range(len(self.arestas)):
                        grau += len(self.arestas[i][j])

        for i in range(len(self.arestas)):
            if self.vertices[i].rotulo == V:
                for j in range(len(self.arestas)):
                        grau += len(self.arestas[j][i])

        return grau

    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''

        for i in range(len(self.arestas)):
            for j in range(len(self.arestas)):
                if len(self.arestas[i][j]) > 1:
                    return True

        return False

    def arestas_sobre_vertice(self, V):
        '''
        Provê uma lista que contém os rótulos das arestas que incidem sobre o vértice passado como parâmetro
        :param V: O vértice a ser analisado
        :return: Uma lista os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''

        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError(f'O vértice {V} não existe no grafo')

        arestas = set()

        indice = self.indice_do_vertice(self.get_vertice(V))
        for j in range(len(self.arestas)):
            for aresta in self.arestas[indice][j]:
                arestas.add(aresta)

        for i in range(len(self.arestas)):
            if self.vertices[i].rotulo == V:
                for j in range(len(self.arestas)):
                    for aresta in self.arestas[j][i]:
                        arestas.add(aresta)

        return arestas

    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''

        for i in range(len(self.arestas)):
            for j in range(len(self.arestas)):
                if i != j and len(self.arestas[i][j]) == 0:
                    return False

        return True

    def warshall(self):
        '''
        Provê a matriz de alcançabilidade de Warshall do grafo
        :return: Uma lista de listas que representa a matriz de alcançabilidade de Warshall associada ao grafo
        '''

        matriz = []

        for i in range(len(self.arestas)):
            linha = []
            for j in range(len(self.arestas)):
                linha.append(1 if len(self.arestas[i][j]) > 0 else 0)
            matriz.append(linha)

        for k in range(len(self.arestas)):
            for i in range(len(self.arestas)):
                for j in range(len(self.arestas)):
                    matriz[i][j] = matriz[i][j] or (matriz[i][k] and matriz[k][j])

        return matriz

    def dijkstra(self, origem, destino):
        grafo = self

        for n in range(len(grafo.arestas)):
            for m in range(len(grafo.arestas)):
                if n == m:
                    grafo.arestas[n][m] = []

        dijkstra = {}
        w = origem

        for v in grafo.vertices:
            if v.rotulo == origem:
                dijkstra[v.rotulo] = [0, 1, None]
            else:
                dijkstra[v.rotulo] = [float('inf'), 0, None]

        while True:
            visitados = True

            if (w == destino):
                lista = []

                def monta_o_caminho (vertice):
                    if vertice != None:
                        monta_o_caminho(dijkstra[vertice][2])
                        lista.append(vertice)

                monta_o_caminho(destino)

                return lista

            sobre = []
            for i in range(len(grafo.arestas)):
                if len(grafo.arestas[grafo.indice_do_vertice(next(v for v in grafo.vertices if v.rotulo == w))][i]) > 0:
                    sobre.append(grafo.vertices[i].rotulo)

            for i in sobre:
                indice_w = grafo.indice_do_vertice(next(v for v in grafo.vertices if v.rotulo == w))
                indice_i = grafo.indice_do_vertice(next(v for v in grafo.vertices if v.rotulo == i))

                peso = next(iter(grafo.arestas[indice_w][indice_i].values()), None).peso

                if dijkstra[i][0] > dijkstra[w][0] + peso:
                    dijkstra[i][0] = dijkstra[w][0] + peso
                    dijkstra[i][2] = w

            menor = float('inf')

            vis = []

            for chave, valor in dijkstra.items():
                vis.append(w)
                if valor[1] == 0 and valor[0] < menor and chave not in vis:
                    w = chave
                    visitados = False
                    menor = valor[0]

                if len(vis) == len(dijkstra):
                    dijkstra[w][1] = 1
                    break

            if visitados:
                return "Nenhum caminho encontrado!"

grafo = MeuGrafo()
grafo.adiciona_vertice("X")
grafo.adiciona_vertice("Y")
grafo.adiciona_vertice("L")
grafo.adiciona_vertice("M")
grafo.adiciona_vertice("N")
grafo.adiciona_vertice("Z")
grafo.adiciona_vertice("K")
grafo.adiciona_aresta("X-Y", "X", "Y", 1)
grafo.adiciona_aresta("X-M", "X", "M", 3)
grafo.adiciona_aresta("Y-L", "Y", "L", 2)
grafo.adiciona_aresta("Y-K", "Y", "K", 4)
grafo.adiciona_aresta("L-Y", "L", "Y", 3)
grafo.adiciona_aresta("L-M", "L", "M", 5)
grafo.adiciona_aresta("N-L", "N", "L", 4)
grafo.adiciona_aresta("N-X", "N", "X", 2)
grafo.adiciona_aresta("Z-X", "Z", "X", 7)
grafo.adiciona_aresta("Z-Y", "Z", "Y", 4)
grafo.adiciona_aresta("Z-K", "Z", "K", 3)
grafo.adiciona_aresta("Z-L", "Z", "L", 1)
grafo.adiciona_aresta("K-Z", "K", "Z", 1)
grafo.adiciona_aresta("K-L", "K", "L", 3)
print(grafo.dijkstra("X", "L"))
