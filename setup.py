from setuptools import setup

setup(name='parking_classifier',
      version='0.1.0',
      install_requires=[
        "Click==7.0",
        "Flask==1.1.1",
        "itsdangerous==1.1.0",
        "Jinja2==2.10.3",
        "MarkupSafe==1.1.1",
        "numpy==1.18.1",
        "opencv-python==4.1.2.30",
        "Werkzeug==0.16.0"
      ],
      packages=['src', 'src.classes', 'src.utils'],
      entry_points={
          'console_scripts': [
              'parking_classifier = src.__main__:app.run'
          ]
      },
      )