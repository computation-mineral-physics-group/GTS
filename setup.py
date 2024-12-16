"""
  GTS -- Gibbs Thermodynamic Surface: an automated toolkit to obtain high-pressure melting data

  Copyright (C) 2024-2024 by Kun Yin and Xuan Zhao

  This program is free software; you can redistribute it and/or modify it under the
  terms of the GNU General Public License as published by the Free Software Foundation
  version 3 of the License.

  This program is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
  PARTICULAR PURPOSE.  See the GNU General Public License for more details.

  E-mail: yinkun@cdut.edu.cn
"""

from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="GibbsTS",
    version="1.0.0",
    description="GTS: An automated toolkit for building Gibbs thermodynamic surface with application to obtain "
                "high-pressure melting data.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Kun Yin, Xuan Zhao",
    author_email="yinkun@cdut.edu.cn",
    license="GNU General Public License v3.0",
    packages=find_packages(where='lib'),
    package_dir={'': 'lib'},
    py_modules=["gibbs_thermo_surface_01", "gibbs_thermo_surface_02", "gibbs_thermo_surface_03",
                "gibbs_thermo_surface_04", "gibbs_thermo_surface_05", "gibbs_thermo_surface_06",
                "gibbs_thermo_surface_07", "gibbs_thermo_surface_08", "gibbs_surf", "save_json"],
    scripts=["lib/GTS"],
    python_requires='>=3.11.4',
    install_requires=[
        'numpy>=1.24.3',
        'scipy>=1.10.1',
        'matplotlib>=3.7.1',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.11.4',
        'Topic :: Scientific/Engineering :: Physics',
    ],

)
