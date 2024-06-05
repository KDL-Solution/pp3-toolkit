import setuptools

install_requires = [
    'requests==2.32.2',
    'pillow==10.3.0',
    'requests_toolbelt==1.0.0'
]

# 안전하게 README 파일 읽기
def read_long_description():
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Long description could not be read from README.md"
    
setuptools.setup(
    name="pp3", # 모듈 이름
    use_scm_version=True,
    packages = setuptools.find_packages(), # 패키지 폴더에 있는 모든 모듈을 자동으로 찾아준다.
    author="Kai", # 제작자
    author_email="koreadeep19@gmail.com", # contact
    description="koreadep play-polyground api toolkit", # 모듈 설명
    long_description=read_long_description(), # README.md에 보통 모듈 설명을 해놓는다.
    long_description_content_type="text/markdown",
    url="https://github.com/KDL-Solution/PP3Toolkit",
    install_requires=install_requires,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    python_requires=">=3.8"
)
