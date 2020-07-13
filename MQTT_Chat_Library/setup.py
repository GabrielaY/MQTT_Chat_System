from setuptools import setup

setup(
    name='mqtt-chat-library',
    version='1.0.3',
    packages=['mqtt_chat_library'],
    url='https://   github.com/GabrielaY/MQTT_Chat_System',
    license='Copyright (c) 2018 The Python Packaging Authority  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.',
    author='Gabriela & Ognian',
    author_email='',
    install_requires=[
        'google',
        'paho-mqtt',
        'protobuf'
    ],
    description='An MQTT based chat system for communication between a Python Application and a Java Application. The project features a Python Client, Java Client and an Admin Client. The Python and Java Clients can communicate using messages while the Admin Client keeps logs of connects and disconnects to the /chat/messages topic.'
)
