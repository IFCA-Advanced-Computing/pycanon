import setuptools

# Passing requirements as file only works on setuptools >= 62.6
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    install_requires=requirements,
)
