from itertools import permutations
from bibgrafo.grafo_lista_adjacencia import GrafoListaAdjacencia
from bibgrafo.grafo_errors import *

class MeuGrafo(GrafoListaAdjacencia):                
    def caminho(self, n):
        '''
            Retorno: Uma lista no formato [v1, a1, v2, a2, v3, a3, ...] onde vx são vértices e ax são arestas ou False se não existir caminho
        '''
        n = n+1
        if n < 2:
            return False    
        
        caminhos = list(permutations(self.vertices, n))
            
        for caminho in caminhos:
            caminho = list(caminho)
            caminho_arestas = []
            for i in range(len(caminho) - 1):
                if not self.tem_aresta(caminho[i].rotulo, caminho[i+1].rotulo):
                    break
                
                ar_1 = list(self.arestas_sobre_vertice(caminho[i].rotulo))
                ar_2 = list(self.arestas_sobre_vertice(caminho[i+1].rotulo))
                
                ar_1.sort()
                ar_2.sort()
                
                for a in ar_1:
                    if a in ar_2:
                        caminho_arestas.append(a)
                        break
            if len(caminho_arestas) == n - 1:
                caminho_final = []
                for i in range(len(caminho)):
                    caminho_final.append(caminho[i].rotulo)
                    if i < len(caminho_arestas):
                        caminho_final.append(caminho_arestas[i])
                return caminho_final
        return False
    
    def conexo(self):
        '''
        Verifica se o grafo é conexo.
        :return: Um valor booleano que indica se o grafo é conexo
        '''
        if len(self.vertices) == 1 and len(self.arestas) == 0:
            return True
        
        for vertice in self.vertices:
            grafo = self.dfs(vertice.rotulo)
            if isinstance(grafo, bool):
                return False
            else:
                if len(grafo.vertices) != len(self.vertices):
                    return False
        return True

    def vertices_nao_adjacentes(self):
        '''
        Provê um conjunto de vértices não adjacentes no grafo.
        O conjunto terá o seguinte formato: {X-Z, X-W, ...}
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Um objeto do tipo set que contém os pares de vértices não adjacentes
        '''

        vertices = set()
        for vertice in self.vertices:
            for vertice2 in self.vertices:
                if vertice != vertice2 and not self.tem_aresta(vertice.rotulo, vertice2.rotulo) and f'{vertice2.rotulo}-{vertice.rotulo}' not in vertices:
                    vertices.add(f'{vertice.rotulo}-{vertice2.rotulo}')
        return vertices

    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        
        for aresta in self.arestas:
            if self.arestas[aresta].v1 == self.arestas[aresta].v2:
                return True
        return False

    def grau(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        '''

        existe = self.existe_rotulo_vertice(V)
        if not existe:
            raise VerticeInvalidoError(f"Vértice {V} não existe no grafo!")

        grau = 0
        for aresta in self.arestas:
            if self.arestas[aresta].v1.rotulo == V:
                grau += 1
            if self.arestas[aresta].v2.rotulo == V:
                grau += 1
        return grau

    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        for aresta in self.arestas:
            for aresta2 in self.arestas:
                # Verifica se as arestas são diferentes
                if aresta != aresta2:
                    if self.arestas[aresta].v1 == self.arestas[aresta2].v1 and self.arestas[aresta].v2 == self.arestas[aresta2].v2:
                        return True
        return False

    def arestas_sobre_vertice(self, V):
        '''
        Provê uma lista que contém os rótulos das arestas que incidem sobre o vértice passado como parâmetro
        :param V: Um string com o rótulo do vértice a ser analisado
        :return: Uma lista os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        
        # Verifica se o vértice existe no grafo
        existe = self.existe_vertice_grafo(V)
        if not existe:
            raise VerticeInvalidoError(f"Vértice {V} não existe no grafo!")
        
        arestas = set()
        for aresta in self.arestas:
            if self.arestas[aresta].v1.rotulo == V or self.arestas[aresta].v2.rotulo == V:
                arestas.add(aresta)
        return arestas
    
    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''
        
        if len(self.vertices_nao_adjacentes()) == 0 and not self.ha_laco() and not self.ha_paralelas():
            return True
        return False

    def tem_aresta(self, V1, V2):
        '''
        Verifica se existe uma aresta entre os vértices V1 e V2
        :param V1: O rótulo do vértice de origem
        :param V2: O rótulo do vértice de destino
        :return: Um valor booleano que indica se existe uma aresta entre os vértices V1 e V2
        :raises: VerticeInvalidoError se algum dos vértices não existir no grafo
        '''
        
        # Verifica se os vértices existem no grafo
        existe1 = False
        existe2 = False
        for vertice in self.vertices:
            if vertice.rotulo == V1:
                existe1 = True
            if vertice.rotulo == V2:
                existe2 = True
        if not existe1:
            raise VerticeInvalidoError(f'O vértice {V1} não existe no grafo')
        if not existe2:
            raise VerticeInvalidoError(f'O vértice {V2} não existe no grafo')
        
        for aresta in self.arestas:
            if (self.arestas[aresta].v1.rotulo == V1 and self.arestas[aresta].v2.rotulo == V2) or (self.arestas[aresta].v1.rotulo == V2 and self.arestas[aresta].v2.rotulo == V1):
                return True
        return False

    def existe_vertice_grafo(self, V):
        # Verifica se o vértice existe no grafo
        existe = False
        for vertice in self.vertices:
            if vertice.rotulo == V:
                existe = True
                break
        return existe

    def dfs(self, V=''):
        if self.existe_rotulo_vertice(V) == False:
            raise VerticeInvalidoError(f"Vértice {V} não existe no grafo!")
        
        grafo = MeuGrafo()
        visitados = set()
        
        def dfs_recursivo(V):
            visitados.add(V)
            grafo.adiciona_vertice(V)
            for aresta in self.arestas:
                if self.arestas[aresta].v1.rotulo == V and self.arestas[aresta].v2.rotulo not in visitados:
                    dfs_recursivo(self.arestas[aresta].v2.rotulo)
                    grafo.adiciona_aresta(aresta, self.arestas[aresta].v1.rotulo, self.arestas[aresta].v2.rotulo)
                if self.arestas[aresta].v2.rotulo == V and self.arestas[aresta].v1.rotulo not in visitados:
                    dfs_recursivo(self.arestas[aresta].v1.rotulo)
                    grafo.adiciona_aresta(aresta, self.arestas[aresta].v2.rotulo, self.arestas[aresta].v1.rotulo)

        dfs_recursivo(V)

        if len(grafo.arestas) == 0:
            return False
        
        return grafo

    def bfs(self, V=''):
        if self.existe_rotulo_vertice(V) == False:
            raise VerticeInvalidoError(f"Vértice {V} não existe no grafo!")
        
        grafo = MeuGrafo()
        visitados = set()
        fila = []
        arestas_visitadas = list()
        
        visitados.add(V)
        fila.append(V)
        
        while fila:
            vertice = fila.pop(0)
            grafo.adiciona_vertice(vertice)
            for aresta in self.arestas:
                if self.arestas[aresta].v1.rotulo == vertice and self.arestas[aresta].v2.rotulo not in visitados:
                    arestas_visitadas.append([aresta, self.arestas[aresta].v1.rotulo, self.arestas[aresta].v2.rotulo])
                    visitados.add(self.arestas[aresta].v2.rotulo)
                    fila.append(self.arestas[aresta].v2.rotulo)
                if self.arestas[aresta].v2.rotulo == vertice and self.arestas[aresta].v1.rotulo not in visitados:
                    arestas_visitadas.append([aresta, self.arestas[aresta].v2.rotulo, self.arestas[aresta].v1.rotulo])
                    visitados.add(self.arestas[aresta].v1.rotulo)
                    fila.append(self.arestas[aresta].v1.rotulo)
        
        if len(arestas_visitadas) == 0:
            return False
        
        for aresta in arestas_visitadas:
            grafo.adiciona_aresta(aresta[0], aresta[1], aresta[2])
        
        return grafo

    def percorrer_grafo(self, inicio=None):
        if inicio is None:
            inicio = self.vertices[0].rotulo

        historia = []
        visitados_set = set()
        arestas_visitadas_set = set()

        def visitar_dfs(atual):
            visitados_set.add(atual)
            if atual not in historia:
                historia.append(atual)

            for aresta in self.arestas:
                if self.arestas[aresta].v1.rotulo == atual and self.arestas[aresta].v2.rotulo not in visitados_set and self.arestas[aresta].rotulo not in arestas_visitadas_set:
                    arestas_visitadas_set.add(aresta)
                    historia.append(self.arestas[aresta].rotulo)
                    visitar_dfs(self.arestas[aresta].v2.rotulo)
                    return

                if self.arestas[aresta].v2.rotulo == atual and self.arestas[aresta].v1.rotulo not in visitados_set and self.arestas[aresta].rotulo not in arestas_visitadas_set:
                    arestas_visitadas_set.add(aresta)
                    historia.append(self.arestas[aresta].rotulo)
                    visitar_dfs(self.arestas[aresta].v1.rotulo)
                    return

                if self.arestas[aresta].v1.rotulo == atual and self.arestas[aresta].v2.rotulo in visitados_set and self.arestas[aresta].rotulo not in arestas_visitadas_set:
                    arestas_visitadas_set.add(aresta)
                    historia.append(self.arestas[aresta].rotulo)
                    historia.append(self.arestas[aresta].v2.rotulo)
                    return

                if self.arestas[aresta].v2.rotulo == atual and self.arestas[aresta].v1.rotulo in visitados_set and self.arestas[aresta].rotulo not in arestas_visitadas_set:
                    arestas_visitadas_set.add(aresta)
                    historia.append(self.arestas[aresta].rotulo)
                    historia.append(self.arestas[aresta].v1.rotulo)
                    return

        visitar_dfs(inicio)

        if historia:
            ultimo = historia[-1]
            i = 0
            while i < len(historia):
                if historia[i] != ultimo:
                    historia.pop(i)
                else:
                    break    

        if len(historia) <= 1:
            return False

        return historia
    
    def ha_ciclo(self):
        caminho = []

        for vertice in self.vertices:
            caminho = self.percorrer_grafo(vertice.rotulo)
            if isinstance(caminho, bool):
                continue
            else:
                if caminho[0] == caminho[-1]:
                    return caminho

        return False
