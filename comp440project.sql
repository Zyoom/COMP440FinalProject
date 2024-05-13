create table agents
(
    id   int auto_increment
        primary key,
    name varchar(255) null
);

create table customers
(
    id    int auto_increment
        primary key,
    email varchar(255) null,
    constraint email
        unique (email)
);

create table emails
(
    id             int auto_increment
        primary key,
    subject        varchar(255) null,
    body           text         null,
    customer_id    int          null,
    agent_id       int          null,
    in_reply_to_id int          null,
    in_reply_to    int          null,
    constraint emails_ibfk_1
        foreign key (customer_id) references customers (id),
    constraint emails_ibfk_2
        foreign key (agent_id) references agents (id),
    constraint emails_ibfk_3
        foreign key (in_reply_to_id) references emails (id)
);

create index agent_id
    on emails (agent_id);

create index customer_id
    on emails (customer_id);

create index in_reply_to_id
    on emails (in_reply_to_id);

create table replies
(
    reply_id       int auto_increment
        primary key,
    email_id       int                                null,
    agent_id       int                                null,
    reply_text     text                               not null,
    reply_date     datetime default CURRENT_TIMESTAMP null,
    in_reply_to_id int                                null,
    constraint fk_in_reply_to_id
        foreign key (in_reply_to_id) references emails (id),
    constraint replies_ibfk_1
        foreign key (email_id) references emails (id),
    constraint fk_email_id
        foreign key (email_id) references emails (id)
            on delete cascade,
    constraint replies_ibfk_2
        foreign key (agent_id) references agents (id)
);

create index agent_id
    on replies (agent_id);

create table userreplies
(
    id             int auto_increment
        primary key,
    email_id       int                                 null,
    customer_email varchar(255)                        null,
    reply_text     text                                null,
    reply_date     timestamp default CURRENT_TIMESTAMP null,
    constraint userreplies_ibfk_1
        foreign key (email_id) references emails (id)
);

create index email_id
    on userreplies (email_id);

