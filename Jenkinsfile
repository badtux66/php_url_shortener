pipeline {
    agent any

    environment {
        SSH_USER = 'pusula'
        SSH_PASSWORD = 'pusula+2023'
    }

    stages {
        stage('Clean Up') {
            steps {
                deleteDir()
            }
        }

        stage('Install PHP and Composer') {
            steps {
                withEnv(['TERM=dumb']) {
                    sh """
                        echo ${SSH_PASSWORD} | sudo -S yum -y install epel-release
                        echo ${SSH_PASSWORD} | sudo -S yum -y install https://rpms.remirepo.net/enterprise/remi-release-8.rpm
                        echo ${SSH_PASSWORD} | sudo -S yum -y install yum-utils
                        echo ${SSH_PASSWORD} | sudo -S yum-config-manager --enable remi-php80
                        echo ${SSH_PASSWORD} | sudo -S yum -y update
                        echo ${SSH_PASSWORD} | sudo -S yum -y install php php-cli php-common php-fpm php-gd php-json php-mbstring php-mysqlnd php-opcache php-pdo php-xml php-tokenizer php-curl unzip
                        curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer
                    """
                }
            }
        }

        stage('Clone repository') {
            steps {
                sh "PATH=$PATH:/usr/bin git clone -b master https://github.com/badtux66/polr"
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'composer install'
            }
        }

        stage('Build application') {
            steps {
                sh 'php artisan build'
            }
        }

        stage('Deploy application') {
            steps {
                sh "sshpass -p ${SSH_PASSWORD} rsync -avz --exclude '.env' ./ ${SSH_USER}@192.168.30.21:/var/www/gshortener"
                sh "sshpass -p ${SSH_PASSWORD} ssh ${SSH_USER}@192.168.30.21 'cp /var/www/gshortener/.env.production /var/www/gshortener/.env'"
            }
        }

        stage('Run migrations') {
            steps {
                sh "sshpass -p ${SSH_PASSWORD} ssh ${SSH_USER}@192.168.30.21 'cd /var/www/gshortener && php artisan migrate --force'"
            }
        }
    }
}
