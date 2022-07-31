[![Build Status](https://github.com/lsmo-epfl/zeopp-lsmo/workflows/ci/badge.svg)](https://github.com/lsmo-epfl/zeopp-lsmo/actions)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/zeopp-lsmo.svg?style=flat)](https://anaconda.org/conda-forge/zeopp-lsmo)

# Zeo++-LSMO

High-throughput analysis of crystalline porous materials
By Maciej Haranczyk, Chris H Rycroft, Richard L Martin, Thomas F Willems

This repository contains a fork of the original zeo++ code (version 0.3.0) with bug fixes and improvements, maintained by the [Laboratory of Molecular Simulation](http://lsmo.epfl.ch/) at EPFL.
For a list of changes, see the [CHANGELOG.md](./CHANGELOG.md).

Email: mharanczyk@lbl.gov (Zeo++) and chr@alum.mit.edu (Voro++)

## About

Zeo++ is a software package for high-throughput analysis of structure
and topology of crystalline porous materials. For a given material's
structure, the code calculates the geometrical parameters describing
pores. The tool is based on the Voronoi decomposition, which for
a given arrangement of atoms in a periodic domain provides a graph
representation of the void space. The resulting Voronoi network
is analyzed to obtain the diameter of the largest included sphere
and the largest free sphere, which are two geometrical parameters
that are frequently used to describe pore geometry. Accessibility
of nodes in the network is also determined for a given guest molecule
and the resulting information is later used to retrieve dimensionality
of channel systems as well as in Monte Carlo sampling of accessible
surfaces, volumes and pore size distributions.
The code also offers some aids with structure analysis, e.g. MOF open
metal site detection, and simluations, e.g. generation of blocking spheres.

## Installation

The easiest way to install zeo++ is through the [conda](https://docs.conda.io/en/latest/) package manager:

```
conda install -c conda-forge zeopp-lsmo
```


## Compilation - Linux / Mac OS / Windows with Cygwin

The code is written in ANSI C++, and compiles on many system architectures. The
package contains the C++ source code of Zeo++ as well as Voro++ library.
On Linux, Mac OS, and Windows (using Cygwin), the compilation and installed
can be carried out using GNU Make.

#### Step by step compilation

Clone the git repository
```
git clone https://github.com/lsmo-epfl/zeopp-lsmo
cd zeopp-lsmo
```

Download Eigen library v3.2.7 (if not already installed)
```
wget https://gitlab.com/libeigen/eigen/-/archive/3.2.7/eigen-3.2.7.tar.bz2
tar xf eigen-3.2.7.tar.bz2
```

Compile Voro++ library (you may need first to review config.mk file in voro++/ directory; please check Voro++ documentation or
read voro++/README):
```
cd voro++
make
```

Compile Zeo++ code:

```
cd ../zeo++
make
```

This will create `network` binary, the main Zeo++ binary.
Please view the Zeo++ website for instructions, review documentation/README or contact the authors to inquire about otherwise undocumented or custom features.

## Related programs

No external dependencies are required to compile and run the code
(except for the Voro++ library provided with the code), but several
programs may be useful for analyzing the output:

- VMD - molecular visualization package can be used to visualize some of
  characteristics calculated by Zeo++, for example, Voronoi networks,
  Monte Carlo-sampled surface areas and volumes etc. Zeo++ can be called
  from within VMD vis TCl ZeoVis interface (not yet documented, if interested,
  please contact me at mharanczyk@lbl.gov)

- The freeware raytracer POV-Ray (available at www.povray.org) can be used for
  high-quality renderings of the Zeo++/VMD outputs.

- VisIt - powerful visualization package; https://wci.llnl.gov/codes/visit/


## Usage

Zeo++ is released as free software through the Lawrence Berkeley National
Laboratory - a detailed copyright notice is provided below, and the complete
terms of the license can be found in the LICENSE file.

I am very interested to hear from users of Zeo++, so if you find this
useful, please email me at mharanczyk@lbl.gov. Also, if you plan to publish an
academic paper using this software, please consider citing the following
publications:

- Thomas F. Willems, Chris H. Rycroft, Michael Kazi, Juan C. Meza,
  and Maciej Haranczyk, "Algorithms and tools for high-throughput
  geometry-based analysis of crystalline porous materials",
  Microporous and Mesoporous Materials 149 (2012) 134-141

- Richard L. Martin, Berend Smit, Maciej Haranczyk, "Addressing challenges
  of identifying geometrically diverse sets of crystalline porous materials",
  Journal of Chemical Information and Modeling, DOI: 10.1021/ci200386x


The first reference is the main Zeo++ reference describing the idea of
using Voronoi networks in analysis of porous materials. The second reference
describes extensions allowing sampling of structures from a database of
porous materials using divrsity-based selelction.

## Development

Before making changes to the code, please install the pre-commit hooks for automatic code formatting and linting:
```
pip install pre-commit
pre-commit install
```

## Copyright Notice

Zeo++, Copyright (c) 2011, The Regents of the
University of California, through Lawrence Berkeley National
Laboratory (subject to receipt of any required approvals from the U.S.
Dept. of Energy).  All rights reserved.

If you have questions about your rights to use or distribute this
software, please contact Berkeley Lab's Technology Transfer Department
at  TTD@lbl.gov.

NOTICE.  This software was developed under partial funding from the
U.S. Department of Energy.  As such, the U.S. Government has been
granted for itself and others acting on its behalf a paid-up,
nonexclusive, irrevocable, worldwide license in the Software to
reproduce, prepare derivative works, and perform publicly and display
publicly.  Beginning five (5) years after the date permission to
assert copyright is obtained from the U.S. Department of Energy, and
subject to any subsequent five (5) year renewals, the U.S. Government
is granted for itself and others acting on its behalf a paid-up,
nonexclusive, irrevocable, worldwide license in the Software to
reproduce, prepare derivative works, distribute copies to the public,
perform publicly and display publicly, and to permit others to do so.


## Acknowledgements

This work was supported by the U.S. Department of Energy under
contract DE-AC02-05CH11231 and through SciDAC project #CSNEW918
entitled “Knowledge guided screening tools for identification
of porous materials for CO2 separations”.
