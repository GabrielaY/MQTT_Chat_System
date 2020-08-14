from setuptools import setup

setup(
    name='ditto-python-client',
    version='1.0.0',
    packages=['ditto-client'],
    url='ssh://<git-psb-username>@git.psb:12222/com.prosyst.mbs.gateway.containers',
    license='Copyright Bosch.IO GmbH 1997, 2020 All rights reserved, also regarding any disposal, exploitation, '
            'reproduction, editing, distribution, as well as in the event of applications for industrial property '
            'rights. This software is the confidential and proprietary information of Bosch.IO GmbH. You shall not '
            'disclose such Confidential Information and shall use it only in accordance with the terms of the license '
            'agreement you entered into with Bosch.IO GmbH.',
    author='Gabriela Yoncheva, Ognian Baruh',
    author_email='external.Gabriela.Yoncheva@bosch.io, external.Ognian.Baruh@bosch.io',
    install_requires=[
        'google',
        'paho-mqtt',
        'pytest',
    ],
    description='Eclipse Ditto client SDK for Python.'
)
