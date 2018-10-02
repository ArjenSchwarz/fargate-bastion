FROM alpine:3.7
EXPOSE 22
RUN apk add --no-cache openssh python py-pip && \
    ssh-keygen -A && \
    mkdir -p /root/.ssh && \
    pip install awscli && \
    apk -v --purge del py-pip
COPY ./publickey /root/.ssh/authorized_keys
RUN chmod 0600 /root/.ssh/authorized_keys
CMD /usr/sbin/sshd -D -e