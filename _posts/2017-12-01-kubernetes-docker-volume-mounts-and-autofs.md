---
title: 'Kubernetes, Docker volume mounts, and autofs'
minute_read: 5
categories:
  - kubernetes
  - docker
tags:
  - docker
  - volume
  - mounts
  - breakfix
  - autofs
  - ssh
  - troubleshooting
---

### Scenario 

I'm unable to login to my docker host via ssh public key, but my password works, and/or I'm able to login to the system console.

Once at the console, I observed an error similar to:

<span style="color:red">
Could not chdir to home directory /home/myuser: Too many levels of symbolic links
    -bash: /home/myuser/.bash_profile: Too many levels of symbolic links
</span>

Hmm wtf ...

### Environment details

- Machine_Type: Virtual 
- OS: Oracle Enterprise Linux 7.x
- Software: Docker 1.12.6, Kubernetes 1.7.1

### Troubleshooting Steps

A fellow admin suggested I check for docker mapped volumes that point to /home

Here's the command I used to query for that:

`sudo docker ps --filter volume=/home --format "Name:\\n\\t{{.Names}}\\nID:\\n\\t{{.ID}}\\nMounts:\\n\\t{{.Mounts}}\\n"`

Boom, looks like the kubernetes weaver pod is using that mapping:

  ```
  Name:
          k8s_weave_weave-net-ljzn9_kube-system_740c10c5-d6b8-11e7-838f-005056b5384e_0
  ID:
          dc95801e4442
  Mounts:
          /opt/kubernetes,/lib/modules,/run/xtables.lo, \
          /var/lib/kubele,/var/lib/weave,/etc,/var/lib/dbus,/var/lib/kubele,/home
  ```

Ok, so why would a docker volume mapped to `/home` induce such a problem?

Turns out that in some cases, binding autofs-mounted paths to docker containers can cause problems on the docker host.

This is due to the way in which kubernetes performs the volume mapping, which utilizes docker volume binds under the hood.

And, depending on how you map a volume to a docker container, you might conflict with autofs volume mounting.

For insight into a similar issue, see:

- Issue with AutoFS mounts and docker 1.11.2: [https://github.com/moby/moby/issues/24303](https://github.com/moby/moby/issues/24303)

According to the issue description above, the problem we're seeing might be fixed by adjusting the bind propagation for the volume mount in question.

- See: [https://docs.docker.com/engine/admin/volumes/bind-mounts/#choosing-the--v-or-mount-flag](https://docs.docker.com/engine/admin/volumes/bind-mounts/#choosing-the--v-or-mount-flag)

However, there's no way to control that setting via a kubernetes manifest, not at present at least, since HostPath bind propagation is currently a proposed feature in kubernetes.

- See: [https://github.com/kubernetes/community/blob/master/contributors/design-proposals/node/propagation.md](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/node/propagation.md) 

So the best course of action is to simply change hostPath setting in the weave-kube manifest, e.g.

- Change:
      ```
      hostPath:
        path: /home
      ```
- To:
      ```
      hostPath:
        path: /opt/kubernetes/bind-mounts/weave-kube/home
      ```

You can then simply redeploy the offending container: `kubectl delete daemonset weave-net && kubectl apply -f weave-net.yaml`

Note: You'll have to perform similar changes to the weave manifest according to whatever other autofs mounts its hostPath(s) might conflict with.

### Learning Points

If you are utilizing autofs on your docker host, ensure you review your autofs settings before deploying your containers.