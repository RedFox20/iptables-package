import mama
from mama.utils.system import console
from mama.utils.gnu_project import BuildProduct

# Explore Mama docs at https://github.com/RedFox20/Mama
class iptables(mama.BuildTarget):

    local_workspace = 'packages'

    def init(self):
        self.libmnl = self.gnu_project('libmnl', '1.0.5',
            url='https://kratt.codefox.ee/linux/{{project}}.tar.bz2',
            build_products=[
                BuildProduct('{{installed}}/lib/libmnl.so.0.2.0', None),
            ])
        
        self.iptables = self.gnu_project('iptables', '1.8.9',
            url='https://kratt.codefox.ee/linux/{{project}}.tar.xz',
            build_products=[
                BuildProduct('{{installed}}/sbin/iptables', None),
                BuildProduct('{{installed}}/lib/libxtables.so.12.7.0', None),
                BuildProduct('{{installed}}/lib/libip4tc.so.2.0.0', None),
            ])

    def settings(self):
        self.config.prefer_gcc(self.name)
        if self.mips:
            self.config.set_mips_toolchain('mipsel')

    def build(self):
        if self.libmnl.should_build():
            self.libmnl.build(options='--disable-static --enable-shared', multithreaded=True)

        if self.iptables.should_build():
            iptables_opts = '--with-gnu-ld --disable-ipv6 --disable-nftables'
            iptables_opts += ' --enable-silent-rules --enable-devel --enable-devel'
            self.iptables.extra_env['libmnl_CFLAGS'] = f"-I{self.libmnl.install_dir('include')} "
            self.iptables.extra_env['libmnl_LIBS'] = self.libmnl.install_dir('lib/libmnl.so')
            self.iptables.build(options=iptables_opts, multithreaded=True)
        else:
            console('sbin/iptables already built', color='green')

    def package(self):
        self.export_include('iptables-built/include', build_dir=True)
        self.export_include('libmnl-built/include', build_dir=True)
        self.export_lib('iptables-built/lib/libxtables.so', build_dir=True)
        self.export_lib('iptables-built/lib/libip4tc.so', build_dir=True)
        self.export_lib('libmnl-built/lib/libmnl.so', build_dir=True)
        # libxtables syslibs: libc.so.6, ld.so.1
