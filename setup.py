from distutils.core import setup

setup(name='pysztaki',
      version='0.2',
      description='Translator script for console using the szotar.sztaki.hu database',
      long_description=open('README.md').read(),
      license = "BSD 3-Clause License",
      author='György Orosz, Daniel Pek',
      author_email='oroszgy@gmail.com',
      url='https://github.com/oroszgy/pysztaki',
      scripts=['sztaki.py'],
      packages=['pysztaki'],
     )
