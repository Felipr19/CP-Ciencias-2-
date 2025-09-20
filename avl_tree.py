class NodoAVL:
    def __init__(self, clave):
        self.clave = clave
        self.izquierdo = None
        self.derecho = None
        self.altura = 1

    def __repr__(self):
        return f"NodoAVL({self.clave})"


class ArbolAVL:
    def __init__(self):
        self.raiz = None

#gets
    def obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def obtener_factor_balance(self, nodo):
        if not nodo:
            return 0
        return self.obtener_altura(nodo.izquierdo) - self.obtener_altura(nodo.derecho)

#rotaciones
    def rotar_derecha(self, y):
        x = y.izquierdo
        T2 = x.derecho


        x.derecho = y
        y.izquierdo = T2


        y.altura = 1 + max(self.obtener_altura(y.izquierdo), self.obtener_altura(y.derecho))
        x.altura = 1 + max(self.obtener_altura(x.izquierdo), self.obtener_altura(x.derecho))

        return x

    def rotar_izquierda(self, x):
        y = x.derecho
        T2 = y.izquierdo


        y.izquierdo = x
        x.derecho = T2


        x.altura = 1 + max(self.obtener_altura(x.izquierdo), self.obtener_altura(x.derecho))
        y.altura = 1 + max(self.obtener_altura(y.izquierdo), self.obtener_altura(y.derecho))

        return y

#insercion 
    def insertar(self, clave):
        self.raiz = self._insertar(self.raiz, clave)

    def _insertar(self, nodo, clave):
        if not nodo:
            return NodoAVL(clave)
        elif clave < nodo.clave:
            nodo.izquierdo = self._insertar(nodo.izquierdo, clave)
        elif clave > nodo.clave:
            nodo.derecho = self._insertar(nodo.derecho, clave)
        else:
            return nodo

        # Actualizar altura
        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierdo), self.obtener_altura(nodo.derecho))

        # Obtener factor de balance
        balance = self.obtener_factor_balance(nodo)

        # Caso izquierda-izquierda
        if balance > 1 and clave < nodo.izquierdo.clave:
            return self.rotar_derecha(nodo)

        # Caso derecha-derecha
        if balance < -1 and clave > nodo.derecho.clave:
            return self.rotar_izquierda(nodo)

        # Caso izquierda-derecha
        if balance > 1 and clave > nodo.izquierdo.clave:
            nodo.izquierdo = self.rotar_izquierda(nodo.izquierdo)
            return self.rotar_derecha(nodo)

        # Caso derecha-izquierda
        if balance < -1 and clave < nodo.derecho.clave:
            nodo.derecho = self.rotar_derecha(nodo.derecho)
            return self.rotar_izquierda(nodo)

        return nodo

#eliminacion
    def eliminar(self, clave):
        self.raiz = self._eliminar(self.raiz, clave)

    def _eliminar(self, nodo, clave):
        if not nodo:
            return nodo

        if clave < nodo.clave:
            nodo.izquierdo = self._eliminar(nodo.izquierdo, clave)
        elif clave > nodo.clave:
            nodo.derecho = self._eliminar(nodo.derecho, clave)
        else:
            if nodo.izquierdo is None:
                return nodo.derecho
            elif nodo.derecho is None:
                return nodo.izquierdo

            temp = self._min_valor_nodo(nodo.derecho)
            nodo.clave = temp.clave
            nodo.derecho = self._eliminar(nodo.derecho, temp.clave)

        if not nodo:
            return nodo

        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierdo), self.obtener_altura(nodo.derecho))
        balance = self.obtener_factor_balance(nodo)

#balanceo
        if balance > 1 and self.obtener_factor_balance(nodo.izquierdo) >= 0:
            return self.rotar_derecha(nodo)
        if balance > 1 and self.obtener_factor_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self.rotar_izquierda(nodo.izquierdo)
            return self.rotar_derecha(nodo)
        if balance < -1 and self.obtener_factor_balance(nodo.derecho) <= 0:
            return self.rotar_izquierda(nodo)
        if balance < -1 and self.obtener_factor_balance(nodo.derecho) > 0:
            nodo.derecho = self.rotar_derecha(nodo.derecho)
            return self.rotar_izquierda(nodo)

        return nodo

    def _min_valor_nodo(self, nodo):
        actual = nodo
        while actual.izquierdo:
            actual = actual.izquierdo
        return actual

#busqueda
    def buscar(self, clave):
        return self._buscar(self.raiz, clave)

    def _buscar(self, nodo, clave):
        if nodo is None or nodo.clave == clave:
            return nodo
        if clave < nodo.clave:
            return self._buscar(nodo.izquierdo, clave)
        return self._buscar(nodo.derecho, clave)

#print
    def imprimir(self):
        def _imprimir(nodo, prefijo="", es_izquierdo=True):
            if nodo:
                _imprimir(nodo.derecho, prefijo + "    ", False)
                print(prefijo + ("└── " if es_izquierdo else "┌── ") + f"{nodo.clave} (alt={nodo.altura})")
                _imprimir(nodo.izquierdo, prefijo + "    ", True)
        _imprimir(self.raiz)


#menu
def menu():
    arbol = ArbolAVL()

    while True:
        print("\n--- Menú Árbol AVL ---")
        print("1. Insertar")
        print("2. Eliminar")
        print("3. Buscar")
        print("4. Mostrar árbol")
        print("5. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            clave = int(input("Clave a insertar: "))
            arbol.insertar(clave)
            print("\nÁrbol después de insertar:")
            arbol.imprimir()

        elif opcion == "2":
            clave = int(input("Clave a eliminar: "))
            arbol.eliminar(clave)
            print("\nÁrbol después de eliminar:")
            arbol.imprimir()

        elif opcion == "3":
            clave = int(input("Clave a buscar: "))
            nodo = arbol.buscar(clave)
            if nodo:
                print(f"Clave {clave} encontrada: {nodo}")
            else:
                print(f"Clave {clave} NO encontrada")

        elif opcion == "4":
            print("\nÁrbol actual:")
            arbol.imprimir()

        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción inválida, intenta de nuevo.")


if __name__ == "__main__":
    menu()
