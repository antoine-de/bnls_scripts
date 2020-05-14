
FROM wojtylacz/pypostal-docker

RUN apt update && apt -y install locales git --fix-broken && locale-gen fr_FR.UTF-8
ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8

RUN git clone https://github.com/cquest/reaccentue.git
RUN mv reaccentue/* .

# Note for the first use, you'll need to manually generate the dico dir (see doc in reaccentue)
ADD dico/ /dico
ADD laposte_hexasmal.csv /

ADD requirements.txt /
RUN pip3 install -r requirements.txt
ADD *.py /

ENTRYPOINT ["python3", "cleanup.py"]