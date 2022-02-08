# Copyright © 2022 Unknown
# All Rights Reserved
FROM unknownxx/lsf:botmanage

ENV LANG C.UTF-8

RUN git clone https://github.com/unknownkz/LynxSuperFederation /usr/src/lsf

WORKDIR /usr/src/lsf
ENV PATH="/usr/src/lsf/bin:$PATH"

RUN pip3 install --no-cache-dir -U -r requirements.txt

RUN chmod a+x startapp
CMD ["./startapp"]
