# This is the base for contrail specific children

ARG CONTRAIL_REGISTRY
ARG CONTRAIL_CONTAINER_TAG
FROM ${CONTRAIL_REGISTRY}/contrail-general-base:${CONTRAIL_CONTAINER_TAG}

ARG BASE_EXTRA_RPMS=""

# note: ldconfig looks strange. contrail-lib installs shared libraries but do not call it...
RUN mkdir -p -m 777 /var/crashes && \
    BASE_EXTRA_RPMS=$(echo $BASE_EXTRA_RPMS | tr -d '"' | tr ',' ' ') && \
    if [[ -n "$BASE_EXTRA_RPMS" ]] ; then \
        echo "INFO: contrail-base: install $BASE_EXTRA_RPMS" ; \
        yum install -y $BASE_EXTRA_RPMS ; \
    fi && \
    yum install -y contrail-lib contrail-setup contrail-utils python-contrail && \
    yum clean all -y && \
    rm -rf /var/cache/yum && \
    ldconfig

COPY *.sh /

ENV PS1="\033[1m($(printenv NODE_TYPE)-$(printenv SERVICE_NAME))\033[m\017[$(id -un)@$(hostname -s) $(pwd)]$ "

CMD ["/usr/bin/tail","-f","/dev/null"]
