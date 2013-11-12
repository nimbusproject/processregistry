from setuptools import setup

import sys
version = "0.1"
name = "processregistry"

if float("%d.%d" % sys.version_info[:2]) < 2.6:
    sys.stderr.write("Your Python version %d.%d.%d is not supported.\n" % sys.version_info[:3])
    sys.stderr.write("%s requires Python 2.6 or newer.\n" % (name))
    sys.exit(1)

setup(name=name,
      version=version,
      description='A Prototype Process Registry',
      author='Nimbus Development Team',
      author_email='workspace-user@globus.org',
      url='http://www.nimbusproject.org/',
      keywords="Nimbus",
      long_description="""Some other time""",
      license="Apache2",
      packages=['processregistry', 'processregistry.registry'],
      include_package_data=True,
      package_data={'processregistry': []},
      install_requires=["django >= 1.5", "django-tastypie", "mimeparse"],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: System :: Clustering',
          'Topic :: System :: Distributed Computing',
      ],)
