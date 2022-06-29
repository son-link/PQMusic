from setuptools import setup

setup(
    name="pqmusic",
    version="1.1.0",
    description="A minimal music player.",
    author="Alfonso Saavedra 'Son Link'",
    author_email='sonlink.dourden@gmail.com',
    license="GPL 3.0",
    url="https://github.com/son-link/PQMusic",
    scripts=['bin/pqmusic'],
    packages=['PQMusic'],
    package_dir={'PQMusic': 'PQMusic'},
    package_data={'PQMusic': ['*', 'locales/*.qm', 'ui/*.py', 'LICENSE']},
    include_package_data=True,
    exclude_package_data={
        '/': [
            'build-appimage.sh',
            'build/',
            'dist/',
            'icons/luv-icon-theme'
        ]
    },
    download_url='https://github.com/son-link/PQMusic/archive/refs/tags/v.0.3.0.tar.gz',
    keywords=['music', 'audio', 'player'],
    install_requires=[
        'pyqt5',
        'mutagen',
        'python-magic',
        'psutil'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: Qt',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Players',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent'
    ],
)
