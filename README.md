# 🚀 FCIS Overflow API (Backend)

![Status](https://img.shields.io/badge/status-completed-brightgreen)
![Language](https://img.shields.io/badge/language-Python%20(Django%20Rest%20Framework)-blue)
![Database](https://img.shields.io/badge/database-PostgreSQL-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> 🌟 **Note**: This repository contains the backend code for FCIS Overflow, an API that emulates the functionality of Stack Overflow. It's especially for computer science students 

## 🌐 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [API Documentation](#-api-documentation)
- [WebSocket Group Chat](#-websocket-group-chat)
- [Blocking User Accounts](#-blocking-user-accounts)
- [Testing](#-testing)
- [Docker Deployment](#-docker-deployment)
- [Environment Variables](#-environment-variables)
- [License](#-license)

## 🌐 Overview
The FCIS Overflow API is designed to replicate the core functionalities of Stack Overflow. It provides a robust backend for a platform where users can ask questions, post answers, and engage in discussions related to computer science courses. This project serves as a comprehensive guide for understanding how a Q&A platform operates and is an excellent resource for both beginners and experienced developers interested in Django and RESTful API development.

## 🌟 Features
- [x] 👤 User Registration and Email Verification via JWT
- [x] 🛡️ User Login with Session Authentication or JWT
- [x] 📌 User Profiles with Profile Pictures and Additional Information
- [x] 📝 Asking Questions with Multiple Attachments
- [x] 💬 Answering Questions and Voting (Up/Down)
- [x] 📊 Filtering Questions by Title, Level, and Course with Pagination 
- [x] 🔍 Searching Questions by Title or Content with Pagination
- [x] 📚 Admin API for Managing Levels and Courses
- [x] 🔗 Retrieving Question and Their Answers
- [x] 🗨️ Group Chat Creation, Member Management, and Real-time Updates with Django Channels
- [x] 🔒 Blocking User Accounts with Admin Intervention
- [x] 🐳 Docker and Docker Compose for Development

## 🚀 Tech Stack
- **Python (Django Rest Framework)**: Server-side Logic
- **Django Channels**: Real-time WebSocket Communication
- **PostgreSQL**: Database
- **Django ORM**: Object-Relational Mapping
- **JWT Authentication**: User Verification
- **Docker-compose**: Containerization for Development and Deployment
- **Redis Channel Layer**: Real-time Chat Updates
- **Signals**: Automatic User Blocking
- **API Testing**: Ensuring Feature Reliability




## 🛠️ Installation & Setup

### 📋 Prerequisites
- **Docker and docker-compose**: [Download and Install](https://www.docker.com/get-started)
### 🧰 Steps
1. **Clone the Repository**
    ```bash
    git clone https://github.com/rengo540/FCIS-overflow-drf.git
    ```
2. **Navigate to the Directory**
    ```bash
    cd FCIS-overflow-drf
    ```
3. **Create `.env` File**
    ```makefile
    # Populate with your secret variables and configuration
    SECRET_KEY=''
    ALLOWED_HOST=
    DEBUG=
    
    DB_ENGINE=django.db.backends.postgresql
    DB_DATABASE=
    DB_USER=
    DB_PASSWORD=
    DB_HOST=db (postgres service name)
    DB_PORT=
    
    EMAIL_HOST_USER=
    EMAIL_HOST_PASSWORD=
    
    REDIS_HOST=cache (redis service name)
    ...
    ```
4. **Start Docker Compose for Development**
    ```bash
    docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d --build
    ```

6. **Create a Superuser (Admin) Account**
    ```bash
    docker-compose exec fcisoverflow-app-container manage.py createsuperuser
    ```


## 📚 API Documentation
[Document your API endpoints here, including request and response examples.]

# 🗨️ WebSocket Group Chat

The FCIS Overflow API includes a WebSocket-based group chat feature that enables real-time communication among users. This chat feature is perfect for collaborative discussions and instant updates within groups.

## 🚀 Getting Started

To use the WebSocket-based group chat feature, follow these steps:

1. **Connect to WebSocket**

    To initiate a WebSocket connection, you need to use WebSocket client libraries or WebSocket-capable tools. You'll connect to the WebSocket server with a URL, typically in the following format:

    ```
    ws://your-api-domain/chat/
    ```

2. **Authentication**

    WebSocket connections can be authenticated using either session authentication or JWT authentication, depending on your setup. Ensure that you include the necessary authentication tokens in the connection request headers.
    this made by middleware authentication
3. **Join a Group**

    To join a group chat, send a WebSocket message to the server indicating your intent to join a specific group. The server will add your WebSocket connection to the corresponding group channel.

4. **Send and Receive Messages**

    Once connected to a group, you can send and receive messages in real time. Messages can be plain text or structured data, depending on your application's requirements.

5. **Real-Time Updates**

    As new messages are sent by participants in the group chat, your WebSocket connection will receive real-time updates. You can update the chat interface to display new messages as they arrive.

## 🌟 Capabilities

The WebSocket-based group chat offers several capabilities:

- **Real-Time Messaging**: Messages are delivered instantly to all participants in the group.

- **Typing Indicators**: You can implement typing indicators to show when users are actively typing.

- **Message History**: Retrieve chat history for a group to display previous messages.

- **Notifications**: Implement notifications to alert users to new messages, even when the chat window is not in focus.

- **Group Management**: Allow users to create, join, and leave chat groups as needed.

- **User Presence**: Show online/offline status of group members.

By leveraging these capabilities, you can create a dynamic and engaging chat experience within your application.

## 📚 Examples

Here are some examples of how you can integrate the WebSocket-based group chat feature into your application:

- **Real-Time Collaboration**: Enable users to collaborate on projects, documents, or discussions in real time.

- **Community Discussions**: Create chat rooms for different topics or interest groups within your application.

- **Support Chat**: Offer real-time customer support through chat channels.

- **Event Updates**: Keep participants informed about event updates, such as agenda changes or announcements.

Feel free to customize and expand upon these examples to fit your specific application's needs.

This WebSocket-based group chat feature enhances user engagement and interaction within your application, providing a richer and more dynamic experience.

    

## 🔒 Blocking User Accounts
[Detail the user account blocking mechanism and admin intervention.]

## 🧪 Testing
[Provide information on running API tests and ensuring feature reliability.]

## 🐳 Docker Deployment
[Explain how to deploy the project using Docker for production.]

## 🌐 Environment Variables
[List and describe the essential environment variables required for the project.]

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

______________________

Feel free to add any additional information or sections as needed for your project's specific requirements. Good luck with your FCIS Overflow API project!

