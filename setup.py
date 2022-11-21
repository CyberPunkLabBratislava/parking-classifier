from setuptools import setup

setup(name='parking_classifier',
      version='0.1.0',
      install_requires=[
        "Click==7.0",
        "Flask==1.1.1",
        "itsdangerous==1.1.0",
        "Jinja2==2.10.3",
        "MarkupSafe==1.1.1",
        "opencv-python==4.1.2.30",
        "numpy==1.18.1",
        "pandas==0.25.3",
        "Werkzeug==0.16.0",
        "pillow==7.0.0",
        "tensorflow==2.9.3",
        "uWSGI==2.0.18"
      ],
      packages=['src', 'src.classes', 'src.utils', 'src.api'],
      entry_points={
          'console_scripts': [
              'parking_classifier = src.__main__:app.run'
          ]
      },
      )