data "aws_ami" "ubuntu" {
    most_recent = true

    filter {
      name = "name"
      values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
    }

    filter {
        name = "virtualization-type"
        values = ["hvm"]
    }

    owners = ["099720109477"]
}

data "aws_key_pair" "existing_key_pair" {
    key_name = "my-ec2-keypair"
}

resource "aws_instance" "website" {
  ami = data.aws_ami.ubuntu.id
  instance_type = "t2.medium"
  vpc_security_group_ids = [aws_security_group.my_instance_SG.id]
  key_name = data.aws_key_pair.existing_key_pair.key_name

  user_data = <<-EOF
                #!/bin/bash
                sudo apt-get update
                sudo apt install docker.io -y
                sudo apt install python3-pip -y
                sudo pip3 install flask yfinance numpy pandas matplotlib
                sudo pip3 install --upgrade mplfinance
                sudo apt install git
                mkdir /home/ubuntu/app
                mkdir /home/ubuntu/app2
                cd /home/ubuntu/app
                git clone https://github.com/Krithik1/Support-and-Resistance-Marker.git
                cp -r terraform-deploy-python-app/* /home/ubuntu/app2
                cd /home/ubuntu/app2
                sudo docker build -t pythonflaskapp .
                sudo docker run -p 5000:5000 pythonflaskapp
                EOF

    tags = {
        Name = "my-python-app"
    }
}
