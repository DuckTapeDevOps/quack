FROM public.ecr.aws/lambda/python:3.12

COPY ingest.py requirements.txt ./

RUN pip install -r requirements.txt
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["index.handler"]
