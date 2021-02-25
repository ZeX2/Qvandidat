import sympy
from sympy.physics.quantum import TensorProduct

Z = sympy.Matrix([[1, 0],
                  [0, -1]])

H1 = (1/sympy.sqrt(2))*sympy.Matrix([[1, 1],
                                     [1, -1]])
H2 = (1/2)*sympy.Matrix([[1, 1, 1, 1],
                         [1, -1, 1, -1],
                         [1, 1, -1, -1],
                         [1, -1, -1, 1]])

t = sympy.Symbol('t')
Rx = sympy.Matrix([[sympy.cos(t/2),-1*sympy.I*sympy.sin(t/2)],
                   [-1*sympy.I*sympy.sin(t/2), sympy.cos(t/2)]])

Rz = sympy.Matrix([[sympy.exp(-1*sympy.I*t/2), 0],
                   [0, sympy.exp(1*sympy.I*t/2)]])

CX = sympy.Matrix([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 0, 1],
                   [0, 0, 1, 0]])

CZ = sympy.Matrix([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, -1]])

#gate = TensorProduct(H1, Rx)*CZ*TensorProduct(sympy.eye(2), H1)

ZZ = sympy.exp((-1*sympy.I*t/2)*TensorProduct(Z,Z))
print(ZZ)

gate = TensorProduct(sympy.eye(2), H1)*CZ*TensorProduct(sympy.eye(2), Rx)*CZ*TensorProduct(sympy.eye(2), H1)
gate.simplify()
print(gate)

ZZ = CX*TensorProduct(sympy.eye(2), Rz)*CX
print(ZZ)
