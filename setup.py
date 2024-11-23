from setuptools import setup, find_packages

setup(
    name='groq_transcribe',
    version='0.1.0',
    description='Advanced audio transcription using Groq Cloud API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/groq_transcribe',
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'python-dotenv>=1.0.0'
    ],
    entry_points={
        'console_scripts': [
            'groq-transcribe=groq_transcribe.cli:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia :: Sound/Audio :: Speech'
    ],
    keywords='transcription groq whisper audio speech-to-text',
    python_requires='>=3.8'
)
