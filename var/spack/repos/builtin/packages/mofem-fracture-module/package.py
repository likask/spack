# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class MofemFractureModule(CMakePackage):
    """mofem fracture module"""

    homepage = "http://mofem.eng.gla.ac.uk"
    git = "https://bitbucket.org/likask/mofem_um_fracture_mechanics.git"

    maintainers = ['likask']

    version('develop', branch='develop')
    version('lukasz', branch='lukasz/develop')
    version('0.12.1', branch='Version0.12.0')
    version('0.12.0', branch='Version0.12.0')
    version('0.11.0', branch='Version0.11.0')
    version('0.10.0', branch='Version0.10.0')
    version('0.9.62', branch='Version0.9.62')
    version('0.9.61', tag='v0.9.61-release')
    version('0.9.60', tag='v0.9.60')
    version('0.9.52', tag='v0.9.52')
    version('0.9.51', tag='v0.9.51')
    version('0.9.50', tag='v0.9.50')
    version('0.9.49', tag='v0.9.49')
    version('0.9.48', tag='v0.9.48')
    version('0.9.47', tag='v0.9.47')
    version('0.9.46', tag='v0.9.46')
    version('0.9.45', tag='v0.9.45')
    version('0.9.44', tag='v0.9.44')
    version('0.9.42', tag='v0.9.42')

    variant('copy_user_modules', default=True,
        description='Copy user modules directory instead linking')

    extends('mofem-cephas')
    depends_on('mofem-mortar-contact@0.12.1', when='@0.12.0')
    depends_on('mofem-mortar-contact@0.12.0', when='@0.12.0')
    depends_on('mofem-mortar-contact@0.11.0', when='@0.11.0')
    depends_on('mofem-users-modules@0.12.0', when='@0.12.0')
    depends_on('mofem-users-modules@0.11.0', when='@0.11.0')
    depends_on('mofem-users-modules@0.10.0', when='@0.10.0')
    depends_on('mofem-users-modules@0.9.2', when='@0.9.62')
    depends_on('mofem-users-modules@0.9.1', when='@0.9.61')
    depends_on('mofem-users-modules@0.9.0', when='@0.9.60')
    depends_on('mofem-users-modules@0.8.21:0.8.99', when='@0.9.52')
    depends_on('mofem-users-modules@0.8.17:', when='@0.9.50')
    depends_on('mofem-users-modules@0.8.16', when='@0.9.49')
    depends_on('mofem-users-modules@0.8.15', when='@0.9.48')
    depends_on('mofem-mortar-contact@develop', when='develop')
    depends_on('mofem-mortar-contact@develop', when='lukasz')
    depends_on('mofem-users-modules@develop', when='@develop')
    depends_on('mofem-users-modules@lukasz', when='@lukasz')
    depends_on("mofem-users-modules", type=('build', 'link', 'run'))
    depends_on("mofem-mortar-contact", 
      type=('build', 'link', 'run'), when='@0.10.0')
    depends_on("mofem-mortar-contact", 
      type=('build', 'link', 'run'), when='@develop')
    depends_on("mofem-mortar-contact", 
      type=('build', 'link', 'run'), when='@lukasz')

    # The CMakeLists.txt installed with mofem-cephas package set cmake
    # environment to install extension from extension repository. It searches
    # for modules in user provides paths, for example in Spack source path.Also
    # it finds all cmake exported targets installed in lib directory, which are
    # built with dependent extensions, f.e.mofem - users - modules or others if
    # needed.
    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        spec = self.spec
        return spec['mofem-users-modules'].prefix.users_modules

    def cmake_args(self):
        spec = self.spec
        source = self.stage.source_path

        options = []

        # obligatory options
        options.extend([
            '-DWITH_SPACK=YES',
            '-DEXTERNAL_MODULES_BUILD=YES',
            '-DUM_INSTALL_PREFIX=%s' % spec['mofem-users-modules'].prefix,
            # BREFIX is a spelling bug added here for back compatibility
            '-DUM_INSTALL_BREFIX=%s' % spec['mofem-users-modules'].prefix,
            '-DEXTERNAL_MODULE_SOURCE_DIRS=%s' % source,
            '-DSTAND_ALLONE_USERS_MODULES=%s' %
            ('YES' if '+copy_user_modules' in spec else 'NO')])

        if self.spec.version >= Version('0.10.0') or \
          self.spec.version == Version('develop') or \
          self.spec.version == Version('lukasz'):
            options.extend(
              ['-DMORTAR_CONTACT_INSTALL_PREFIX=%s' % 
              spec['mofem-mortar-contact'].prefix])

        # Set module version
        if self.spec.version == Version('develop') or \
          self.spec.version == Version('lukasz'):
            options.extend([
                '-DFM_VERSION_MAJOR=%s' % 0,
                '-DFM_VERSION_MINOR=%s' % 0,
                '-DFM_VERSION_BUILD=%s' % 0])
        else:
            options.extend([
                '-DFM_VERSION_MAJOR=%s' % self.spec.version[0],
                '-DFM_VERSION_MINOR=%s' % self.spec.version[1],
                '-DFM_VERSION_BUILD=%s' % self.spec.version[2]])

        # build tests
        options.append('-DMOFEM_UM_BUILD_TESTS={0}'.format(
            'ON' if self.run_tests else 'OFF'))

        return options

    # This function is not needed to run code installed by extension, nor in
    # the install process. However, for users like to have access to source
    # code to play, change and make it. Having source code at hand one can
    # compile in own build directory it in package view when the extension is
    # activated.
    @run_after('install')
    def copy_source_code(self):
        source = self.stage.source_path
        prefix = self.prefix
        install_tree(source, prefix.ext_users_modules.fracture_mechanics)
