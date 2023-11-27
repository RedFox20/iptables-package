import mama
from mama.utils.system import console
from mama.utils.gnu_project import BuildProduct

# Explore Mama docs at https://github.com/RedFox20/Mama
class iptables(mama.BuildTarget):

    local_workspace = 'packages'

    def init(self):
        self.libmnl = self.gnu_project('libmnl', '1.0.5',
            url='http://kratt.codefox.ee/linux/{{project}}.tar.bz2',
            build_products=[
                BuildProduct('{{installed}}/lib/libmnl.a', None),
            ])
        self.iptables = self.gnu_project('iptables', '1.8.9',
            url='http://kratt.codefox.ee/linux/{{project}}.tar.xz',
            build_products=[
                BuildProduct('{{installed}}/sbin/iptables', '{{build}}/sbin/iptables'),
                BuildProduct('{{installed}}/lib/libxtables.a', '{{build}}/lib/libxtables.a'),
                BuildProduct('{{installed}}/lib/libip4tc.a', '{{build}}/lib/libip4tc.a'),
            ])

    def settings(self):
        self.config.prefer_gcc(self.name)
        if self.mips:
            self.config.set_mips_toolchain('mipsel')

    def build(self):
        if self.libmnl.should_build():
            self.libmnl.build(options='--enable-static')

        if self.iptables.should_build():
            iptables_opts = '--with-gnu-ld --disable-ipv6 --disable-nftables'
            iptables_opts += ' --enable-silent-rules --enable-devel'
            iptables_opts += ' --disable-shared --enable-static' # build everything as static
            self.iptables.extra_env['libmnl_CFLAGS'] = f"-I{self.libmnl.install_dir('include')} "
            self.iptables.extra_env['libmnl_LIBS'] = self.libmnl.install_dir('lib/libmnl.a')
            self.iptables.build(options=iptables_opts)
            self.iptables.deploy_all_products()
        else:
            console('sbin/iptables already built', color='green')

    def package(self):
        self.export_include('include', build_dir=True)
        self.export_asset('sbin/iptables', category='sbin', build_dir=True)
        self.export_lib('lib/libxtables.a', build_dir=True)
        self.export_lib('lib/libip4tc.a', build_dir=True)
