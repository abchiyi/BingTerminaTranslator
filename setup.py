import setuptools

import os
setuptools.setup(
    # 从 git 中获取版本，以最后一个版本号作为打包发布的版本号
    version=os.popen('git tag').read().split()[-1],
)
