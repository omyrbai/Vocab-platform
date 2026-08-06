-- vocab_platform.languages definition

CREATE TABLE `languages` (
  `lang_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `lang_code` char(2) NOT NULL,
  `language_name` varchar(100) NOT NULL,
  `native_name` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`lang_id`),
  UNIQUE KEY `uq_languages_code` (`lang_code`),
  UNIQUE KEY `uq_languages_name` (`language_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- vocab_platform.topics definition

CREATE TABLE `topics` (
  `topic_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `parent_topic_id` bigint(20) unsigned DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`topic_id`),
  KEY `fk_topics_parent` (`parent_topic_id`),
  CONSTRAINT `fk_topics_parent` FOREIGN KEY (`parent_topic_id`) REFERENCES `topics` (`topic_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- vocab_platform.terms definition

CREATE TABLE `terms` (
  `term_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `topic_id` bigint(20) unsigned DEFAULT NULL,
  `src_lang_id` smallint(5) unsigned NOT NULL,
  `trg_lang_id` smallint(5) unsigned NOT NULL,
  `term` varchar(255) NOT NULL,
  `pronunciation` varchar(255) DEFAULT NULL,
  `definition` text NOT NULL,
  `example` text NOT NULL,
  `translation` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`term_id`),
  UNIQUE KEY `uq_term` (`topic_id`,`src_lang_id`,`trg_lang_id`,`term`),
  KEY `fk_terms_src_lang` (`src_lang_id`),
  KEY `fk_terms_trg_lang` (`trg_lang_id`),
  CONSTRAINT `fk_terms_src_lang` FOREIGN KEY (`src_lang_id`) REFERENCES `languages` (`lang_id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_terms_topic` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`topic_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_terms_trg_lang` FOREIGN KEY (`trg_lang_id`) REFERENCES `languages` (`lang_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;