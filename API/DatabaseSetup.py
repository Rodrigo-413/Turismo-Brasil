import mysql.connector
from mysql.connector import Error

class DatabaseSetup:
    def __init__(self):
        self.host = 'localHost'
        self.user = 'root'
        self.password = '16022006'
        self.database = 'misout_db'
    
    def create_connection(self):
        """Cria conexão com o MySQL"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            return connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None
    
    def create_database(self):
        """Cria o banco de dados"""
        try:
            connection = self.create_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                print(f"Banco de dados '{self.database}' criado com sucesso!")
                cursor.close()
                connection.close()
        except Error as e:
            print(f"Erro ao criar banco de dados: {e}")
    
    def create_tables(self):
        """Cria as 5 entidades principais do sistema"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            cursor = connection.cursor()
            
            # 1. ENTIDADE: USUÁRIOS (Cadastro/Login)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nome_completo VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    senha VARCHAR(255) NOT NULL,
                    tipo_plano ENUM('turista', 'viajante', 'explorador') DEFAULT 'turista',
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ativo BOOLEAN DEFAULT TRUE
                )
            ''')
            
            # 2. ENTIDADE: DESTINOS (Seleção de cidades)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS destinos (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nome VARCHAR(100) NOT NULL,
                    estado VARCHAR(2) NOT NULL,
                    apelido VARCHAR(50),
                    descricao TEXT,
                    imagem_url VARCHAR(255)
                )
            ''')
            
            # 3. ENTIDADE: CATEGORIAS (Botões de filtro)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categorias (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nome VARCHAR(50) NOT NULL,
                    icone VARCHAR(100)
                )
            ''')
            
            # 4. ENTIDADE: PONTOS_TURISTICOS (Inscrição de locais)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pontos_turisticos (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    destino_id INT NOT NULL,
                    categoria_id INT NOT NULL,
                    nome VARCHAR(100) NOT NULL,
                    endereco TEXT,
                    ponto_referencia VARCHAR(100),
                    tipo_turismo VARCHAR(50),
                    dias_funcionamento VARCHAR(100),
                    preco_minimo DECIMAL(10,2),
                    necessita_ingresso BOOLEAN,
                    descricao TEXT,
                    usuario_cadastrou INT,
                    aprovado BOOLEAN DEFAULT FALSE,
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (destino_id) REFERENCES destinos(id),
                    FOREIGN KEY (categoria_id) REFERENCES categorias(id),
                    FOREIGN KEY (usuario_cadastrou) REFERENCES usuarios(id)
                )
            ''')
            
            # 5. ENTIDADE: ASSINATURAS (Planos e pagamentos)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS assinaturas (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    usuario_id INT NOT NULL,
                    tipo_plano ENUM('viajante', 'explorador') NOT NULL,
                    data_inicio DATE NOT NULL,
                    data_fim DATE NOT NULL,
                    valor DECIMAL(10,2) NOT NULL,
                    status ENUM('ativa', 'cancelada', 'expirada') DEFAULT 'ativa',
                    metodo_pagamento ENUM('cartao', 'pix'),
                    telefone VARCHAR(20),
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            ''')

            # 6. ENTIDADE: PLANOS (Tipos de assinatura disponíveis)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS planos (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nome VARCHAR(50) NOT NULL,
                    tipo ENUM('turista', 'viajante', 'explorador') UNIQUE NOT NULL,
                    valor DECIMAL(10,2) NOT NULL,
                    descricao TEXT,
                    beneficios TEXT,
                    ativo BOOLEAN DEFAULT TRUE
                )
            ''')
            
            connection.commit()
            print("Todas as tabelas foram criadas com sucesso!")
            
            cursor.close()
            connection.close()
            
        except Error as e:
            print(f"Erro ao criar tabelas: {e}")
    
    def insert_sample_data(self):
        """Insere dados de exemplo para teste"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            cursor = connection.cursor()
            

            destinos = [
                ('São Paulo', 'SP', 'Terra da garoa', 'Maior cidade do Brasil', '/assets/sao-paulo.jpg'),
                ('Campinas', 'SP', 'Princesa d\'Oeste', 'Cidade universitária', '/assets/campinas.jpg'),
                ('Campos do Jordão', 'SP', 'Suíça Brasileira', 'Cidade serrana', '/assets/campos-jordao.jpg'),
                ('Ubatuba', 'SP', 'Capital do Surf', 'Cidade com belas praias', '/assets/ubatuba.jpg')
            ]
            
            cursor.executemany('''
                INSERT IGNORE INTO destinos (nome, estado, apelido, descricao, imagem_url)
                VALUES (%s, %s, %s, %s, %s)
            ''', destinos)
            

            categorias = [
                ('Museus', '🏛️'),
                ('Estádios', '⚽'),
                ('Shoppings', '🛍️'),
                ('Eventos', '🎪'),
                ('Teatros', '🎭'),
                ('Parques', '🌳'),
                ('Restaurantes', '🍽️'),
                ('Igrejas', '⛪')
            ]
            
            cursor.executemany('''
                INSERT IGNORE INTO categorias (nome, icone)
                VALUES (%s, %s)
            ''', categorias)
            

            cursor.execute("SELECT id, nome FROM destinos")
            destinos_ids = {nome: id for id, nome in cursor.fetchall()}
            
            cursor.execute("SELECT id, nome FROM categorias")
            categorias_ids = {nome: id for id, nome in cursor.fetchall()}
            
            # PONTOS TURÍSTICOS - SÃO PAULO
            pontos_sp = [
                # Museus SP
                (destinos_ids['São Paulo'], categorias_ids['Museus'], 'Museu do Ipiranga', 
                'Parque da Independência, s/n - Ipiranga', 'Próximo ao Monumento à Independência',
                'Cultural', 'Terça a Domingo', 20.00, True),
                
                (destinos_ids['São Paulo'], categorias_ids['Museus'], 'MASP', 
                'Av. Paulista, 1578 - Bela Vista', 'Em frente ao Trianon',
                'Cultural', 'Terça a Domingo', 50.00, True),
                
                (destinos_ids['São Paulo'], categorias_ids['Museus'], 'Pinacoteca', 
                'Praça da Luz, 2 - Luz', 'Estação da Luz',
                'Cultural', 'Quarta a Segunda', 20.00, True),
                
                # Estádios SP
                (destinos_ids['São Paulo'], categorias_ids['Estádios'], 'Allianz Parque', 
                'Av. Francisco Matarazzo, 1705 - Água Branca', 'Parque Trianon',
                'Esportivo', 'Diariamente', 80.00, True),
                
                (destinos_ids['São Paulo'], categorias_ids['Estádios'], 'Morumbi', 
                'Praça Roberto Gomes Pedrosa, 1 - Morumbi', 'Shopping Morumbi',
                'Esportivo', 'Diariamente', 60.00, True),
                
                # Shoppings SP
                (destinos_ids['São Paulo'], categorias_ids['Shoppings'], 'Shopping Ibirapuera', 
                'Av. Ibirapuera, 3103 - Moema', 'Parque Ibirapuera',
                'Compras', 'Segunda a Sábado', 0.00, False),
                
                (destinos_ids['São Paulo'], categorias_ids['Shoppings'], 'Shopping Eldorado', 
                'Av. Rebouças, 3970 - Pinheiros', 'Marginal Pinheiros',
                'Compras', 'Segunda a Sábado', 0.00, False),
                
                # Teatros SP
                (destinos_ids['São Paulo'], categorias_ids['Teatros'], 'Teatro Municipal', 
                'Praça Ramos de Azevedo, s/n - Centro', 'Vale do Anhangabaú',
                'Cultural', 'Terça a Domingo', 40.00, True),
                
                # Parques SP
                (destinos_ids['São Paulo'], categorias_ids['Parques'], 'Parque Ibirapuera', 
                'Av. Pedro Álvares Cabral - Vila Mariana', 'Museu de Arte Moderna',
                'Natureza', 'Diariamente', 0.00, False),
                
                (destinos_ids['São Paulo'], categorias_ids['Parques'], 'Parque do Carmo', 
                'Av. Afonso de Sampaio e Sousa, 951 - Itaquera', 'Lago das Rosas',
                'Natureza', 'Diariamente', 0.00, False)
            ]
            
            # PONTOS TURÍSTICOS - CAMPINAS
            pontos_campinas = [
                # Museus Campinas
                (destinos_ids['Campinas'], categorias_ids['Museus'], 'Museu Carlos Gomes', 
                'Praça Bento Quirino, 14 - Centro', 'Theatro Carlos Gomes',
                'Cultural', 'Terça a Sexta', 10.00, True),
                
                # Estádios Campinas
                (destinos_ids['Campinas'], categorias_ids['Estádios'], 'Moisés Lucarelli', 
                'Av. Dr. Thomaz Alves, 144 - Ponte Preta', 'Ponte Preta',
                'Esportivo', 'Diariamente', 30.00, True),
                
                # Shoppings Campinas
                (destinos_ids['Campinas'], categorias_ids['Shoppings'], 'Shopping Iguatemi', 
                'Av. Iguatemi, 777 - Vila Brandina', 'Marginal Castelo Branco',
                'Compras', 'Segunda a Sábado', 0.00, False),
                
                # Parques Campinas
                (destinos_ids['Campinas'], categorias_ids['Parques'], 'Parque Portugal', 
                'Av. Dr. Heitor Penteado, 1671 - Taquaral', 'Lagoa do Taquaral',
                'Natureza', 'Diariamente', 0.00, False),
                
                # Restaurantes Campinas
                (destinos_ids['Campinas'], categorias_ids['Restaurantes'], 'Restaurante Chapéu de Palha', 
                'Rua José Paulino, 1367 - Centro', 'Praça Carlos Gomes',
                'Gastronômico', 'Terça a Domingo', 80.00, False)
            ]
            
            # PONTOS TURÍSTICOS - CAMPOS DO JORDÃO
            pontos_campos = [
                # Museus Campos
                (destinos_ids['Campos do Jordão'], categorias_ids['Museus'], 'Museu Felícia Leirner', 
                'Av. Dr. Luis Arrobas Martins, 1880 - Alto da Boa Vista', 'Auditório Cláudio Santoro',
                'Cultural', 'Terça a Domingo', 20.00, True),
                
                # Restaurantes Campos
                (destinos_ids['Campos do Jordão'], categorias_ids['Restaurantes'], 'Baden Baden', 
                'Av. Dr. Januário Miráglia, 2497 - Vila Jaguaribe', 'Centro de Campos',
                'Gastronômico', 'Diariamente', 120.00, False),
                
                (destinos_ids['Campos do Jordão'], categorias_ids['Restaurantes'], 'Villa Capuano', 
                'Rua Dr. José Maria de Almeida, 251 - Capivari', 'Praça de Capivari',
                'Gastronômico', 'Diariamente', 90.00, False),
                
                # Parques Campos
                (destinos_ids['Campos do Jordão'], categorias_ids['Parques'], 'Parque Amantikir', 
                'Estrada Municipal Pedro Paulo, 2783 - Bairro do Loteamento', 'Entrada de Campos',
                'Natureza', 'Diariamente', 45.00, True),
                
                # Igrejas Campos
                (destinos_ids['Campos do Jordão'], categorias_ids['Igrejas'], 'Igreja de São João', 
                'Praça São João, 52 - Abernéssia', 'Centro de Abernéssia',
                'Religioso', 'Diariamente', 0.00, False)
            ]
            
            # Inserir todos os pontos turísticos
            todos_pontos = pontos_sp + pontos_campinas + pontos_campos
            
            cursor.executemany('''
                INSERT IGNORE INTO pontos_turisticos 
                (destino_id, categoria_id, nome, endereco, ponto_referencia, tipo_turismo, 
                dias_funcionamento, preco_minimo, necessita_ingresso, aprovado) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
            ''', todos_pontos)
            
            connection.commit()
            print("Dados de exemplo inseridos com sucesso!")
            
            cursor.execute("""
                SELECT d.nome as cidade, COUNT(pt.id) as total_pontos
                FROM destinos d 
                LEFT JOIN pontos_turisticos pt ON d.id = pt.destino_id AND pt.aprovado = TRUE
                GROUP BY d.nome
            """)
            
            stats = cursor.fetchall()
            print("\n📊 ESTATÍSTICAS DOS PONTOS TURÍSTICOS:")
            for cidade, total in stats:
                status = "✅ COM PONTOS" if total > 0 else "❌ SEM PONTOS"
                print(f"  {cidade}: {total} pontos - {status}")
            
            cursor.close()
            connection.close()
            
        except Error as e:
            print(f"Erro ao inserir dados de exemplo: {e}")
    
    def run_setup(self):
        """Executa o setup completo do banco de dados"""
        print("Iniciando setup do banco de dados MISOUT...")
        
        # Criar banco de dados
        self.create_database()
        
        # Criar tabelas
        self.create_tables()
        
        # Inserir dados de exemplo
        self.insert_sample_data()
        
        print("Setup do banco de dados concluído!")

if __name__ == "__main__":
    db_setup = DatabaseSetup()
    
    # Configurações do banco
    db_setup.host = 'localHost'
    db_setup.user = 'root'
    db_setup.password = '16022006'
    db_setup.database = 'misout_db'
    
    # Executa o setup completo
    db_setup.run_setup()