package main

import rego.v1

is_deployment if {
  input.kind == "Deployment"
}

containers contains container if {
  is_deployment
  some container in input.spec.template.spec.containers
}

deny contains message if {
  some container in containers
  not container.resources.requests.cpu
  message := sprintf("Container %q must define resources.requests.cpu", [container.name])
}

deny contains message if {
  some container in containers
  not container.resources.requests.memory
  message := sprintf("Container %q must define resources.requests.memory", [container.name])
}

deny contains message if {
  some container in containers
  not container.resources.limits.cpu
  message := sprintf("Container %q must define resources.limits.cpu", [container.name])
}

deny contains message if {
  some container in containers
  not container.resources.limits.memory
  message := sprintf("Container %q must define resources.limits.memory", [container.name])
}