# The Manual for How to Use Convolution & Elliptic Solver
This is the technical introduction for the concept and my source code of convolution & elliptic solver. Both of them are important idea in my work (see KKW2024).
Before diving into technical details about source code, here I will quickly introduce you their concepts and purposes using them. Then, the structure of the source code will be illustrated to make you quickly get started.
Note that convolution and elliptic solver are not dependent to each other. So, you can skip one of them.

## Concept
In KKW2024, we demonstrate that the nonlocal effect (Kuo and Neelin, 2022) can be applied to a more realistic large eddy simulation. To be simplistic, we demonstrated that, for deep convective cloud, the forcing structures (e.g. buoyancy, dynamic-related terms) that are smaller than 3 km scale will not affect the entire vertical acceleration profiles too much. To prove this, our study use "convolution" to distinguish large and small scales of forcing structures and use "elliptic solver" to obtain vertical acceleration.

### Convolution

### Elliptic Solver


## Source Code
### Prerequisite Knowledge

### Convolution

### Elliptic Solver
