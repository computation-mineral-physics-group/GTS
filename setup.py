"""
  GTS -- Gibbs Thermodynamic Surface: an automated toolkit to obtain high-pressure melting data

  Copyright (C) 2019-2019 by Xuan Zhao

  This program is free software; you can redistribute it and/or modify it under the
  terms of the GNU General Public License as published by the Free Software Foundation
  version 3 of the License.

  This program is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
  PARTICULAR PURPOSE.  See the GNU General Public License for more details.

  E-mail: yinkun@cdut.edu.cn
"""

from setuptools import setup, find_packages
import pathlib

# 读取 README 文件内容
# here = pathlib.Path(__file__).parent.resolve()
# long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="GTS",
    version="1.0.0",
    description="Derivation of melting curve from Gibbs thermodynamic surface for davemaoite.",
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    author="Yin Kun",
    author_email="yinkun@cdut.edu.cn",
    # url="https://example.com/GTS",
    license="GNU General Public License v3.0",
    packages=find_packages(where='lib'),
    package_dir={'': 'lib'},
    py_modules=["gibbs_thermo_surface_01", "gibbs_thermo_surface_02", "gibbs_thermo_surface_03",
                "gibbs_thermo_surface_04", "gibbs_thermo_surface_05", "gibbs_thermo_surface_06",
                "gibbs_thermo_surface_07", "gibbs_thermo_surface_08", "gibbs_surf", "save_json"],
    scripts=["lib/GTS"],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Chemistry',
    ],
    # project_urls={
    #     'Bug Reports': 'https://example.com/GTS/issues',
    #     'Source': 'https://example.com/GTS',
    # },
)
