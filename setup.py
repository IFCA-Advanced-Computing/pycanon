import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='pycanon',
    version='0.0.1',
    author='Judith sáinz-Pardo Díaz',
    author_email='sainzpardo@ifca.unican.es',
    description='Check anonymization techniques.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.ifca.es/privacy-security/pycanon',
    license='Apache License 2.0',
    packages=['pycanon'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pycanon = pycanon.cli:app',
        ],
    },
    command_options={
        'build_sphinx': {
            'source_dir': ('setup.py', 'doc/source'),
            'build_dir': ('setup.py', 'doc/build'),
            'all_files': ('setyp.py', 1),
        },
    },
)
