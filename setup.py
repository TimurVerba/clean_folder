from setuptools import setup, find_namespace_packages


setup(name='clean_folder',
      version='0.1.1',
      description='Clean folder',
      author='Timur Verba',
      author_email='verba.timur.official@gmail.com',
      license='MIT',
      classifiers=["Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent"],
      packages=find_namespace_packages(),
      entry_points={"console_scripts":['clean_folder = clean_folder.clean:run']}
      # greeting - це команда
      # после = пишем путь к нашему файлу
      # после : пишет название функции
      )