# Copyright © 2022 Unknown
# All Rights Reserved
FROM unknownxx/lsf:botmanage

ENV TZ=Asia/Jakarta

RUN git clone https://github.com/unknownkz/LynxSuperFederation /usr/src/lsf

WORKDIR /usr/src/lsf
ENV PATH="/usr/src/lsf:$PATH"

RUN pip3 freeze > dev-req.txt
RUN pip3 install -U -r dev-req.txt
RUN rm -rf -- /var/lib/apt/lists/*

RUN chmod a+x startapp
CMD ["./startapp"]
