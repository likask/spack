##############################################################################
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *


class MofemFractureModule(CMakePackage):
    """mofem fracture module"""

    homepage = "http://mofem.eng.gla.ac.uk"
    git = "https://bitbucket.org/likask/mofem_um_fracture_mechanics.git"

    maintainers = ['likask']

    version('develop', branch='develop')
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
    depends_on('mofem-users-modules@0.8.21:', when='@0.9.52')
    depends_on('mofem-users-modules@0.8.17:', when='@0.9.50')
    depends_on('mofem-users-modules@0.8.16', when='@0.9.49')
    depends_on('mofem-users-modules@0.8.15', when='@0.9.48')
    depends_on("mofem-users-modules", type=('build', 'link', 'run'))

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
            '-DUM_INSTALL_BREFIX=%s' % spec['mofem-users-modules'].prefix,
            '-DEXTERNAL_MODULE_SOURCE_DIRS=%s' % source,
            '-DSTAND_ALLONE_USERS_MODULES=%s' %
            ('YES' if '+copy_user_modules' in spec else 'NO')])

        # Set module version
        if self.spec.version == Version('develop'):
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
