pipeline {
    agent any

    environment {
        SSH_USER = 'root'
        SSH_PASSWORD = 'pusula+2023'
    }

    stages {
        stage('Clean Up') {
            steps {
                deleteDir()
            }
        }


        stage('Clone repository') {
            steps {
                sh "git clone -b master https://github.com/badtux66/polr"
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'composer install --no-dev -o'
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
