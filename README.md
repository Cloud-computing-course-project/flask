# Storage Web Application with In-Memory Key-Value Cache

This repository contains an application that offers you the opportunity to develop a storage web application with an in-memory key-value cache. Through this project, you will gain hands-on experience in deploying and running your application on Amazon EC2.

## Application Overview

The storage web application consists of five key components:

1. **Web Browser**: The web browser acts as the client and initiates requests to the application. It provides a user interface for interacting with the web application.

2. **Web Front End**: The web front end component manages requests and operations received from the web browser. It handles the user input, processes requests, and communicates with other components to fulfill the requested operations.

3. **Local File System**: All data is stored in the local file system. This component manages the storage and retrieval of data from disk.

4. **Mem-Cache**: The mem-cache component provides faster access to frequently accessed data by storing it in memory. It serves as an in-memory key-value cache, improving the overall performance of the application.

5. **Relational Database (RDBMS)**: This component stores a list of known keys, configuration parameters, and other important values. It provides persistent storage for the application and allows efficient retrieval and querying of data.


## Acknowledgements

We would like to acknowledge the following resources and frameworks that contributed to the development of this application:

- [Amazon EC2](https://aws.amazon.com/ec2/)
- [Amazon S3](https://aws.amazon.com/s3/)
- [Flask](https://flask.palletsprojects.com/en/2.3.x/)

Thank you for exploring our storage web application! We hope you find this project informative and useful for your web development journey.
