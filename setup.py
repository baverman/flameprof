from setuptools import setup, find_packages
import flameprof

setup(
    name='flameprof',
    version=flameprof.version,
    url='https://github.com/baverman/flameprof/',
    license='MIT',
    author='Anton Bobrov',
    author_email='baverman@gmail.com',
    description='cProfile flamegraph generator',
    long_description=open('README.rst').read(),
    py_modules=['flameprof'],
    scripts=['bin/flameprof'],
    entry_points = {
        'console_scripts': ['flameprof=flameprof:main'],
    },
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Monitoring',
    ]
)
