from setuptools import setup

requires = [
    'pyramid',
]

setup(name='benford_app',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = benford_app:main
      """,
)
