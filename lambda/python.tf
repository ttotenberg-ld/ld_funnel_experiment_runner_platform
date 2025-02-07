resource "null_resource" "python_ldsdk" {
  triggers = {
    build_number = timestamp()
  }

  provisioner "local-exec" {
    command = "pip install --target ${path.module}/demoexpgen/ --upgrade launchdarkly_server_sdk"
  }
}

resource "null_resource" "python_ldclient" {
  triggers = {
    build_number = timestamp()
  }

  provisioner "local-exec" {
    command = "pip install --target ${path.module}/demoexpgen/ --upgrade ldclient"
  }
}

resource "null_resource" "python_names" {
  triggers = {
    build_number = timestamp()
  }

  provisioner "local-exec" {
    command = "pip install --target ${path.module}/demoexpgen/ --upgrade names"
  }
}
