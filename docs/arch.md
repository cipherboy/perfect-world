# Architecture Description

The below sections begin outlining various design decisions of a perfect world.

## Overview

perfect-world (pw) aims to replicate a "perfect world" where applications are
separated by different user accounts, allowing the operating system, file
system, and SELinux to fully separate disparate actions. This is useful from
several perspectives:
    - Security: ensuring that each application has the minimum necessary
        permissions.
    - Reproducibility: ensuring that application development starts from a
        known state.
    - Isolation: ensuring that only limited access to specific resources is
        allowed.
These can be accomplished by various means: native applications, chroot jails,
docker containers, and virtual machines. This project aims to be lighter weight
than similar separation projects such as Qubes OS, but potentially allow for
more security than the Android model.


## Design Decisions

The user should be allowed to decide the level of separation a logical unit
has: user, chroot, container, or virtual machine. Logical units need not be
single applications, and can be development environments, etc. Significant
automation is required for this to be practical, and secure inter-account
communication is necessary.


## World (User) Accounts

The basis of a world will be a separate user account. The current assumption
will be that the base system is single-user and thus we can create other user
accounts as we see fit. To enable secure communication between worlds, it is
proposed to set up a Kerberos realm and optionally a local 2FA authentication
server. This would allow local 2FA without requiring an internet connection
and potentially, with proper PAM integration, allow for quicker (non-password)
based authentication between worlds.

### Naming Convention

One long form name could be `pw-$admin-$world`, however this could cause some
issues if dashes are not allowed (or use underscores). In this case, `$admin`
would be the name of the controlling admin user, and `$world` would be the
chosen name. Otherwise, the admin could be left to create their own usernames,
which would likely be shorter.

### UID Convention

Suggested:

    - 100 - 299: base worlds (next free)
    - 300 - 499: chrooted worlds (next free)
    - 500 - 699: container worlds (next free)
    - 700 - 899: virtual machine worlds (next free)

In this way, world types can be inferred by their uid.

### Group Convention

In addition to UIDs, groups can be used to signal world types. This would also
allow for additional groups for signaling features:

Types:
    - pwbase: base/raw application worlds
    - pwchroot: chrooted worlds
    - pwcontainer: containerized worlds
    - pwvm: virtual machine worlds

Features:
    - pwcommunication: for communicating with other worlds besides the admin
    - pwgui: for launching gui applications
    - pwadmin: for performing administrative actions
    - pwclipboard: for access to the perfect-world clipboard
    - pwsharedfs: for access to shared file system locations (r/w)
    - pwsharedfsr: for read-only access to shared file system locations


## Secure IAC

By virtue of having a Kerberos principal/keytab entry, worlds would be able to
communicate securely via sockets wrapped with Kerberos. This would allow worlds
to validate who is communicating with them, verify that they have the correct
permissions to do so, and ensure that this communication happens securely. This
can be done via gssapi calls.

Alternatively, these communications could go through a central daemon, for
logging and an additional ACL layer (daemon controls the creation of both
ends of the pipes, ensuring that no other world can read/write to that socket).
Furthermore, creation of the socket can be validated against user input/intent.

This could be used for a variety of purposes: allowing access to the clipboard,
sharing specific files or directories, granting SSH access, and potentially
allowing actions to be performed on files (say, granting access to a reduced
set of GPG features for git/etc. to function without giving access to the
underlying key). Without centralization, these features could be relatively
meaningless as distributed logs would have to be consistently audited, etc.,
but by centralizing, specific and limited rules could be constructed on a
per-application pair basis (always requiring approval for gpg operations for
instance).

## File System Access

One feature would be segregating file system locations for each world; however,
it is desirable to have a shared location for all worlds. This could be
accomplished by having a shared location with group ownership; one for
read-only access and another for read-write access. Thus if a world only needs
to read files (such as a browser having limited access for uploading files),
this can be accomplished via a read-only location, whereas a shared
Downloads folder would require read-write for all members.
