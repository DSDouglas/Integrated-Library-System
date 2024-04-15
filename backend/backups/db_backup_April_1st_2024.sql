-- MariaDB dump 10.19  Distrib 10.5.23-MariaDB, for Linux (x86_64)
--
-- Host: ils-db-instance.cti8om2oa2p6.us-east-1.rds.amazonaws.com    Database: librarysystem
-- ------------------------------------------------------
-- Server version	10.11.6-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Admin`
--

DROP TABLE IF EXISTS `Admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Admin` (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `admin_id` (`admin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Admin`
--

LOCK TABLES `Admin` WRITE;
/*!40000 ALTER TABLE `Admin` DISABLE KEYS */;
INSERT INTO `Admin` VALUES (1,'T.V.','Frank','watchmerock@deep13.com','yesdrf','65x$x#b6Da65psq@'),(2,'Bridget','Nelson','ladynuuveena@mst3k.net','hihoney','joXGBqEn7f#k!s5F');
/*!40000 ALTER TABLE `Admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Book`
--

DROP TABLE IF EXISTS `Book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Book` (
  `book_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `pub_year` year(4) DEFAULT NULL,
  `publisher` varchar(255) DEFAULT NULL,
  `genre` varchar(255) DEFAULT NULL,
  `isbn` bigint(20) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `on_hold` tinyint(1) DEFAULT NULL,
  `hold_end` date DEFAULT NULL,
  `checkout_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `fee` tinyint(1) DEFAULT NULL,
  `fee_amount` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`book_id`),
  UNIQUE KEY `book_id` (`book_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `Book_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Patron` (`patron_id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Book`
--

LOCK TABLES `Book` WRITE;
/*!40000 ALTER TABLE `Book` DISABLE KEYS */;
INSERT INTO `Book` VALUES (1,'The Hobbit','J. R. R. Tolkien',2013,'Boston : Mariner Books/Houghton Mifflin Harcourt','Young Adult',395071229,2,0,NULL,NULL,NULL,0,0.00),(2,'Thud!','Terry Pratchett',2014,'New York : Harper, an imprint of HarperCollinsPublishers','Comedy, Fantasy, Horror, Science Fiction',62334985,2,0,NULL,NULL,NULL,0,0.00),(3,'Monstrous Regiment',' Terry Pratchett',2014,'New York : Harper, an imprint of HarperCollinsPublishers','Comedy, Fantasy, Horror, Science Fiction',62307415,NULL,0,NULL,NULL,NULL,0,0.00),(4,'The Antikythera Mechanism: The History and Mystery of the Ancient World’s Most Famous Astronomical Device','Charles River Editors',2017,'CreateSpace Independent Publishing Platform','History',1519706138,NULL,0,NULL,NULL,NULL,0,0.00),(5,'Asterix and the Chariot Race','Jean-yves Ferri',2018,'London : Orion','Graphic Novel',1510105003,NULL,0,NULL,NULL,NULL,0,0.00),(6,'Asterix and the Missing Scroll','Jean-yves Ferri',2016,'London Orion Books','Graphic Novel',1510100466,NULL,0,NULL,NULL,NULL,0,0.00),(7,'Real bento: fresh and easy lunchbox recipes from a Japanese working mom','Kanae Inoue',2020,'Tokyo : Tuttle Publishing','Food',4805315774,NULL,0,NULL,NULL,NULL,0,0.00),(8,'Disney Princess Tea Parties','Sarah W. Caron',2022,'San Rafael, California : Insight editions','Food',1647223755,NULL,0,NULL,NULL,NULL,0,0.00),(9,'Cousteaus Great White Shark','Jean-Michel Cousteau, Mose Richards',1992,'Harry N Abrams Inc','Science',810931818,NULL,0,NULL,NULL,NULL,0,0.00),(10,'Catch-22','Joseph Heller',2011,'Simon & Schuster','Comedy, Drama',1451626657,NULL,0,NULL,NULL,NULL,0,0.00),(11,'Babel','R. F. Kuang',2022,'Harper Voyager','Fantasy, Horror, Science Fiction',63021426,NULL,0,NULL,NULL,NULL,0,0.00),(12,'1Q84','Haruki Murakami',2011,'Knopf Doubleday Publishing Group','Fantasy, Science Fiction',307593312,NULL,0,NULL,NULL,NULL,0,0.00),(13,'The Fifth Season','N. K. Jemisin',2015,'Orbit','Fantasy',316229296,NULL,0,NULL,NULL,NULL,0,0.00),(14,'The Eye of the World','Robert Jordan',2020,'Tor Books','Fantasy',1250754739,NULL,0,NULL,NULL,NULL,0,0.00),(15,'Mr. Midshipman Hornblower','C. S. Forester',1998,'Little Brown & Co; Later Printing','Young Adult',316290602,NULL,0,NULL,NULL,NULL,0,0.00),(16,'Chronicles of the Black Company','Glen Cook',2007,'Tor Books','Fantasy',765319233,NULL,0,NULL,NULL,NULL,0,0.00),(17,'Heir to the Empire','Timothy Zahn',1992,'New York : Bantam Books','Fantasy, Horror, Science Fiction',553296129,NULL,0,NULL,NULL,NULL,0,0.00),(18,'Nice Dragons Finish Last','Rachel Aaron',2014,'CreateSpace Independent Publishing Platform','Fantasy , Science Fiction',1500506338,NULL,0,NULL,NULL,NULL,0,0.00),(19,'Lanzelet: Romance of Lancelot','Ulrich Von Zatzikhoven',1951,'Columbia University Press','Fantasy, History',231018339,NULL,0,NULL,NULL,NULL,0,0.00),(20,'Hieroglyphs and the Afterlife in Ancient Egypt','Werner Forman, Stephen Quirke',1996,'University of Oklahoma Press','History',806127511,NULL,0,NULL,NULL,NULL,0,0.00),(21,'The Book of Taliesin: Poems of Heroism and Magic in Another Britain','Rowan Williams, Gwyneth Lewis',2019,'Penguin Classics','Fantasy, History, Poetry',241381134,NULL,0,NULL,NULL,NULL,0,0.00),(22,'A Little Princess','Frances Hodgson Burnett',1995,'Grosset & Dunlap, New York','History, Young Adult',448409498,NULL,0,NULL,NULL,NULL,0,0.00),(23,'What Color Is Your Parachute?','Richard N. Bolles',2022,'Ten Speed Press','Business',1984861204,NULL,0,NULL,NULL,NULL,0,0.00),(24,'The Economy of Renaissance Florence','Richard A. Goldthwaite',2011,'Johns Hopkins University Press','Economics, History',1421400596,NULL,0,NULL,NULL,NULL,0,0.00),(25,'The Lute in Britain: A History of the Instrument and Its Music','Matthew Spring',2001,'Oxford University Press','History, Music',198166206,NULL,0,NULL,NULL,NULL,0,0.00),(26,'Just for Fun: The Story of an Accidental Revolutionary','Linus Torvalds, David Diamond',2002,'Harper Business','Biography, Computers, History',66620732,NULL,0,NULL,NULL,NULL,0,0.00),(27,'The Year-Round Solar Greenhouse: How to Design and Build a Net-Zero Energy Greenhouse','Lindsey Schiller, Marc Plinke',2016,'New Society Publishers','Garden, Science, Technology',865718245,NULL,0,NULL,NULL,NULL,0,0.00),(28,'Tea: History, Terroirs, Varieties','Kevin Gascoyne, Francis Marchand, Jasmin Desharnais, Hugo Americi',2018,'Firefly Books','Food, History, Science, Travel',228100275,NULL,0,NULL,NULL,NULL,0,0.00),(29,'Ian McKellen: A Biography','Garry OConnor',2019,'St. Martins Press','Biography, History',1250223881,NULL,0,NULL,NULL,NULL,0,0.00),(30,'How Your House Works: A Visual Guide to Understanding and Maintaining Your Home','Charlie Wing',2018,'RSMeans','Home, Science, Technology',1119467616,NULL,0,NULL,NULL,NULL,0,0.00),(31,'Dodger','Terry Pratchett',2012,'Clarion Books','Drama, History, Mystery, Romance, Young Adult',62009494,NULL,0,NULL,NULL,NULL,0,0.00),(32,'Bloodsucking Fiends: A Love Story','Christopher Moore',1995,'Simon & Schuster','Comedy, Fantasy, Horror, Romance',684810972,NULL,0,NULL,NULL,NULL,0,0.00),(33,'The Chronicles of Master Li and Number Ten Ox','Barry Hughart',1998,'The Stars Our Destination Books','Comedy, Fantasy, History, Horror, Mystery',966543602,NULL,0,NULL,NULL,NULL,0,0.00),(34,'The Blue Zones, Second Edition: 9 Lessons for Living Longer From the People Whove Lived the Longest','Dan Buettner',2012,'National Geographic','Health',1426209487,NULL,0,NULL,NULL,NULL,0,0.00),(35,'Built from Broken: A Science-Based Guide to Healing Painful Joints, Preventing Injuries, and Rebuilding Your Body','Scott H Hogan',2011,'North Atlantic Books','Health',1583943714,NULL,0,NULL,NULL,NULL,0,0.00),(36,'Scary Stories to Tell in the Dark: Three Books to Chill Your Bones','Alvin Schwartz',2019,'HarperCollins','Horror',62968971,NULL,0,NULL,NULL,NULL,0,0.00),(37,'Cant Spell Treason Without Tea','Rebecca Thorne',2024,'Bramble ','Comedy, Fantasy, LGBTQ+, Romance',1250333296,NULL,0,NULL,NULL,NULL,0,0.00),(38,'Fish & Chips','Madeleine Urban, Abigail Roux',2010,'Dreamspinner ','Comedy, LGBTQ+, Mystery, Romance, Suspense',1615812261,NULL,0,NULL,NULL,NULL,0,0.00),(39,'The Murder at the Vicarage','Agatha Christie',2016,'William Morrow & Company','Murder, Mystery, Suspense',62573381,NULL,0,NULL,NULL,NULL,0,0.00),(40,'The Secret of the Old Clock','Carolyn Keene',1930,'Grosset & Dunlap','Comedy, Mystery, Young Adult',448095017,NULL,0,NULL,NULL,NULL,0,0.00),(41,'The Plantagenets: The Warrior Kings and Queens Who Made England','Dan Jones',2013,'Viking','Biography, History, Politics',670026654,NULL,0,NULL,NULL,NULL,0,0.00),(42,'Division to Unification in Imperial China: The Three Kingdoms to the Tang Dynasty','Jing Liu',2016,'Stone Bridge Press','Biography, History, Politics',1611720303,NULL,0,NULL,NULL,NULL,0,0.00),(43,'The Heist','Janet Evanovich, Lee Goldberg',2013,'Bantam','Comedy, Suspense',345543041,NULL,0,NULL,NULL,NULL,0,0.00),(44,'The History of the Computer: People, Inventions, and Technology that Changed Our World','Rachel Ignotosky',2022,'Ten Speed Press','Computers, History, Science, Technology',1984857428,NULL,0,NULL,NULL,NULL,0,0.00),(45,'From Bean to Bar: A Chocolate Lover’s Guide to Britain','Andrew Baker',2020,'AA Publishing','Food, Travel',749581832,NULL,0,NULL,NULL,NULL,0,0.00),(46,'Understanding The British: A hilarious guide from Apologising to Wimbledon','Adam Fletcher',2022,'Independently published','Comedy, Travel',1724018205,NULL,0,NULL,NULL,NULL,0,0.00),(47,'Food in History','Reay Tannahill',1995,'Crown','Food, History',517884046,NULL,0,NULL,NULL,NULL,0,0.00),(48,'An Edible History of Humanity','Tom Standage',2010,'Bloomsbury USA ','Food, History',802719910,NULL,0,NULL,NULL,NULL,0,0.00),(49,'The Hitchhikers Guide to the Galaxy','Douglas Adams',2004,'Crown','Comedy, Science Fiction, Young Adult',1400052920,NULL,0,NULL,NULL,NULL,0,0.00),(50,'100 Things to Do in Asheville Before You Die','Kristy Tolley',2021,'Reedy Press','Travel',16810629510,NULL,0,NULL,NULL,NULL,0,0.00);
/*!40000 ALTER TABLE `Book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fee`
--

DROP TABLE IF EXISTS `Fee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fee` (
  `fee_id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) DEFAULT NULL,
  `fee_amount` decimal(10,2) DEFAULT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`fee_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `Fee_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `Book` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fee`
--

LOCK TABLES `Fee` WRITE;
/*!40000 ALTER TABLE `Fee` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Librarian`
--

DROP TABLE IF EXISTS `Librarian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Librarian` (
  `librarian_id` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`librarian_id`),
  UNIQUE KEY `librarian_id` (`librarian_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Librarian`
--

LOCK TABLES `Librarian` WRITE;
/*!40000 ALTER TABLE `Librarian` DISABLE KEYS */;
INSERT INTO `Librarian` VALUES (1,'Patrick','Brantseg','purplelady@sol.com','rbasehart','&iy6oso!YJoad4kr'),(2,'Mary','Pehl','noescape@castlef.com','chickenbiscuitt','&&ikPk@mMB4pK$o4');
/*!40000 ALTER TABLE `Librarian` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Patron`
--

DROP TABLE IF EXISTS `Patron`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Patron` (
  `patron_id` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`patron_id`),
  UNIQUE KEY `patron_id` (`patron_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Patron`
--

LOCK TABLES `Patron` WRITE;
/*!40000 ALTER TABLE `Patron` DISABLE KEYS */;
INSERT INTO `Patron` VALUES (1,'Joel','Robinson','robotfriends@sol.com','jhodgrob','#k#eJH85?gkJC6&3'),(2,'Clayton','Forrestor','obeyme@deep13.com','doctorevil','7Li8k3b@x$LkQFBM'),(3,'Crow','Robot','arthurgold@sol.com','artfuldodger','CkH9#?ek4qKTPh$5'),(4,'J.','Weinstein','hiddengypsy@mst3k.net','richardb','5!nRBJKKxkTpbEXH'),(5,'Tom','Servo','smoothtalker@sol.com','weathernine','x#SD9x8geA#Nh4C3'),(6,'Laurence','Erhardt','irminion@deep13.com','dontlook','PJJMiY#L&8?afcN7'),(7,'Jim','Mallon','rbayhart@gsnail.com','ramchips','ndQeffX#3&mPMy7F'),(8,'Kevin','Murphy','professorbobo@castlef.com','sonofcoco','YjSNS4#bpjoPeeY@'),(9,'Frank','Conniff','mybeautifulhair@deep13.com','hitthebutton','5S46#BT6!TG6t738'),(10,'Mike','Nelson','getmedown@sol.com','torgotheme','7jkFakbd5mFdA?@&'),(11,'Pearl','Forrestor','imincharge@castlef.com','cheezits','jJn!@7BC9yfrh#Ce'),(12,'Bill','Corbett','brainguy@castlef.com','observer','C5pDf#MgGhj5i&7G');
/*!40000 ALTER TABLE `Patron` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_admin`
--

DROP TABLE IF EXISTS `app_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_admin` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `checkout_limit` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_admin`
--

LOCK TABLES `app_admin` WRITE;
/*!40000 ALTER TABLE `app_admin` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_book`
--

DROP TABLE IF EXISTS `app_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_book` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `genre` varchar(255) NOT NULL,
  `isbn` int(11) NOT NULL,
  `userid` varchar(255) NOT NULL,
  `onhold` tinyint(1) NOT NULL,
  `checkout` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_book`
--

LOCK TABLES `app_book` WRITE;
/*!40000 ALTER TABLE `app_book` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_librarian`
--

DROP TABLE IF EXISTS `app_librarian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_librarian` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_librarian`
--

LOCK TABLES `app_librarian` WRITE;
/*!40000 ALTER TABLE `app_librarian` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_librarian` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_patron`
--

DROP TABLE IF EXISTS `app_patron`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_patron` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `password` varchar(255) NOT NULL,
  `user_id` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_patron`
--

LOCK TABLES `app_patron` WRITE;
/*!40000 ALTER TABLE `app_patron` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_patron` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Patrons');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add admin',1,'add_admin'),(2,'Can change admin',1,'change_admin'),(3,'Can delete admin',1,'delete_admin'),(4,'Can view admin',1,'view_admin'),(5,'Can add book',2,'add_book'),(6,'Can change book',2,'change_book'),(7,'Can delete book',2,'delete_book'),(8,'Can view book',2,'view_book'),(9,'Can add librarian',3,'add_librarian'),(10,'Can change librarian',3,'change_librarian'),(11,'Can delete librarian',3,'delete_librarian'),(12,'Can view librarian',3,'view_librarian'),(13,'Can add patron',4,'add_patron'),(14,'Can change patron',4,'change_patron'),(15,'Can delete patron',4,'delete_patron'),(16,'Can view patron',4,'view_patron'),(17,'Can add log entry',5,'add_logentry'),(18,'Can change log entry',5,'change_logentry'),(19,'Can delete log entry',5,'delete_logentry'),(20,'Can view log entry',5,'view_logentry'),(21,'Can add permission',6,'add_permission'),(22,'Can change permission',6,'change_permission'),(23,'Can delete permission',6,'delete_permission'),(24,'Can view permission',6,'view_permission'),(25,'Can add group',7,'add_group'),(26,'Can change group',7,'change_group'),(27,'Can delete group',7,'delete_group'),(28,'Can view group',7,'view_group'),(29,'Can add user',8,'add_user'),(30,'Can change user',8,'change_user'),(31,'Can delete user',8,'delete_user'),(32,'Can view user',8,'view_user'),(33,'Can add content type',9,'add_contenttype'),(34,'Can change content type',9,'change_contenttype'),(35,'Can delete content type',9,'delete_contenttype'),(36,'Can view content type',9,'view_contenttype'),(37,'Can add session',10,'add_session'),(38,'Can change session',10,'change_session'),(39,'Can delete session',10,'delete_session'),(40,'Can view session',10,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$lMeG5yrU2xoIISh3qYTBkG$S8iluDRur5vR4jqMz5NTnXa4rvkJ0dplzCU9m6VTTCE=','2024-02-27 19:45:32.738582',1,'admin','','','admin@admin.com',1,1,'2024-02-27 18:41:19.317301'),(2,'pbkdf2_sha256$600000$myDGCxBtmuiqeOwwFDaHQU$OMgxYeYXgjYc2SGZSXwb28AoFIJXbCqwqO4U2voxkGg=','2024-03-01 17:21:38.178083',0,'connor_user','','','conman0503@gmail.com',0,1,'2024-02-27 18:43:50.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,2,1);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-02-27 18:42:26.750380','1','Patrons',1,'[{\"added\": {}}]',7,1),(2,'2024-02-27 18:43:51.439155','2','connor_user',1,'[{\"added\": {}}]',8,1),(3,'2024-02-27 18:49:36.552711','2','connor_user',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',8,1),(4,'2024-02-27 19:08:29.806431','2','connor_user',2,'[{\"changed\": {\"fields\": [\"Email address\"]}}]',8,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (5,'admin','logentry'),(1,'app','admin'),(2,'app','book'),(3,'app','librarian'),(4,'app','patron'),(7,'auth','group'),(6,'auth','permission'),(8,'auth','user'),(9,'contenttypes','contenttype'),(10,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-02-23 17:03:07.963252'),(2,'auth','0001_initial','2024-02-23 17:03:08.355429'),(3,'admin','0001_initial','2024-02-23 17:03:08.439939'),(4,'admin','0002_logentry_remove_auto_add','2024-02-23 17:03:08.451482'),(5,'admin','0003_logentry_add_action_flag_choices','2024-02-23 17:03:08.463741'),(6,'app','0001_initial','2024-02-23 17:03:08.541528'),(7,'app','0002_rename_name_patron_password_remove_admin_name_and_more','2024-02-23 17:03:08.602349'),(8,'app','0003_remove_book_date_published_remove_book_publisher','2024-02-23 17:03:08.643840'),(9,'app','0004_delete_user_alter_admin_options_alter_book_options_and_more','2024-02-23 17:03:08.662465'),(10,'contenttypes','0002_remove_content_type_name','2024-02-23 17:03:08.729597'),(11,'auth','0002_alter_permission_name_max_length','2024-02-23 17:03:08.759410'),(12,'auth','0003_alter_user_email_max_length','2024-02-23 17:03:08.789651'),(13,'auth','0004_alter_user_username_opts','2024-02-23 17:03:08.801691'),(14,'auth','0005_alter_user_last_login_null','2024-02-23 17:03:08.842200'),(15,'auth','0006_require_contenttypes_0002','2024-02-23 17:03:08.847719'),(16,'auth','0007_alter_validators_add_error_messages','2024-02-23 17:03:08.860596'),(17,'auth','0008_alter_user_username_max_length','2024-02-23 17:03:08.888800'),(18,'auth','0009_alter_user_last_name_max_length','2024-02-23 17:03:08.927564'),(19,'auth','0010_alter_group_name_max_length','2024-02-23 17:03:08.956151'),(20,'auth','0011_update_proxy_permissions','2024-02-23 17:03:08.971542'),(21,'auth','0012_alter_user_first_name_max_length','2024-02-23 17:03:08.998822'),(22,'sessions','0001_initial','2024-02-23 17:03:09.040272');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('qbkfhvzxc0hjtnxpuj14ug7i1y0rlm2f','.eJxVjDsOwjAUBO_iGlmO4y8lPWew1n4PHECJFCcV4u4kUgpod2b2LRLWpaa18ZwGEmehxel3yyhPHndAD4z3SZZpXOYhy12RB23yOhG_Lof7d1DR6lY7i4LiyFjKZFTMpKhX7Bm9dzdE7hG6oB0pAx9j6LTnAnAOm2yiFZ8vAuQ4OA:1rg6Zm:XxL8QpzN27USVTZ-YuPkpE0vaMHjToRaY7viJg4pIVk','2024-03-15 17:21:38.182585');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-01 20:04:29
