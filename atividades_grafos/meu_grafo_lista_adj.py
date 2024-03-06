from bibgrafo.grafo_lista_adjacencia import GrafoListaAdjacencia
from bibgrafo.grafo_errors import *

class MeuGrafo(GrafoListaAdjacencia):

    def vertices_nao_adjacentes(self):
        '''
        Provê um conjunto de vértices não adjacentes no grafo.
        O conjunto terá o seguinte formato: {X-Z, X-W, ...}
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Um objeto do tipo set que contém os pares de vértices não adjacentes
        '''

        vertices = []
        for vertice in self.vertices:
            for vertice2 in self.vertices:
                if vertice != vertice2 and not self.ha_aresta(vertice.rotulo, vertice2.rotulo) and f'{vertice2.rotulo}-{vertice.rotulo}' not in vertices:
                    vertices.append(f'{vertice.rotulo}-{vertice2.rotulo}')
        return set(vertices)

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

        # Verifica se o vértice existe no grafo
        existe = False
        for vertice in self.vertices:
            if vertice.rotulo == V:
                existe = True
                break
        if not existe:
            raise VerticeInvalidoError(f'O vértice {V} não existe no grafo')
        

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
        existe = False
        for vertice in self.vertices:
            if vertice.rotulo == V:
                existe = True
                break
        if not existe:
            raise VerticeInvalidoError(f'O vértice {V} não existe no grafo')
        
        arestas = []
        for aresta in self.arestas:
            if self.arestas[aresta].v1.rotulo == V or self.arestas[aresta].v2.rotulo == V:
                arestas.append(aresta)

        return set(arestas)
    
    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''
        
        for vertice in self.vertices:
            if self.grau(vertice.rotulo) != len(self.vertices) - 1:
                return False
        return True

    def ha_aresta(self, V1, V2):
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
