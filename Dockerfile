FROM continuumio/miniconda3 AS build

WORKDIR /pydatastructs

COPY . .

RUN conda env create --file environment.yml
RUN conda run -n pyds-env python scripts/build/install.py
RUN conda run -n pyds-env python scripts/build/develop.py

CMD ["conda", "run", "-n", "pyds-env", "python", "-c", "from pydatastructs.utils.testing_util import test; test(); import time; time.sleep(3600)"]