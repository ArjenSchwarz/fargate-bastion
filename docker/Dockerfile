FROM alpine:3.7
EXPOSE 22
RUN apk add --no-cache openssh && \
    ssh-keygen -A && \
    mkdir -p /root/.ssh
COPY ./publickey /root/.ssh/authorized_keys
RUN chmod 0600 /root/.ssh/authorized_keys
CMD /usr/sbin/sshd -D -e