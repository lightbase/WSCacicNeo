import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()

requires = [
    'SQLAlchemy',
    'psycopg2',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'pyramid_chameleon',
    'bcrypt',
    # 'lbauth',
    'pyramid',
    'pyramid_restler',
    'pyramid_who',
    'requests',
    'waitress',
    #'liblightbase',
    'pyramid_beaker'
]

setup(name='WSCacicNeo',
      version='1.0.1b',
      description='WSCacicNeo',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='wscacicneo',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = wscacicneo:main
      [console_scripts]
      initialize_WSCacicNeo_db = wscacicneo.scripts.initializedb:main
      """,
      )
