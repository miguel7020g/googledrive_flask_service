CREATE TABLE `drive_file_register` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(20) NOT NULL DEFAULT 'no_name',
  `file_url` varchar(100) NOT NULL DEFAULT 'no_url',
  `file_date_created` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

