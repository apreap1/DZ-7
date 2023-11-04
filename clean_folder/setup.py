from setuptools import setup


setup(
      name='clean_folder',
      version='1.1.3',
      description='Clean folder',
      url='https://github.com/apreap1/DZ-7',
      author='Yurii',
      license='MIT',
      entry_points={
          'console_scripts':[
               'clean-folder = clean_folder.clean:main']}
      )

#pip uninstall clean_folder
