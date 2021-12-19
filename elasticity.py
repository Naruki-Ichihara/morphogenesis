from dolfin import *
from dolfin_adjoint import *
from morphogenesis.Solvers.AMGsolver import AMG2Dsolver
from morphogenesis.Solvers.SLUDsolver import SLUDsolver
from morphogenesis.Utils.file_io import export_result

#mesh = BoxMesh(
#    MPI.comm_world, Point(0.0, 0.0, 0.0),
#                    Point(20.0, 10.0, 10.0), 40, 20, 20)

mesh = RectangleMesh(MPI.comm_world, Point(0, 0), Point(20, 10), 200, 100)

# Elasticity parameters
E = 1.0e9
nu = 0.3
mu = E/(2.0*(1.0 + nu))
lmbda = E*nu/((1.0 + nu)*(1.0 - 2.0*nu))

# Stress computation
def sigma(v):
    return 2.0*mu*sym(grad(v)) + lmbda*tr(sym(grad(v)))*Identity(len(v))

# Create function space
V = VectorFunctionSpace(mesh, "Lagrange", 1)

# Define variational problem
f = Constant((0, -1e3))
u = TrialFunction(V)
v = TestFunction(V)
a = inner(sigma(u), grad(v))*dx
L = inner(f, v)*dx

# Set up boundary condition on inner surface
def clamped_boundary(x, on_boundary):
    return on_boundary and x[0] < 1e-10

bc = DirichletBC(V, Constant((0, 0)), clamped_boundary)
u = Function(V)

problem = AMG2Dsolver(a, L, [bc])
u = problem.forwardSolve(u, V, True)

export_result(u, 'result/test.xdmf')