from setuptools import setup

setup(
    name='DashGourd-Web-Api',
    version='0.1.1',
    url='https://github.com/richard-to/dashgourd',
    author='Richard To',
    description='Example web api for DashGourd using Flask Blueprint',
    platforms='any',
    packages=[
        'dashgourd'
    ],
    namespace_packages=['dashgourd'],    
    include_package_data=True,
    install_requires=[
        'Flask'
    ]    
)
