from setuptools import find_packages, setup

package_name = 'amphi_plain_sim'

data_files = []
data_files.append(('share/ament_index/resource_index/packages', ['resource/' + package_name]))
data_files.append(('share/' + package_name + '/launch', ['launch/amphi_launch.py']))
data_files.append(('share/' + package_name + '/worlds', ['worlds/plain_world.wbt']))
data_files.append(('share/' + package_name + '/resource', ['resource/robot.urdf']))
data_files.append(('share/' + package_name + '/worlds/meshes', ['worlds/meshes/body.stl','worlds/meshes/screw_left.stl','worlds/meshes/screw_right.stl']))
data_files.append(('share/' + package_name, ['package.xml']))
setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nonu',
    maintainer_email='ashwinshine.nonu@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'amphi_sim_plain_driver = amphi_plain_sim.amphi_sim_plain_driver:main'
        ],
    },
)
