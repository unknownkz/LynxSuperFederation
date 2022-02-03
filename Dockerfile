# Copyright © 2022 Unknown
# All Rights Reserved
FROM unknownxx/lsf:botmanage
RUN apt-get update -y
RUN git clone https://github.com/unknownkz/LynxSuperFederation /usr/src/lsf
COPY requirements.txt .
WORKDIR /usr/src/lsf
RUN pip3 install --no-cache-dir -U -r requirements.txt
COPY . .
RUN chmod a+x startapp
CMD ["./startapp"]
