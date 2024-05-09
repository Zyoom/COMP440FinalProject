# Customer Service Email Management System

## Overview

This project is designed for COMP 440, focusing on efficient management and response handling for customer service emails. It aims to maintain seamless communication between agents and customers, ensuring that emails are tracked and handled appropriately. 

## Features

- **Common Email Pool:** All incoming emails are stored in a common pool accessible by customer service agents.
- **Email Assignment:** Emails are assigned to agents who manage the customer interaction.
- **Conversation Tracking:** Email conversations are tracked to maintain continuity with the same agent.
- **Email Management:** Agents can view, reply to, and delete emails.
- **User Interaction:** Users can view past conversations and reply to ongoing threads.

## Tools and Technologies

- **Frontend:** HTML, CSS
- **Backend:** Python
- **Database:** MySQL
- **IDEs:** PyCharm, MySQL Workbench

## Database Design

### Tables and Key Constraints

- **agents, customers, emails, replies, userreplies:** Each table includes an auto-increment primary key for unique identification.
- **customers:** Unique constraint on the email field to prevent duplicate entries.

### Foreign Key Relationships

- **emails table:** Links to `customers` and `agents`, and can reference other emails for threading.
- **replies and userreplies tables:** Link replies to their corresponding emails and track the agent or user responding.

### Deletion and Indexing

- **Cascading Deletes:** Deleting an email will remove all associated replies.
- **Indexing:** Foreign keys are indexed to enhance query performance and efficiency.

### Data Integrity and Timestamps

- **Timestamps:** Utilize datetime and timestamp fields to log exact times of replies, defaulting to the current timestamp.

## Contributions

David Pedroza, Jainivash Korisal
