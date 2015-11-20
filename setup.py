from setuptools import setup

setup(name='LoadPM25',
      version='0.2',
      description='Load PM2.5',
      author='sw',
      author_email='sunwei.r@gmail.com',
      scripts=["src/load_pm25.py"],
      install_requires = [
          'requests>=2.8.0'
      ]
)
