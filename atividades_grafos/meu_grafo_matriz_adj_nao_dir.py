from bibgrafo.grafo_matriz_adj_nao_dir import GrafoMatrizAdjacenciaNaoDirecionado
from bibgrafo.grafo_errors import *

class MeuGrafo(GrafoMatrizAdjacenciaNaoDirecionado):
    def vertices_nao_adjacentes(self):
        '''
        Provê um conjunto (set) de vértices não adjacentes no grafo.
        O conjunto terá o seguinte formato: {X-Z, X-W, ...}
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Um conjunto (set) com os pares de vértices não adjacentes
        '''
        vertices = set()
        
        for vertice in self.vertices:
            for vertice2 in self.vertices:
                if vertice != vertice2 and not self.tem_aresta(vertice.rotulo, vertice2.rotulo) and f'{vertice2}-{vertice}' not in vertices:
                    vertices.add(f'{vertice}-{vertice2}')
        
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
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        '''
        if self.existe_rotulo_vertice(V) == False:
            raise VerticeInvalidoError(f'O vértice {V} não existe no grafo')
        
        grau = 0
        
        # Descobre o grau do vértice
        for v in range(len(self.vertices)):
            if self.vertices[v].rotulo == V:
                for i in range(len(self.arestas[v])-1):
                    if v == i:
                        grau += len(self.arestas[v][i]) * 2
                    else:
                        grau += len(self.arestas[v][i])
        return grau
            
    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        for i in range(len(self.arestas)):
            for j in range(len(self.arestas[i])):
                if len(self.arestas[i][j]) > 1:
                    return True
        return False

    def arestas_sobre_vertice(self, V):
        '''
        Provê um conjunto (set) que contém os rótulos das arestas que
        incidem sobre o vértice passado como parâmetro
        :param V: O vértice a ser analisado
        :return: Um conjunto com os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        '''
        if self.existe_rotulo_vertice(V) == False:
            raise VerticeInvalidoError(f'O vértice {V} não existe no grafo')
        
        arestas = set()
        
        for i in range(len(self.arestas)):
            for j in range(len(self.arestas[i])):
                if len(self.arestas[i][j]) != 0:  
                    if self.vertices[i].rotulo == V:
                        for aresta in self.arestas[i][j]:
                            arestas.add(aresta)
                    if self.vertices[j].rotulo == V:
                        for aresta in self.arestas[i][j]:
                            arestas.add(aresta) 
                            
        return arestas  

    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''
        if not self.ha_laco() and not self.ha_paralelas() and len(self.vertices_nao_adjacentes()) == 0:
            return True
        return False

    def tem_aresta(self, v1, v2):
        '''
        Verifica se existe uma aresta entre os vértices passados como parâmetro
        :param v1: O rótulo do vértice de origem
        :param v2: O rótulo do vértice de destino
        :return: Um valor booleano que indica a existência da aresta
        '''
        
        if self.existe_rotulo_vertice(v1) == False or self.existe_rotulo_vertice(v2) == False:
            return False
        
        for i in range(len(self.arestas)):
            for j in range(len(self.arestas[i])):
                if len(self.arestas[i][j]) != 0:
                    if self.vertices[i].rotulo == v1 and self.vertices[j].rotulo == v2:
                        return True
        return False