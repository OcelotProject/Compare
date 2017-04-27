from setuptools import setup
import os

packages = []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('ocelot'):
    # Ignore dirnames that start with '.'
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


setup(
    name='ocelot-compare',
    version="0.1",
    packages=packages,
    author="Chris Mutel",
    author_email="cmutel@gmail.com",
    license=open('LICENSE.txt').read(),
    package_data={'ocelot_compare': package_files(os.path.join('ocelot', 'data'))},
    entry_points = {
        'console_scripts': [
            'ocelot-compare = ocelot_compare.bin.cli:main',
        ]
    },
    install_requires=[
        'appdirs',
        'bw2parameters',
        'docopt',
        'docutils',
        'jinja2',
        'lxml',
        'numpy',
        'pandas',
        'psutil',
        'pyprind',
        'pytest',
        'stats_arrays',
        'toolz',
        'voluptuous',
        'wrapt',
    ],
    url="https://ocelot.space/",
    long_description=open('README.rst').read(),
    description='Comparison tool for Ocelot runs',
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
