from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='ntlmrecon',  # Required

    version='0.4b0',  # Required

    description='A tool to enumerate information from NTLM authentication enabled web endpoints',  # Optional

    long_description=long_description,  # Optional

    long_description_content_type='text/markdown',  # Optional (see note above)

    url='https://github.com/sachinkamath/ntlmrecon',  # Optional

    # This should be your name or the name of the organization which owns the
    # project.
    author='Sachin S Kamath (@sachinkamath)',  # Optional

    # This should be a valid email address corresponding to the author listed
    # above.
    author_email='mail@skamath.me',  # Optional

    keywords='security recon redteam cybersecurity ntlm ntlmrecon',  # Optional

    package_dir={'': 'src'},

    packages=find_packages(where='src'),  # Required

    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',

    install_requires=['requests', 'colorama', 'termcolor', 'iptools'],  # TODO

    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': [
            'ntlmrecon=ntlmrecon:main',
        ],
    },

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/sachinkamath/ntlmrecon/issues',
        'Source': 'https://github.com/sachinkamath/ntlmrecon/',
    },
)

