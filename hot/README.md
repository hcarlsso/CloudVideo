# Heat orch template

This template will setup the application on the openstack cluster. Currently
it is derived from the faafo application. Weak point of design is the reliance
on the mysql database, but it could probably be replaced by openstack swift.

To fire up cluster type:

    openstack stack create -t arch_video.yaml VideoConverter
