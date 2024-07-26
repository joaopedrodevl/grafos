from bibgrafo.grafo_matriz_adj_dir import *
from bibgrafo.grafo_exceptions import *

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