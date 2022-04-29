import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name = 'check-anonymity',
    version = '0.0.1',
    author = 'Judith sáinz-Pardo Díaz',
    author_email = 'sainzpardo@ifca.unican.es',
    description = 'Check anonymization techniques.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://gitlab.ifca.es/sainzj/check-anonymity',
    license = 'Apache License 2.0',
    packages = ['check-anonymity'],
    install_requires = requirements
)
