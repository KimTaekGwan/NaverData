CREATE TABLE `Crawling_Keywords` (
  `search_id` integer PRIMARY KEY AUTOINCREMENT,
  `type` varchar(255),
  `period` varchar(255),
  `start_date` timestamp,
  `end_date` timestamp,
  `device` varchar(255),
  `gender` varchar(255),
  `age` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `Search_Shop` (
  `search_id` integer PRIMARY KEY,
  `keyword_id` integer,
  `sort` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `Query_Keyword` (
  `query_ID` integer PRIMARY KEY AUTOINCREMENT,
  `keyword_id` integer,
  `add_keyword_id` integer,
  `keyword` varchar(255),
  `sort` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `Search_Keyword` (
  `search_id` integer PRIMARY KEY AUTOINCREMENT,
  `query_id` integer,
  `sort` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `Keywords_Top` (
  `keyword_id` integer PRIMARY KEY AUTOINCREMENT,
  `search_id` integer,
  `ranking` integer,
  `keyword` varchar(255),
  `type` varchar(255)
);

CREATE TABLE `Data_Product` (
  `product_id` integer PRIMARY KEY AUTOINCREMENT,
  `search_id` integer,
  `name` varchar(255),
  `lprice` integer,
  `hprice` integer,
  `link` varchar(255),
  `mallName` varchar(255),
  `maker` maker,
  `brand` varchar(255),
  `category1` varchar(255),
  `category2` varchar(255),
  `category3` varchar(255),
  `category4` varchar(255),
  `product_naver_id` integer,
  `score` float
);

CREATE TABLE `Crawling_store` (
  `search_id` integer PRIMARY KEY AUTOINCREMENT,
  `product_id` integer,
  `created_at` timestamp
);

CREATE TABLE `Data_Reviews` (
  `search_id` integer PRIMARY KEY AUTOINCREMENT,
  `review_id` integer,
  `user_id` varchar(255),
  `score` integer,
  `date` timestamp,
  `data` text,
  `emotion_text` varchar(255),
  `emotion_score` float
);

CREATE TABLE `Data_Posts` (
  `post_id` integer PRIMARY KEY AUTOINCREMENT,
  `search_id` integer,
  `title` varchar(255),
  `link` integer,
  `postdate` timestamp,
  `data` text COMMENT 'Description',
  `emotion_text` varchar(255),
  `emotion_score` float
);

CREATE TABLE `Keyword_Reviews` (
  `keyword_id` integer PRIMARY KEY AUTOINCREMENT,
  `review_id` integer,
  `ranking` integer,
  `keyword` integer,
  `emotion_text` varchar(255),
  `emotion_score` float
);

CREATE TABLE `Keyword_Posts` (
  `keyword_id` integer PRIMARY KEY AUTOINCREMENT,
  `post_id` integer,
  `ranking` integer,
  `keyword` integer,
  `emotion_text` varchar(255),
  `emotion_score` float
);

-- ALTER TABLE `Keywords_Top` ADD FOREIGN KEY (`search_id`) REFERENCES `Crawling_Keywords` (`search_id`);

-- ALTER TABLE `Data_Product` ADD FOREIGN KEY (`search_id`) REFERENCES `Search_Shop` (`search_id`);

-- ALTER TABLE `Search_Shop` ADD FOREIGN KEY (`keyword_id`) REFERENCES `Keywords_Top` (`keyword_id`);

-- ALTER TABLE `Crawling_store` ADD FOREIGN KEY (`product_id`) REFERENCES `Data_Product` (`product_id`);

-- ALTER TABLE `Data_Reviews` ADD FOREIGN KEY (`search_id`) REFERENCES `Crawling_store` (`search_id`);

-- ALTER TABLE `Data_Posts` ADD FOREIGN KEY (`search_id`) REFERENCES `Search_Keyword` (`search_id`);

-- ALTER TABLE `Keyword_Reviews` ADD FOREIGN KEY (`review_id`) REFERENCES `Data_Reviews` (`review_id`);

-- ALTER TABLE `Keyword_Posts` ADD FOREIGN KEY (`post_id`) REFERENCES `Data_Posts` (`post_id`);

-- ALTER TABLE `Query_Keyword` ADD FOREIGN KEY (`keyword_id`) REFERENCES `Keywords_Top` (`keyword_id`);

-- ALTER TABLE `Search_Keyword` ADD FOREIGN KEY (`query_id`) REFERENCES `Query_Keyword` (`query_ID`);

-- ALTER TABLE `Query_Keyword` ADD FOREIGN KEY (`add_keyword_id`) REFERENCES `Keyword_Posts` (`keyword_id`);
