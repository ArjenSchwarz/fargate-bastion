FROM amazonlinux:2
EXPOSE 22
ARG EKS_K8S_VERSION=1.11.5
RUN yum install -y python3 python3-pip tar openssh-server vim-minimal bash-completion jq && yum clean all && pip3 install awscli
RUN ssh-keygen -A && \
    curl -o /usr/local/bin/kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/$EKS_K8S_VERSION/2018-12-06/bin/linux/amd64/kubectl && \
    chmod +x /usr/local/bin/kubectl && \
    curl -o /usr/local/bin/aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/$EKS_K8S_VERSION/2018-12-06/bin/linux/amd64/aws-iam-authenticator && \
    chmod +x /usr/local/bin/aws-iam-authenticator && \
    curl --silent --location "https://github.com/weaveworks/eksctl/releases/download/latest_release/eksctl_linux_amd64.tar.gz" | tar xz -C /usr/local/bin/ && \
    mkdir /root/.ssh
COPY ./.bashrc /root/.bashrc
# COPY ./publickey /root/.ssh/authorized_keys
# RUN chmod 0600 /root/.ssh/authorized_keys
CMD /usr/sbin/sshd -D -e
