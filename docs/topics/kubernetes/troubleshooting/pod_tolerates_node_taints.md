---
title: 'Pod Tolerates Node Taints'
minute_read: 5
categories:
  - kubernetes
  - microservices
tags:
  - kubernetes
  - microservices
---

### Scenario 

You have a single node (master) kubernetes deployment and you want to schedule standard pods. 

The master name is your hostname: `$(hostname)`

Upon your attempt at deploying a service, you notice the state of the resulting pod remains in *Pending*. 

Further investigation via `kubectl describe pod YOUR_POD_NAME` reveals an error similar to <span style="color:red">No nodes are available that match all of the following predicates:: PodToleratesNodeTaints</span>

Due Diligence: 

*   All kubernetes nodes are in a 'Ready' status: `kubectl get nodes`
*   All kubernetes nodes have sufficient resources for pod deployment: `kubectl describe nodes` 
*   Your image is available on the docker registry you've specified in your kubernetes manifest (.yaml)

### Root Cause

As per the kubernetes documentation, standard pods are not allowed scheduling on the master node.

The mechanism by which this is disallowed is via node taints.

You can read more about this here: 

- [Taints and Tolerations - Kubernetes](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/)

### Solution

You want to be able to schedule a standard pod (i.e. does not belong to the kube-system namespace) on your kubernets master node.

As follows: `kubectl taint nodes $(hostname) node-role.kubernetes.io/master:NoSchedule-` 

You should see a confirmation similar to: *node untainted*.

You should now be able to schedule pods on this node.

### Notes 

I came across the github issue description by Googling the following search term: 

`"No nodes are available that match all of the following predicates" "PodToleratesNodeTaints"`