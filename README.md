compat-nettle32-srpm
====================

This is based on sergiomb2's work at

     https://github.com/sergiomb2/SambaAD

I've peeld off the "compat-nettle32" tool he published for RHEL 7
and published it as a separate submodule, the way I do for other git submodules
for Samba compilation See this URL for the layout.

     https://github.com/nkadel/samba4repo

compat-nettle32 is needed to build a compat-gnutls34 on RHEL 7.

To build it locally, first obtain the tarball from the Source:
location in the .spec file. To build it locally, use:

   make build

To compile it with mock and put it in ../samba4repo for reference:

   make all install

Nico Kadel-Garcia <nkadel@gmail.com>
