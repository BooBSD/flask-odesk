"""
Flask-oDesk
-----------

Adds oDesk API support to Flask.
"""
from setuptools import setup


setup(
    name='Flask-oDesk',
    version='0.1',
    url='https://github.com/BooBSD/flask-odesk',
    license='BSD',
    author='Artem Gnilov',
    author_email='boobsd@gmail.com',
    description='Adds oDesk API support to Flask',
    long_description='',
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'oauth2',
        'python-odesk>=0.4'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
