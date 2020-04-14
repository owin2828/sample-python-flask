import setuptools

print("==================================")
print(setuptools.find_packages())
print("==================================")


setuptools.setup(
    name="python-flask-sample-app",
    version="0.0.1",
    author="sw_architecture",
    author_email="seungjoon.oh@kt.com",
    description="python flask sample package",
    url="http://10.217.66.21/devops/newdeal-python-flask-sample",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
       'Flask>=0.2',
       'flask-restplus>=0.10',
       'redis>=3.3.1',
       'Werkzeug==0.16.1',
       'pytest>=5.1.1'
    ],
    setup_requires=[
    ],
    scripts=[
    ],
)
