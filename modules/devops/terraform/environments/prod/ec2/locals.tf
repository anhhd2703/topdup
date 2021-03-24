locals {
  user_data = <<EOF
#!/bin/bash
sudo apt-get update
EOF
}
