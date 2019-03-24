FROM amazonlinux:2
EXPOSE 22
RUN yum install -y python3 python3-pip tar openssh-server && yum clean all
RUN ssh-keygen -A && \
    pip3 install awscli && \
    curl -o /usr/local/bin/kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.11.5/2018-12-06/bin/linux/amd64/kubectl && \
    chmod +x /usr/local/bin/kubectl && \
    curl --silent --location "https://github.com/weaveworks/eksctl/releases/download/latest_release/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /usr/local/bin/ && \
    mkdir /root/.ssh
COPY ./publickey /root/.ssh/authorized_keys
RUN chmod 0600 /root/.ssh/authorized_keys
CMD /usr/sbin/sshd -D -e