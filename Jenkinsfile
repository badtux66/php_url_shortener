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
                script {
                    sh 'echo "pusula+2023" | sudo -S yum -y install epel-release'
                    sh 'echo "pusula+2023" | sudo -S yum -y install https://rpms.remirepo.net/enterprise/remi-release-8.rpm'
                    sh 'echo "pusula+2023" | sudo -S yum -y install yum-utils'
                    sh 'echo "pusula+2023" | sudo -S yum-config-manager --enable remi-php80'
                    sh 'echo "pusula+2023" | sudo -S yum -y update'
                    sh 'echo "pusula+2023" | sudo -S yum -y install php php-cli php-common php-fpm php-gd php-json php-mbstring php-mysqlnd php-opcache php-pdo php-xml php-tokenizer php-curl unzip'
                    sh 'curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer'
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
                sh "rsync -avz --exclude '.env' ./ ${SSH_USER}:${SSH_PASSWORD}@192.168.30.21:/var/www/gshortener"
                sh "ssh ${SSH_USER}@192.168.30.21 'cp /var/www/gshortener/.env.production /var/www/gshortener/.env'"
            }
        }

        stage('Run migrations') {
            steps {
                sh "ssh ${SSH_USER}@192.168.30.21 'cd /var/www/gshortener && php artisan migrate --force'"
            }
        }
    }
}
