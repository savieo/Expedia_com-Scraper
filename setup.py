from setuptools import setup
import os

major_version = open('VERSION').read()
minor_version = os.environ.get('CI_PIPELINE_ID', '0')
version = '{}.{}'.format(major_version, minor_version)
project_name = os.environ.get('CI_PROJECT_NAME', 'test_project')
branch_name = os.environ.get('CI_COMMIT_REF_NAME', 'test_branch')
spider_name = '{}_{}'.format(project_name, branch_name)
author_name = os.environ.get('GITLAB_USER_NAME', 'admin')
author_email = os.environ.get('GITLAB_USER_EMAIL', 'admin')
spider_name = project_name if branch_name in ('master') else spider_name

setup(name=spider_name,
      version=version,
      description='spider',
      install_requires=['pyocclient','requests==2.13.0'],
      url='https://code.turbolab.in',
      author=author_name,
      author_email=author_email,
      packages=['2363_Expedia_com'],
      include_package_data=True,
      zip_safe=False)
