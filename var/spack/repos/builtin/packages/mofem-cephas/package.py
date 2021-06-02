# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class MofemCephas(CMakePackage):
    """MoFEM is finite element core library"""

    homepage = "http://mofem.eng.gla.ac.uk"
    git = "https://bitbucket.org/likask/mofem-cephas.git"

    maintainers = ['likask']

    version('develop', branch='develop')
    version('lukasz', branch='lukasz/develop')
    version('0.12.0', branch='Version0.12.0')
    version('0.11.1', branch='Version0.11.1')
    version('0.11.0', branch='Version0.11.0')
    version('0.10.0', branch='Version0.10.0')
    version('0.9.2', branch='Version0.9.2')
    version('0.9.1', tag='v0.9.1-release')
    version('0.9.0', tag='v0.9.0')
    version('0.8.23', tag='v0.8.23')
    version('0.8.22', tag='v0.8.22')
    version('0.8.21', tag='v0.8.21')
    version('0.8.20', tag='v0.8.20')
    version('0.8.19', tag='v0.8.19')
    version('0.8.18', tag='v0.8.18')
    version('0.8.17', tag='v0.8.17')
    version('0.8.16', tag='v0.8.16')
    version('0.8.15', tag='v0.8.15')
    version('0.8.14', tag='v0.8.14')
    version('0.8.13', tag='v0.8.13')
    version('0.8.12', tag='v0.8.12')
    version('0.8.11', tag='v0.8.11')
    version('0.8.10', tag='v0.8.10')
    version('0.8.9', tag='v0.8.9')
    version('0.8.8', tag='v0.8.8')
    version('0.8.7', tag='v0.8.7')

    # This option can be only used for development of core lib
    variant('install_id', values=int, default=0,
        description='Internal install Id used by Jenkins')
    variant('copy_user_modules', default=True,
        description='Copy user modules directory instead linking to source')
    variant('adol-c', default=True, description='Compile with ADOL-C')
    variant('tetgen', default=True, description='Compile with Tetgen')
    variant('med', default=True, description='Compile with Med')
    variant('slepc', default=False, description='Compile with Slepc')

    depends_on('mpi')
    depends_on('boost@:1.69 cxxstd=14')
    depends_on('parmetis')
    depends_on('petsc@:3.11.99+mumps+mpi')
    depends_on('slepc@:3.11.99', when='+slepc')

    # MOAB install
    depends_on('moab@:5.1.0', when='@0.8.7:0.9.1')
    depends_on('moab', when='@0.9.2:')
    depends_on('moab', when='@develop')
    depends_on('moab', when='@lukasz')

    # Upper bound set to ADOL-C until issues with memory leaks
    # for versions 2.6: fully resolved
    depends_on('adol-c@2.5.2~examples', when='+adol-c')
    depends_on('tetgen', when='+tetgen')
    depends_on('parmetis')
    depends_on('blas')

    # MED install
    depends_on('med', when='+med')
    depends_on('med@:3.99.99', when='+med @0.8.7:0.9.0')
    depends_on('med@4.0.0:', when='+med @0.9.1:')
    depends_on('med@4.0.0:', when='+med @develop')
    depends_on('med@4.0.0:', when='+med @lukasz')

    extendable = True

    root_cmakelists_dir = 'mofem'

    def cmake_args(self):
        spec = self.spec
        options = []

        # obligatory options
        options.extend([
            '-DWITH_SPACK=YES',
            '-DPETSC_DIR=%s' % spec['petsc'].prefix,
            '-DPETSC_ARCH=',
            '-DMOAB_DIR=%s' % spec['moab'].prefix,
            '-DBOOST_DIR=%s' % spec['boost'].prefix,
            '-DBLAS_DIR=%s' % spec['blas'].prefix])

        # build tests
        options.append('-DMOFEM_BUILD_TESTS={0}'.format(
            'ON' if self.run_tests else 'OFF'))

        # variant packages
        if '+adol-c' in spec:
            options.append('-DADOL-C_DIR=%s' % spec['adol-c'].prefix)

        if '+tetgen' in spec:
            options.append('-DTETGEN_DIR=%s' % spec['tetgen'].prefix)

        if '+med' in spec:
            options.append('-DMED_DIR=%s' % spec['med'].prefix)

        if '+slepc' in spec:
            options.append('-DSLEPC_DIR=%s' % spec['slepc'].prefix)

        # copy users modules, i.e. stand alone vs linked users modules
        options.append(
            '-DSTAND_ALLONE_USERS_MODULES=%s' %
            ('YES' if '+copy_user_modules' in spec else 'NO'))
        return options
