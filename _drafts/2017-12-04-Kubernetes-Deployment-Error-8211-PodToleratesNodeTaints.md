---
ID: 900
post_title: 'Kubernetes Deployment Error &#8211; PodToleratesNodeTaints'
author: Bert Tejeda
post_excerpt: ""
layout: post
permalink: http://bertdotself.com/?p=900
published: false
---
# Scenario You have a single node (master) kubernetes deployment and you want to schedule standard pods. The master name is your hostname: 

`$(hostname)`. Upon your attempt at deploying a service, you notice the state of the resulting pod remains in *Pending*. Further investigation via `kubectl describe pod {{ YOUR_POD_NAME }}` reveals an error similar to `No nodes are available that match all of the following predicates:: PodToleratesNodeTaints` Due Diligence: 
*   All kubernetes nodes are in a 'Ready' status: `kubectl get nodes`
*   All kubernetes nodes have sufficient resources for pod deployment: `kubectl describe nodes` 
*   Your image is available on the docker registry you've specified in your kubernetes manifest (.yaml)

# Troubleshooting According to this post: "No nodes are available that match all of the following predicates:: PodFitsHostPorts (1), PodToleratesNodeTaints" 

<https://github.com/kubernetes/kubernetes/issues/49440> The troubleshooting methodology was to review the kubernetes codebase: 
*   Navigate to the kubernetes github repo 
*   Search the repository for the relevant function 
*   Kubernetes is written in golang, so search for "func PodToleratesNodeTaints" As such, the following block of code: 

`if v1helper.TolerationsTolerateTaintsWithFilter(pod.Spec.Tolerations, taints, filter) {
  return true, nil, nil
}` Will not be executed, which will trigger the next line of code: `return false, []algorithm.PredicateFailureReason{ErrTaintsTolerationsNotMatch}, nil` Effectively returning false, hence the original error Further investigation on your master: `kubectl describe node $(hostname) | grep -i taint` If the command returns something similar to: `Taints:     node-role.kubernetes.io/master:NoSchedule` Then your node is unschedulable. The fix would be to remove this taint, as follows: `kubectl taint nodes $(hostname) node-role.kubernetes.io/master:NoSchedule-` You should see a confirmation similar to: `node {{ NODE_NAME }} untainted` You should now be able to schedule pods on this node 
# Notes I came across the github issue description by Googling the following search term: 

`gls*"No nodes are available that match all of the following predicates" "PodToleratesNodeTaints"`