CREATE TABLE `usuarios` (
   `id` int NOT NULL AUTO_INCREMENT,
   `nome` varchar(50) DEFAULT NULL,
   `saldo` decimal(10,2) DEFAULT '0.00',
   `cpf` varchar(11) DEFAULT NULL,
   `senha` varchar(255) DEFAULT NULL,
   `criado_em` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`id`)
 ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `transacoes` (
   `id` int NOT NULL AUTO_INCREMENT,
   `origem` int DEFAULT NULL,
   `destino` int DEFAULT NULL,
   `valor` decimal(10,2) NOT NULL,
   `tipo` varchar(20) DEFAULT NULL,
   `data` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`id`)
 ) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

