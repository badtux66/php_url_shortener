pipeline {
    agent any

    environment {
        SSH_USER = 'pusula'
        SSH_PASSWORD = 'pusula+2023'
    }

    stages {
        stage('Clone repository') {
            steps {
                sh "PATH=$PATH:/usr/bin git clone -b main https://github.com/badtux66/polr"
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
