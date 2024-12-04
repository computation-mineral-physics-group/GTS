# GTS: Gibbs Thermodynamic Surface

![version](https://img.shields.io/badge/version-1.0.0-blue)
![python](https://img.shields.io/badge/python-3.11.4%2B-brightgreen)
![license](https://img.shields.io/badge/license-GPL_3.0-yellow)

## Overview

**GTS: Gibbs Thermodynamic Surface** is an automated toolkit designed for efficiently obtaining high-pressure melting data, including melting points and thermodynamic potentials of materials. By constructing the Gibbs thermodynamic surface using a geometrical method, it provides fast and accurate calculations for both solid and liquid phases.

---

## Features

- **Automated surface generation**: Builds thermodynamic surfaces for solid and liquid phases.
- **Melting data**: Obtaining melting data for solid and liquid phases based on user-defined pressure conditions. With the *ab initio* molecular dynamics (AIMD) simulation data in the NVT (N, number of atoms; V, volume; T, temperature) ensemble and the reference point, GTS is able to rapidly present melting data, including volume, pressure, temperature, and thermodynamic potentials
- **A reference point**: Comparing the traditionally-used Clausius-Clapeyron integration (CCI) method with our GTS approach, the same thing is that a reference melting point is needed.


---

## Installation

Installing GTS in a Python 3 environment is straightforward. We recommend two ways to install GTS:

### From PyPI

You can install GTS directly from PyPI:
      ```
      pip install GTS
      ```

### From Source

1. Clone the repository:
    ```bash
    git clone https://github.com/XuanZhao-study/GTS.git
    cd GTS
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Install GTS:
    ```bash
    pip install .
    ```

---

## Run

GTS provides two primary functions: **building the Gibbs thermodynamic surface** and **calculating melting data**. These functionalities can be accessed via a command-line interface.

### Input Files

It is of great importance to prepare two files before running: `{name}_solid_input.txt`, `{name}_liquid_input.txt`. 



### Command For Running

| Argument                         | Type    | Default         | Description                                                                |
|----------------------------------|---------|-----------------|----------------------------------------------------------------------------|
| `-n, --name`                     | `str`   | None            | The name of the material for which you want to obtain melting data.        |
| `-s, --surface`                  | `bool`  | `False`         | Build the Gibbs thermodynamic surface and store its data in `[name].json`. |
| `-tmr, --temp_melting_refer`     | `float` | `0`             | The reference melting temperature (unit: K).                               |
| `-pmr, --pressure_melting_refer` | `float` | `0`             | The reference melting pressure (unit: GPa).                                |
| `-p, --pressure`                 | `float` | `0`             | The target pressure for melting point calculation (unit: GPa).             |
| `-i, --image`                    | `bool`  | `False`         | Save the G-T plot indicating the melting point.                            |
| `-u, --unit`                     | `str`   | `internal`      | Units defined by the user. (e.g., `vasp` or `internal`).                   |
| `-d, --debug`                    | `bool`  | `False`         | Enable debug mode.                                                         |
| `-v, --version`                  | `flag`  | `VersionAction` | Show the program's version.                                                |

---

## Example Usage

### 1. Generate Thermodynamic Surface
Run the following command to generate the Gibbs thermodynamic surface for the target material and store the data in `[name].json`:

```bash
GTS -n [name] -s -mtr [value] -mpr [value]
```

### 2. Obtain Melting Data
This command will output the user-defined melting point and its thermodynamic potentials for the two phases (solid phase and liquid phase) in the terminal.

```bash
GTS -n [name] -p [value] -u [type] -i
```

### 3. Debug Model
In step 1, GTS retains the original data for building primitive surfaces in two directories: `{name}_solid` and `{name}_liquid`. After entropy calibration, derived surface data is stored in `twophase`.

In step 2, the fitting data of the G-T plot is kept in the directory: `{name}_melting_data`, during obtaining melting data.

---

## Requirements

- **Python version**: 3.11.4 or higher
- **Dependencies**: Listed in `requirements.txt`

---

## Contribution

Contributions are welcome! If you have suggestions or improvements, please feel free to contact us.

---

## License

This project is licensed under the [GNU General Public License v3](LICENSE.txt).

---

## Contact

Authors:  
- **Kun Yin** ([yinkun@cdut.edu.cn](mailto:yinkun@cdut.edu.cn))  
- **Xuan Zhao**










