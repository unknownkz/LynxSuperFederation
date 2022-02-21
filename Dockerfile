# Copyright © 2022 Unknown
# All Rights Reserved
FROM unknownxx/lsf:botmanage

RUN git clone https://github.com/unknownkz/LynxSuperFederation /usr/src/lsf

WORKDIR /usr/src/lsf
ENV PATH="/usr/src/lsf:$PATH"

RUN pip3 install -U -r requirements.txt
RUN rm -rf -- /var/lib/apt/lists/*

RUN chmod a+x startapp
CMD ["./startapp"]
