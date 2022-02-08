# setup.py
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='main_project',
     version='0.1',
     author="Sushant Kumar",
     author_email="sushantkumar23@gmail.com",
     description="An app that analyses your profile to recommend similar people",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/sushantkumar23/twittercloud",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent"
     ]
 )
