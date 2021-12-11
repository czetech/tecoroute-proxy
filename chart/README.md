# Helm chart for TecoRoute Proxy

Proxy for easy authentication to the TecoRoute service.

**Homepage:** <https://opensource.cze.tech/tecoroute-proxy>

## Requirements

Kubernetes: `>= 1.14.0-0`

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| nameOverride | string | `""` | Override the name of the chart |
| fullnameOverride | string | `""` | Override the default fully qualified app name |
| control | string | `"/TR_PROXY"` | The control path. |
| origin | string | `"http://route.tecomat.com:61682"` | TecoRoute service URL. |
| verbose | bool | `false` | Verbose mode. |
| image.repository | string | `"czetech/tecoroute-proxy"` | Image repository |
| image.tag | string | `"0.3.0"` | Image tag |
| image.pullPolicy | string | `"IfNotPresent"` | [Image pull policy][k8s-imagepull] (imagePullPolicy of a container) |
| imagePullSecrets | list | `[]` | [Registry secret][k8s-registry] (imagePullSecrets of a pod, see example in [values.yaml]) |
| http.annotations | object | `{}` | _http deployment_ annotations |
| http.replicaCount | int | `1` | Number of _http deployment_ replicas |
| http.podAnnotations | object | `{}` | _http deployment_ pod annotations |
| http.lifecycle | object | `{}` | _http deployment_ container [lifecycle hooks][k8s-lifecycle] |
| http.resources | object | `{}` | _http deployment_ container [resources][k8s-resources] |
| http.affinity | object | `{}` | _http deployment_ pod [affinity][k8s-affinity] |
| http.nodeSelector | object | `{}` | _http deployment_ pod [node selector][k8s-nodeselector] |
| http.tolerations | list | `[]` | _http deployment_ pod [tolerations][k8s-tolerations] |
| http.service.annotations | object | `{}` | _http service_ annotations |
| http.service.type | string | `"ClusterIP"` | _http service_ [type][k8s-servicetype] |
| http.service.port | int | `80` | _http service_ port |
| http.service.nodePort | int | `nil` | _http service_ node port |
| ingress.enabled | bool | `false` | Ingress record generation |
| ingress.className | string | `nil` | Ingress class name |
| ingress.annotations | object | `{}` | Ingress annotations |
| ingress.tls | list | `[]` | Ingress [TLS certificates][k8s-tls] |
| ingress.hosts | list | `[]` | List of hosts pointing to an application (list of strings) |
| ingress.path | string | `"/"` | Path pointing to an application (the format depends on the Kubernetes provider) |
| ingress.pathType | string | `"ImplementationSpecific"` | Ingress [path type][k8s-pathtype] |
| ingress.precedingPaths | list | `[]` | Additional arbitrary paths that may need to be added to the ingress before the main path (see example in [values.yaml]) |
| ingress.succeedingPaths | list | `[]` | Same as precedingPaths but added after the main path |

## Source Code

* <https://github.com/czetech/tecoroute-proxy>

[k8s-affinity]: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity
[k8s-imagepull]: https://kubernetes.io/docs/concepts/containers/images/#updating-images
[k8s-lifecycle]: https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/
[k8s-nodeselector]: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/
[k8s-pathtype]: https://kubernetes.io/docs/concepts/services-networking/ingress/#path-types
[k8s-registry]: https://kubernetes.io/docs/concepts/containers/images/#using-a-private-registry
[k8s-resources]: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
[k8s-servicetype]: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types
[k8s-tls]: https://kubernetes.io/docs/concepts/services-networking/ingress/#tls
[k8s-tolerations]: https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/
[values.yaml]: values.yaml
