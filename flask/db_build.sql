DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS Communities;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Communities_Joined;



CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP NOT NULL,
    Username TEXT NOT NULL,
    Password TEXT NOT NULL,
    Karma INTEGER NOT NULL DEFAULT 100,
    About TEXT
);


CREATE TABLE Categories (
    category_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    Name TEXT NOT NULL
);
CREATE TABLE Communities (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    Name TEXT NOT NULL,
    ABOUT TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

CREATE TABLE Posts (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    Votes INTEGER NOT NULL DEFAULT 0,
    creator_id INTEGER NOT NULL,
    community_id INTEGER NOT NULL,
    FOREIGN KEY (creator_id) REFERENCES Users(id),
    FOREIGN KEY (community_id) REFERENCES Communities(id)
);
CREATE TABLE Comments (
    comment_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Content TEXT NOT NULL,
    Votes INTEGER NOT NULL DEFAULT 0,
    creator_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    FOREIGN KEY (creator_id) REFERENCES Users(id),
    FOREIGN KEY (post_id) REFERENCES Posts(id)
);


CREATE TABLE Communities_Joined (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    community_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (community_id) REFERENCES Communities(id)
);