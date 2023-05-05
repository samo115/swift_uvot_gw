# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /swift_uvot_gw

# Copy the application files into the working directory
COPY . /swift_uvot_gw

##Copy ssh key to allow access to git: samo115/tom_build
#COPY ~/.ssh/id_ed25519 /home/user/.ssh/id_ed25519

#RUN chown -R user:user /home/user/.ssh
#RUN echo "Host remotehost\n\tStrictHostKeyChecking no\n" >> /home/user/.ssh/config


# Install the application dependencies
RUN pip install -r requirements.txt

# Define the entry point for the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 55000