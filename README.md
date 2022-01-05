# fenics-optimize
<!-- # Short Description -->

**fenics-optimize** is an add-on module of the [FEniCS computing platform](https://fenicsproject.org/) for multiphysics optimization problems. 

<!-- # Badges -->

[![Github issues](https://img.shields.io/github/issues/Naruki-Ichihara/morphogenesis?style=for-the-badge&logo=appveyor)](https://github.com/Naruki-Ichihara/morphogenesis/issues)
[![Github forks](https://img.shields.io/github/forks/Naruki-Ichihara/morphogenesis?style=for-the-badge&logo=appveyor)](https://github.com/Naruki-Ichihara/morphogenesis/network/members)
[![Github stars](https://img.shields.io/github/stars/Naruki-Ichihara/morphogenesis?style=for-the-badge&logo=appveyor)](https://github.com/Naruki-Ichihara/morphogenesis/stargazers)
[![Github top language](https://img.shields.io/github/languages/top/Naruki-Ichihara/morphogenesis?style=for-the-badge&logo=appveyor)](https://github.com/Naruki-Ichihara/morphogenesis/)
[![Github license](https://img.shields.io/github/license/Naruki-Ichihara/morphogenesis?style=for-the-badge&logo=appveyor)](https://github.com/Naruki-Ichihara/morphogenesis/)

## Motivation and significance

<p align="center">
  <img src="https://user-images.githubusercontent.com/70839257/148230717-e25da51a-3f96-461d-960f-8f22381387fc.png" />
</p>

**fenics-optimize** enables reusable and straightforward UFL coding for physical optimization problems and provides decorators that bridge easily between a fenics calculation chain and optimizers.

## Installation
### Docker

[![dockeri.co](https://dockeri.co/image/ichiharanaruki/fenics-optimize)](https://hub.docker.com/r/ichiharanaruki/fenics-optimize)

Docker enables to build and ship the environment for **fenics-optimize** for almost any platform, e.g., Linux, macOS, or windows.

First, please install Docker. Linux users should follow the [instraction](https://docs.docker.com/get-started/). Mac or Windows users should install the [Docker Desktop](https://www.docker.com/products/docker-desktop), which suits your platform.

Second, clone this repository on your system.
```
git clone https://github.com/Naruki-Ichihara/fenics-optimize.git
```
and move to the docker-compose directory
```
cd morphogenesis/.docker_optimize
```
Then, launch the docker-compose and pull the image from our docker hub.
```
docker-compose up
```
This container will survive until when you stop the container.

### install on your host
First, make sure to install the following dependencies:

* [FEniCS](https://fenicsproject.org/) + [pyadjoint](https://github.com/dolfin-adjoint/pyadjoint)
* [cyipopt](https://github.com/mechmotum/cyipopt)
* [nlopt](https://github.com/stevengj/nlopt/) with python plugin
* [fecr](https://github.com/IvanYashchuk/fecr)

Second, clone this repository on your system and move in this directory.
```
git clone https://github.com/Naruki-Ichihara/fenics-optimize.git && cd fenics-optimize
```
Then, install this repository.
```
pip install .
```

## Example
2-D Poisson topology optimization problem.

First, import `optimize` with `dolfin`, `dolfin-adjoint` and `numpy`.
```python
from dolfin import *
from dolfin_adjoint import *
import optimize as op
import numpy as np
```

Then define the pysical model using the FEniCS with decorator `with_derivative`.

`with_derivative` will wrrap the fenics function to the numpy function and compute Jacobian automatically.

```python
@op.with_derivative([X])
def forward(xs):
    rho = op.helmholtzFilter(xs[0], X, R=r)
    Th = Function(X, name='Temperature')
    u = TrialFunction(X)
    v = TestFunction(X)
    a = inner(grad(u), k(rho)*grad(v))*dx
    L = f*v*dx
    A, b = assemble_system(a, L, bcs)
    Th = op.AMGsolver(A, b).solve(Th, X, False)
    cost = assemble(inner(grad(Th), k(rho)*grad(Th))*dx)
    return cost

@op.with_derivative([X])
def constraint(xs):
    rho_bulk = project(Constant(1.0), X)
    rho_0 = assemble(rho_bulk*dx)
    rho_f = assemble(xs[0]*dx)
    rel = rho_f/rho_0
    return rel - V
```

Finally, optimize the cost function with inequality constraints.

```python
op.MMAoptimize(problemSize, x0, forward, constraint, maxeval=1000, bounds=[0, 1], rel=1e-20)
```

## Contributors

- [Naruki-Ichihara](https://github.com/Naruki-Ichihara)

## References
## Cite
