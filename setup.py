from setuptools import setup

setup(
    name='DashGourd-Web-Api',
    version='0.1.2',
    url='https://github.com/richard-to/dashgourd-web-api',
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
