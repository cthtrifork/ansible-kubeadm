# Install ansible-kubeadm

## Prepare inventory

create an inventory like this

```sh
[kube_control_plane]
kubeadm-cp-01   ansible_host=ip-cp1
kubeadm-cp-02   ansible_host=ip-cp2
kubeadm-cp-03   ansible_host=ip-cp3

[kube_workers]
kubeadm-node-01 ansible_host=ip-no1
# ... more nodes

[all:vars]
ansible_user=caspertdk
ansible_become=true
```

## Run

```sh
ansible-playbook -i hosts enix.kubeadm.00_apiserver_proxy.yml enix.kubeadm.01_site.yml
```

You can customize install by adding group_vars, following [Variables references](variables.md)