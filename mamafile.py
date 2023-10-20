import mama
from mama.utils.system import console
from mama.utils.gnu_project import BuildProduct

# Explore Mama docs at https://github.com/RedFox20/Mama
class iptables(mama.BuildTarget):

    local_workspace = 'packages'

    def init(self):
        self.iptables = self.gnu_project('iptables', '1.8.9',
            url='https://kratt.codefox.ee/linux/{{project}}.tar.xz',
            build_products=[
                BuildProduct('{{installed}}/sbin/iptables', None),
            ])

    def settings(self):
        self.config.prefer_gcc(self.name)
        if self.mips:
            self.config.set_mips_toolchain('mipsel')

    def build(self):
        if self.iptables.should_build():
            iptables_opts = '--disable-nftables --disable-ipv6 --disable-nflog'
            self.iptables.build(options=iptables_opts)
        else:
            console('sbin/iptables already built', color='green')

    def package(self):
        self.export_include('iptables-built/include', build_dir=True)
        self.export_lib('iptables-built/lib/libxtables.so', build_dir=True)
        self.export_lib('iptables-built/lib/libip4tc.so', build_dir=True)
        # libxtables syslibs: libc.so.6, ld.so.1
