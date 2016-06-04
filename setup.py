import os.path

from setuptools import setup
from setuptools.command.test import test as TestCommand

here = os.path.dirname(__file__)
readme_path = os.path.join(here, 'README.rst')
readme = open(readme_path).read()

setup(
    name='sphinx-autodoc-napoleon-typehints',
    use_scm_version=True,
    description='Type hints (PEP 484) support for the Sphinx autodoc extension',
    long_description=readme,
    author='Davis Kirkendall',
    author_email='davis.e.kirkendall@gmail.com',
    url='https://github.com/daviskirk/sphinx-autodoc-napoleon-typehints',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Framework :: Sphinx :: Extension',
        'Topic :: Documentation :: Sphinx',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    license='MIT',
    zip_safe=True,
    py_modules=['sphinx_autodoc_napoleon_typehints'],
    setup_requires=[
        'pytest-runner',
        'setuptools_scm >= 1.7.0'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'sphinx-testing',
    ],
    install_requires=[
        'Sphinx >= 1.4',
        'sphinxcontrib-napoleon',
        'typing'
    ]
)
